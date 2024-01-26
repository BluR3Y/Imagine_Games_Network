# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImagineGamesScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# Scrapy Item used to define the structure of article content
class Article(scrapy.Item):
    url = scrapy.Field()
    legacy_id = scrapy.Field()
    slug = scrapy.Field()
    category = scrapy.Field()
    vertical = scrapy.Field()
    cover = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    description = scrapy.Field()
    excerpt = scrapy.Field()
    processedHtml = scrapy.Field()
    publish_date = scrapy.Field()
    modify_date = scrapy.Field()
    contributors = scrapy.Field()
    review = scrapy.Field()
    objects = scrapy.Field()
    
# Scrapy Item used to define the structure of video content
class Video(scrapy.Item):
    url = scrapy.Field()
    thumbnail = scrapy.Field()
    slug = scrapy.Field()
    published_date = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    duration = scrapy.Field()
    object = scrapy.Field()
    assets = scrapy.Field()
    vertical = scrapy.Field()
    contributors = scrapy.Field()


# Possibly include Review Item
# Possibly include Wiki Item