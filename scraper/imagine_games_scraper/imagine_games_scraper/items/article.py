import scrapy
from uuid import uuid4

# Scrapy Item used to define the structure of article content
# AKA MordernArticle
class Article(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    content = scrapy.Field()    # id referencing ModernContent
    article = scrapy.Field()    # id referencing ArticleContent
    review = scrapy.Field()     # Reference to official Review

    def __init__(self, article_data = {}, manual_assignments = {}, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())
        self['content'] = manual_assignments.get('content', article_data.get('content'))
        self['article'] = manual_assignments.get('article', article_data.get('article'))
        self['review'] = manual_assignments.get('review', article_data.get('review'))

class ArticleContent(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    hero_video_content_id = scrapy.Field()
    hero_video_content_slug = scrapy.Field()
    processed_html = scrapy.Field()

    def __init__(self, content_data = {}, manual_assignment = {}, *args, **kwargs):
        super(ArticleContent, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())
        self['legacy_id'] = manual_assignment.get('id', content_data.get('id'))
        self['hero_video_content_id'] = manual_assignment.get('hero_video_content_id', content_data.get('heroVideoContentId'))
        self['hero_video_content_slug'] = manual_assignment.get('hero_video_content_slug', content_data.get('heroVideoContentSlug'))
        self['processed_html'] = manual_assignment.get('processed_html', content_data.get('processedHtml'))

# Missing: Embed connection