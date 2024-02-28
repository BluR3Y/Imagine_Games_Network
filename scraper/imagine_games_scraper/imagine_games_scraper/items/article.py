import scrapy
from uuid import uuid4

class Article(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    content_id = scrapy.Field()
    article_content_id = scrapy.Field()
    review_id = scrapy.Field()

    __tablename__ = "articles"

    def __init__(self, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())

    # def required_fields_filled(self):
    #     required_fields = ['content_id','article_content_id']

    #     for attr in required_fields:
    #         if self[attr] == None:
    #             return False
    #     return True
    # Last Here: Adding methods to scrapy items

class ArticleContent(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    hero_video_content_id = scrapy.Field()
    hero_video_content_slug = scrapy.Field()
    processed_html = scrapy.Field()

    __tablename__ = "article_contents"

    def __init__(self, *args, **kwargs):
        super(ArticleContent, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())