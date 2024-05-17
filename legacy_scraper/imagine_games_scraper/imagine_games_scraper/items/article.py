import scrapy
from imagine_games_scraper.items.base_item import Item

class Article(Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    content_id = scrapy.Field()
    article_content_id = scrapy.Field()
    review_id = scrapy.Field()

    __tablename__ = "articles"

    def __init__(self, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)

class ArticleContent(Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    hero_video_content_id = scrapy.Field()
    hero_video_content_slug = scrapy.Field()
    processed_html = scrapy.Field()

    __tablename__ = "article_contents"

    def __init__(self, *args, **kwargs):
        super(ArticleContent, self).__init__(*args, **kwargs)
