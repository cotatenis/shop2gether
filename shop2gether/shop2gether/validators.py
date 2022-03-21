from schematics.models import Model
from schematics.types import URLType, StringType, ListType, FloatType, DateTimeType, BooleanType, ModelType

class StockInfo(Model):
    is_in_stock = BooleanType(required=True)
    label = StringType()
    oldPrice = StringType()
    price = StringType()
    products = ListType(StringType)
    qty_stock = StringType()

class Shop2GetherItem(Model):
    brand = StringType(required=True)
    product = StringType(required=True)
    price = FloatType(required=True)
    url = URLType(required=True)
    description = ListType(StringType)
    sku = StringType(required=True)
    usku = StringType(required=True)
    stock_info = ListType(ModelType(StockInfo))
    timestamp = DateTimeType(required=True)
    spider = ListType(StringType, required=True)
    spider_version = StringType(required=True)
    image_urls = ListType(URLType)
    image_uris = ListType(StringType, required=True)
    reference_first_image = StringType()

