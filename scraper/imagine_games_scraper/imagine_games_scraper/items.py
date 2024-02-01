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
    brand = scrapy.Field()
    contributors = scrapy.Field()
    review = scrapy.Field()
    objects = scrapy.Field()
    embeded_content = scrapy.Field()
    
# Scrapy Item used to define the structure of video content
class Video(scrapy.Item):
    url = scrapy.Field()
    legacy_id = scrapy.Field()
    thumbnail = scrapy.Field()
    slug = scrapy.Field()
    publish_date = scrapy.Field()
    modify_date = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    events = scrapy.Field()
    objects = scrapy.Field()
    assets = scrapy.Field()
    vertical = scrapy.Field()
    contributors = scrapy.Field()
    metadata = scrapy.Field()

# Scrapy Item used to define the structure of reporter content
class Reporter(scrapy.Item):
    legacy_id = scrapy.Field()
    legacy_author_id = scrapy.Field()
    uri = scrapy.Field()
    name = scrapy.Field()
    nickname = scrapy.Field()
    avatar = scrapy.Field()
    cover = scrapy.Field()
    position = scrapy.Field()
    bio = scrapy.Field()
    location = scrapy.Field()
    socials = scrapy.Field()

# Scrapy Item used to define the structure of entertainment
class Entertainment(scrapy.Item):
    legacy_id = scrapy.Field()
    uri = scrapy.Field()
    slug = scrapy.Field()
    wiki_slug = scrapy.Field()
    type = scrapy.Field()
    cover = scrapy.Field()
    names = scrapy.Field()
    descriptions = scrapy.Field()
    franchises = scrapy.Field()
    genres = scrapy.Field()
    features = scrapy.Field()
    producers = scrapy.Field()
    publishers = scrapy.Field()
    regions = scrapy.Field()


# Possibly include Review Item
# Possibly include Wiki Item