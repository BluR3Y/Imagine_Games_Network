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
    wiki = scrapy.Field()
    wiki_slug = scrapy.Field()
    type = scrapy.Field()
    cover = scrapy.Field()
    gallery = scrapy.Field()
    names = scrapy.Field()
    descriptions = scrapy.Field()
    franchises = scrapy.Field()
    genres = scrapy.Field()
    features = scrapy.Field()
    producers = scrapy.Field()
    publishers = scrapy.Field()
    regions = scrapy.Field()
    reviews = scrapy.Field()

class EntertainmentWiki(scrapy.Item):
    legacy_id = scrapy.Field()
    name = scrapy.Field()
    maps = scrapy.Field()
    navigation = scrapy.Field()

class WikiMap(scrapy.Item):
    name = scrapy.Field()
    slug = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    type = scrapy.Field()
    initial_zoom = scrapy.Field()
    min_zoom = scrapy.Field()
    max_zoom = scrapy.Field()
    initial_latitude = scrapy.Field()
    initial_longitude = scrapy.Field()
    tile_sets = scrapy.Field()
    background_color = scrapy.Field()

class Attribute(scrapy.Item):
    type = scrapy.Field()
    name = scrapy.Field()
    slug = scrapy.Field()

class Region(scrapy.Item):
    legacy_id = scrapy.Field()
    name = scrapy.Field()
    region = scrapy.Field()
    releases = scrapy.Field()

class Rating(scrapy.Item):
    legacy_id = scrapy.Field()
    type = scrapy.Field()
    name = scrapy.Field()
    slug = scrapy.Field()
    descriptors = scrapy.Field()

class ReporterReview(scrapy.Item):
    legacy_id = scrapy.Field()
    score = scrapy.Field()
    score_text = scrapy.Field()
    editors_choice = scrapy.Field()
    score_summary = scrapy.Field()
    review_date = scrapy.Field()

class UserReview(scrapy.Item):
    legacy_id = scrapy.Field()
    legacy_user_id = scrapy.Field()
    legacy_object_id = scrapy.Field()
    is_liked = scrapy.Field()
    score = scrapy.Field()
    text = scrapy.Field()
    is_spoiler = scrapy.Field()
    publish_date = scrapy.Field()
    modify_date = scrapy.Field()
    platform = scrapy.Field()
    tags = scrapy.Field()

class User(scrapy.Item):
    legacy_id = scrapy.Field()
    avatar = scrapy.Field()
    name = scrapy.Field()
    nickname = scrapy.Field()
    privacy = scrapy.Field()

class UserReviewTag(scrapy.Item):
    legacy_id = scrapy.Field()
    name =scrapy.Field()
    is_positive = scrapy.Field()

# Possibly include Wiki Item