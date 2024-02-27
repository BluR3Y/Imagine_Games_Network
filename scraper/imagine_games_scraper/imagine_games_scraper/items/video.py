import scrapy
from uuid import uuid4

class Video(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    content_id = scrapy.Field()
    metadata_id = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(Video, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())

class VideoMetadata(scrapy.Item):
    id = scrapy.Field()
    ad_breaks = scrapy.Field()
    chat_enabled = scrapy.Field()
    description_html = scrapy.Field()
    downloadable = scrapy.Field()
    duration = scrapy.Field()
    m3u_url = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(VideoMetadata, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())

class VideoAsset(scrapy.Item):
    id = scrapy.Field()
    video_id = scrapy.Field()
    url = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    fps = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(VideoAsset, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())

class VideoCaption(scrapy.Item):
    id = scrapy.Field()
    video_id = scrapy.Field()
    language = scrapy.Field()
    text = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(VideoCaption, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())