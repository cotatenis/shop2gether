import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags, replace_escape_chars, strip_html5_whitespace
from scrapy.item import Item
from price_parser import parse_price

def get_price(text):
    return str(parse_price(text).amount)

def cleaning_description(text):
    return text.replace("\u00ae", " ").replace("\xa0", " ")
def sku_cleaning(sku):
    return sku.replace("\xa0"," ").replace("\u00ae", " ").split(":")[1].strip()


class Shop2GetherItem(Item):
    brand = scrapy.Field(input_processor=MapCompose(remove_tags, replace_escape_chars, strip_html5_whitespace), output_processor=TakeFirst())
    product = scrapy.Field(input_processor=MapCompose(remove_tags, replace_escape_chars, strip_html5_whitespace), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_tags, replace_escape_chars, strip_html5_whitespace, get_price), output_processor=TakeFirst())
    url = scrapy.Field(input_processor=MapCompose(strip_html5_whitespace), output_processor=TakeFirst())
    description = scrapy.Field(input_processor=MapCompose(remove_tags, replace_escape_chars, cleaning_description, strip_html5_whitespace))
    sku = scrapy.Field(output_processor=TakeFirst())
    usku = scrapy.Field(output_processor=TakeFirst())
    stock_info = scrapy.Field()
    timestamp = scrapy.Field()
    spider = scrapy.Field()
    spider_version = scrapy.Field(output_processor=TakeFirst())
    image_urls = scrapy.Field()
    image_uris = scrapy.Field()
    reference_first_image = scrapy.Field(output_processor=TakeFirst())