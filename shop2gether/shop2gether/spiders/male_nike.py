from shop2gether.spiders.female_nike import Shop2GNikeFemaleSpider

class Shop2GNikeMaleSpider(Shop2GNikeFemaleSpider):
    name = 'shop2-nike-male'
    start_urls = ["https://www.shop2gether.com.br/masculino/calcados/category/t-nis.html?marca=2854"]