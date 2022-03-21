from scrapy import Request, Spider
from time import sleep
from parsel import Selector
from shop2gether.items import Shop2GetherItem
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import JavascriptException
from collections import defaultdict
import re
import json
from scrapy.loader import ItemLoader
from scrapy.utils.project import get_project_settings
class Shop2GAdidasSpider(Spider):
    settings = get_project_settings()
    name = 'shop2-adidas'
    version = settings.get("VERSION")
    allowed_domains = ['www.shop2gether.com.br']
    start_urls = [
         #adidas originals
        'https://www.shop2gether.com.br/catalog/category/view/id/108260/?marca=1565',
         #adidas
         'https://www.shop2gether.com.br/catalog/category/view/id/108260/?marca=2378'
    ]
    options = ChromeOptions()
    options.headless = True
    driver = Chrome(options=options)
    def start_requests(self):
        for url in self.start_urls:
            yield Request(
                url=url, 
                callback=self.parse, 
            )
    def parse(self, response):
        #product details
        image_urls = []
        product_details = LinkExtractor(restrict_xpaths="//div[starts-with(@class, 'product-brand')]/a")
        links_product_details = [data.url for data in product_details.extract_links(response)]
        for url in links_product_details:
            self.driver.get(url)
            selector = Selector(text=self.driver.page_source)
            if url == 'https://www.shop2gether.com.br/tenis-superstar-slip-on-6.html':
                store_sku = 'FW7051'
                usku = "FW7051"
            else:    
                store_sku, usku = self.parse_sku(selector=selector, url=url)
            image_urls, reference_first_image = self.fetch_product_images(sku = usku)
            image_uris = self.parse_image_uris(sku=usku, images_list=image_urls)
            product_container = selector.xpath("//div[starts-with(@class, 'product-view')]")
            i = ItemLoader(item=Shop2GetherItem(), selector=product_container)
            i.add_xpath('brand', "//a[starts-with(@href, '/catalog')]")
            i.add_xpath("product", "//div[starts-with(@class, 'product-name')]/span")
            i.add_xpath("price", "//p[starts-with(@class, 'special-price')]//span[starts-with(@id, 'product-price')]|//div[@class='price-info']//span[@class='price']")
            i.add_value("url", url)
            i.add_xpath("description", "//div[starts-with(@class, 'new-product-tabs-desc-content')]/p")
            i.add_value("sku", store_sku)
            i.add_value("usku", usku)
            i.add_value("stock_info", self.parse_product_labels(selector=selector))
            i.add_value("spider_version", self.version)
            i.add_value("spider", self.name)
            i.add_value("image_urls", image_urls)
            i.add_value("image_uris", image_uris)
            i.add_value("reference_first_image", reference_first_image)
            yield i.load_item()
        #paginate
        le_pagination = LinkExtractor(restrict_xpaths=("//div[starts-with(@class, 'pages')]//li/a"))
        pagination_urls = [data.url for data in le_pagination.extract_links(response)]
        if pagination_urls:
            for url in pagination_urls:
                yield Request(
                    url=url, 
                    callback=self.parse, 
                )

    def fetch_product_images(self, sku):
        container_imgs = []
        reference_first_image = ""
        sel = Selector(text=self.driver.page_source)
        raw_attr = sel.xpath("//div[@class='zoomWindowContainer']/div/@style").get()
        if raw_attr:
            image_url = raw_attr[raw_attr.find('url'):][4:].replace("\"","")[:-2]
            container_imgs.append(image_url)
            reference_first_image = f"gs://cotatenis-images/shop2gether/thumbs/400_400/{sku}_{image_url.split('/')[-1]}"
        imgs_elements = self.driver.find_elements_by_xpath("//ul[@class='product-image-thumbs']//li/a/img")
        for img_element in imgs_elements[1:]:
            try:
                self.driver.execute_script('document.getElementById("launcher").style.display = "none";')
            except JavascriptException:
                pass
            finally:
                img_element.click()
            sleep(2)
            sel = Selector(text=self.driver.page_source)
            raw_attr = sel.xpath("//div[@class='zoomWindowContainer']/div/@style").get()
            if raw_attr:
                image_url = raw_attr[raw_attr.find('url'):][4:].replace("\"","")[:-2]
                container_imgs.append(image_url)
        return container_imgs, reference_first_image


    def parse_product_labels(self, selector: Selector) -> list:
        """Process content inside several script tags to get information 
        about stock availability and shoes sizes. 

        Parameters
        ----------
        selector : [Selector]

        Returns
        -------
        [list]
            list of objects
        """
        label_container = []
        map_bool = defaultdict(lambda: "")
        map_bool['true'] = True
        map_bool['false'] = False
        script_labels = selector.xpath("//div[@class='product-options']//dl/following-sibling::script").get()
        re_labels = r'{\"id\":\"\d+\",\"label":\"\d+\",\"price\":\"\d+",\"oldPrice\":\"\d+\",\"products\":\[\"\d+\"\]}'
        raw_data_labels = re.findall(re_labels, script_labels)
        for raw_lb in raw_data_labels:
            label_container.append(json.loads(raw_lb))
        script_tag = selector.xpath("//div[@class='product-options']//script").get()
        #script tag with id and stock bool info
        raw_ids_and_stock = re.findall(r'\"[0-9]+\":{\"\w+\":[false|true]+', script_tag)
        _ids = [re.findall(r'\d+', d)[0] for d in raw_ids_and_stock]
        bool_stocks = [re.findall(r'true|false', d)[0] for d in raw_ids_and_stock]
        bool_stocks = [map_bool[data] for data in bool_stocks]
        #stock quantity info
        raw_script_stock_info = re.findall(r'\"qty_stock\":\"\d+?.\d+\"}', script_tag)
        stock_qty = [re.findall(r'\d+?.\d+', value)[0] for value in raw_script_stock_info]
        data_mapping = {}
        for _id, bool, sqty in zip(_ids, bool_stocks, stock_qty):
            data_mapping[_id] = {'is_in_stock' : bool, 'qty_stock' : sqty}
        for data in label_container:
            _id = data.get("id")
            label = data.get("label")
            price = data.get("price")
            old_price = data.get("oldPrice")
            products = data.get("products")
            try:
                data_mapping[_id]['label'] = label
            except KeyError:
                continue
            try:
                data_mapping[_id]['price'] = price
            except KeyError:
                continue
            try:
                data_mapping[_id]['oldPrice'] = old_price
            except KeyError:
                continue
            try:
                data_mapping[_id]['products'] = products
            except KeyError:
                continue
        return [d for d in data_mapping.values()]

    def parse_sku(self, selector: Selector, url: str):
        store_sku = ""
        usku = ""
        sku_pattern = r'^[0-9A-Z]{6}_\w+'
        sku =  selector.xpath("//div[starts-with(@class, 'new-product-tabs-desc-content')]/p").re(r"SKU:[\s+]?\w+")
        if sku:
            store_sku = self.sku_cleaning(sku[0])
            usku = store_sku.split("_")[0]
        if not sku:
            try:
                store_sku = selector.xpath("//div[starts-with(@class, 'new-product-tabs-desc-content')]/p").re(r"SKU[\s+]?[\\xa0]?.+")[0].split("<span>")[1].split("</span>")[0]
            except IndexError:
                try:
                    raw_store_sku = selector.xpath("//div[starts-with(@class, 'new-product-tabs-desc-content')]/p").re(r"SKU[\s+]?[\\xa0]?.+")[0]
                except IndexError:
                    try:
                        store_sku = selector.xpath("//div[starts-with(@class, 'new-product-tabs-desc-content')]/p/span/@data-sheets-value").re(r"\w+_\w+")[0]
                    except IndexError:
                        store_sku = None
                        usku = None
                    else:
                        usku = store_sku.split("_")[0]
                else:
                    store_sku = re.search(r"\w+_\w+", raw_store_sku)
                    if store_sku:
                        store_sku = store_sku.group(0)
                        usku = store_sku.split("_")[0]
                        return store_sku, usku
                    else:
                        store_sku = None
                        usku = None
            else:
                if not re.search(sku_pattern, store_sku):
                   string_sku_store = ' '.join(selector.xpath("//div[starts-with(@class, 'new-product-tabs-desc-content')]/p").re(r"SKU[\s+]?[\\xa0]?.+"))
                   sku_match = re.findall(r'[0-9A-Z]{6}_\w+', string_sku_store)
                   if sku_match:
                       store_sku = sku_match[0]
                       usku = store_sku.split("_")[0]
                   else:
                       store_sku = None
                       usku = None
                else:
                    usku = store_sku.split("_")[0]
        return store_sku, usku

    
    def parse_image_uris(self, sku: str, images_list: list):
        return [f"{self.settings.get('IMAGES_STORE')}{sku}_{filename.split('/')[-1]}" for filename in images_list]

    @staticmethod
    def sku_cleaning(sku: str):
        return sku.replace("\xa0"," ").replace("\u00ae", " ").split(":")[1].strip()