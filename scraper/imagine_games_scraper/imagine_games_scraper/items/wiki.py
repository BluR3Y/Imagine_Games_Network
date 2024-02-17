import scrapy
from uuid import uuid4

class Wiki(scrapy.Item):
    id = scrapy.Field()