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
    thumbnail = scrapy.Field()
    tags = scrapy.Field()
    category = scrapy.Field()
    reporter_name = scrapy.Field()
    reporter_avatar = scrapy.Field()
    headline = scrapy.Field()
    sub_headline = scrapy.Field()
    published_date = scrapy.Field()
    modified_date = scrapy.Field()

# Scrapy Item used to define the structure of video content
class Video(scrapy.Item):
    url = scrapy.Field()
    thumbnail = scrapy.Field()
    content_category = scrapy.Field()
    content_sub_category = scrapy.Field()
    reporter = scrapy.Field()

# Possibly include Review Item
# Possibly include Wiki Item