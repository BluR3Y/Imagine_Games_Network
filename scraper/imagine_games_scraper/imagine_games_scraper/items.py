import scrapy
from uuid import uuid4

# class Image(scrapy.Item):
#     id = scrapy.Field()
#     legacy_id = scrapy.Field()
#     legacy_url = scrapy.Field()
#     url = scrapy.Field()
#     link = scrapy.Field()
#     caption = scrapy.Field()

class Item(scrapy.Item):
    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)

    obj = scrapy.Field()