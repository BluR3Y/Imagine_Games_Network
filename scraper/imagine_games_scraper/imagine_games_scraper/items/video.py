import scrapy

from imagine_games_scraper.items.base_item import Item

class Video(Item):
    legacy_id = scrapy.Field()
    content_id = scrapy.Field()
    metadata_id = scrapy.Field()

    __tablename__ = 'videos'

    def __init__(self, *args, **kwargs):
        super(Video, self).__init__(*args, **kwargs)

class VideoMetadata(Item):
    ad_breaks = scrapy.Field()
    chat_enabled = scrapy.Field()
    description_html = scrapy.Field()
    downloadable = scrapy.Field()
    duration = scrapy.Field()
    m3u_url = scrapy.Field()

    __tablename__ = 'video_metadatas'

    def __init__(self, *args, **kwargs):
        super(VideoMetadata, self).__init__(*args, **kwargs)

class VideoAsset(Item):
    video_id = scrapy.Field()
    legacy_url = scrapy.Field()
    key = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    fps = scrapy.Field()

    __tablename__ = 'video_assets'

    def __init__(self, *args, **kwargs):
        super(VideoAsset, self).__init__(*args, **kwargs)

class VideoCaption(Item):
    video_id = scrapy.Field()
    language = scrapy.Field()
    text = scrapy.Field()

    __tablename__ = 'video_captions'

    def __init__(self, *args, **kwargs):
        super(VideoCaption, self).__init__(*args, **kwargs)