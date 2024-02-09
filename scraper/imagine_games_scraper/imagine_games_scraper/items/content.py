import scrapy

class ImagineGamesScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# Scrapy Item used to define the structure of article content
# AKA MordernArticle
class Article(scrapy.Item):
    legacy_id = scrapy.Field()
    content = scrapy.Field()    # id referencing ModernContent
    article = scrapy.Field()    # Embedded HTML
    embeds = scrapy.Field()
    review = scrapy.Field()     # Reference to official Review

    def __init__(self, article_data = {}, manual_assignments = {}, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)

        self['legacy_id'] = manual_assignments.get('id', article_data.get('id'))
        self['content'] = manual_assignments.get('content', article_data.get('content'))
        self['article'] = manual_assignments.get('article', article_data.get('article'))
        self['embeds'] = manual_assignments.get('embeds', article_data.get('embeds'))
        self['review'] = manual_assignments.get('review', article_data.get('review'))

class ArticleContent(scrapy.Item):
    legacy_id = scrapy.Field()
    hero_video_content_id = scrapy.Field()
    hero_video_content_slug = scrapy.Field()
    processed_html = scrapy.Field()
# Missing: Embed connection

# Scrapy Item used to define the structure of video content
# AKA ModernVideo
class Video(scrapy.Item):
    legacy_id = scrapy.Field()
    content = scrapy.Field()    # id referencing ModernContent
    metadata = scrapy.Field()   # id referencing VideoMetadata
    assets = scrapy.Field()     # id referncing VideoAsset

    def __init__(self, video_data = {}, manual_assignments = {}, *args, **kwargs):
        super(Video, self).__init__(*args, **kwargs)

        self['legacy_id'] = manual_assignments.get('id', video_data.get('id'))
        self['content'] = manual_assignments.get('content')
        self['metadata'] = manual_assignments.get('metadata', video_data.get('metadata'))
        self['assets'] = manual_assignments.get('assets', video_data.get('reviassetsew'))

# AKA ModernContent
class Content(scrapy.Item):
    legacy_id = scrapy.Field()
    url = scrapy.Field()
    slug = scrapy.Field()
    type = scrapy.Field()   # Article, Catalog, Slideshow, Video, Poll
    vertical = scrapy.Field() # News, Review
    cover = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    feed_title = scrapy.Field()
    feed_cover = scrapy.Field()
    excerpt = scrapy.Field()
    description = scrapy.Field()
    state = scrapy.Field()
    publish_date = scrapy.Field()
    modify_date = scrapy.Field()
    events = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field() # id referencing ContentCategory
    contributors = scrapy.Field() # id referencing Reporters
    attributes = scrapy.Field()     # id referencing Attributes: platform, genre, producer, franchise, etc
    objects = scrapy.Field()  # id referencing objects

    def __init__(self, content_data = {}, manual_assignments = {}, *args, **kwargs):
        super(Content, self).__init__(*args, **kwargs)

        self['legacy_id'] = manual_assignments.get('id', content_data.get('id'))
        self['url'] = manual_assignments.get('url', content_data.get('url'))
        self['slug'] = manual_assignments.get('slug', content_data.get('slug'))
        self['type'] = manual_assignments.get('type', content_data.get('type'))
        self['vertical'] = manual_assignments.get('vertical', content_data.get('vertical'))
        self['cover'] = manual_assignments.get('cover', content_data.get('headerImageUrl'))
        self['title'] = manual_assignments.get('title', content_data.get('title'))
        self['subtitle'] = manual_assignments.get('subtitle', content_data.get('subtitle'))
        self['feed_title'] = manual_assignments.get('feedTitle', content_data.get('feedTitle'))
        self['feed_cover'] = manual_assignments.get('feed_cover', content_data['feedImage']['url'] if content_data.get('feedImage') else None)
        self['excerpt'] = manual_assignments.get('excerpt', content_data.get('excerpt'))
        self['description'] = manual_assignments.get('description', content_data.get('description'))
        self['state'] = manual_assignments.get('state', content_data.get('state'))
        self['publish_date'] = manual_assignments.get('publishDate', content_data.get('publishDate'))
        self['modify_date'] = manual_assignments.get('updatedAt', content_data.get('updatedAt'))
        self['events'] = manual_assignments.get('events', content_data.get('events'))
        self['brand'] = manual_assignments.get('brand', content_data.get('brand'))
        self['category'] = manual_assignments.get('category')
        self['contributors'] = manual_assignments.get('contributors')
        self['attributes'] = manual_assignments.get('attributes')
        self['objects'] = manual_assignments.get('objects')

class ContentCategory(scrapy.Item):
    legacy_id = scrapy.Field()
    name = scrapy.Field()

    def __init__(self, category_data = {}, manual_assignments = {}, *args, **kwargs):
        super(ContentCategory, self).__init__(*args, **kwargs)    

        self['legacy_id'] = manual_assignments.get('id', category_data.get('id'))
        self['name'] = manual_assignments.get('name', category_data.get('name'))

class Brand(scrapy.Item):
    legacy_id = scrapy.Field()
    slug = scrapy.Field()
    name = scrapy.Field()
    logo_light = scrapy.Field()
    logo_dark = scrapy.Field()

    def __init__(self, brand_data = {}, manual_assignments = {}, *args, **kwargs):
        super(Brand, self).__init__(*args, **kwargs)

        self['legacy_id'] = manual_assignments.get('id', brand_data.get('id'))
        self['slug'] = manual_assignments.get('slug', brand_data.get('slug'))
        self['name'] = manual_assignments.get('name', brand_data.get('name'))
        self['logo_light'] = manual_assignments.get('logo_light', brand_data.get('logoLight'))
        self['logo_dark'] = manual_assignments.get('logo_dark', brand_data.get('logoDark'))