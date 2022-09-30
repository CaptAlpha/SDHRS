import scrapy

class Profile(scrapy.Item):
    name = scrapy.Field()
    specialty = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    website = scrapy.Field()
    rating = scrapy.Field()
    reviews = scrapy.Field()

class Reviews(scrapy.Item):
    date = scrapy.Field()
    rating = scrapy.Field()
    review = scrapy.Field()