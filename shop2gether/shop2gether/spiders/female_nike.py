from shop2gether.spiders.adidas import Shop2GAdidasSpider
from parsel import Selector

class Shop2GNikeFemaleSpider(Shop2GAdidasSpider):
    name = 'shop2-nike-female'
    start_urls = ["https://www.shop2gether.com.br/feminino/calcados/category/tenis.html?marca=2854"]

    def parse_sku(self, selector: Selector, url: str):
        sku_pattern = r"\w+-\w+_\w+"
        store_sku =  selector.xpath("//div[starts-with(@class, 'new-product-tabs-desc-content')]/p").re(sku_pattern)
        if store_sku:
            return store_sku[0], store_sku[0].split("_")[0]
        else:
            return None, None
