import scrapy
from uuid import uuid4

# Scrapy Item used to define the structure of video content
# AKA ModernVideo
class Video(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    content = scrapy.Field()    # id referencing ModernContent
    metadata = scrapy.Field()   # id referencing VideoMetadata
    assets = scrapy.Field()     # id referncing VideoAsset

    def __init__(self, video_data = {}, manual_assignments = {}, *args, **kwargs):
        super(Video, self).__init__(*args, **kwargs)

        self['id'] = uuid4()
        self['legacy_id'] = manual_assignments.get('id', video_data.get('id'))
        self['content'] = manual_assignments.get('content')
        self['metadata'] = manual_assignments.get('metadata', video_data.get('metadata'))
        self['assets'] = manual_assignments.get('assets', video_data.get('reviassetsew'))

class VideoMetadata(scrapy.Item):
    id = scrapy.Field()
    ad_breaks = scrapy.Field()
    captions = scrapy.Field()   # id referencing VideoCaption
    chat_enabled = scrapy.Field()
    description_html = scrapy.Field()
    downloadable = scrapy.Field()
    duration = scrapy.Field()
    m3u_url = scrapy.Field()

    def __init__(self, meta_data = {}, manual_assignments = {}, *args, **kwargs):
        super(VideoMetadata, self).__init__(*args, **kwargs)

        self['id'] = uuid4()
        self['ad_breaks'] = manual_assignments.get('ad_breaks', meta_data.get('adBreaks'))
        self['captions'] = manual_assignments.get('captions', meta_data.get('captions'))
        self['chat_enabled'] = manual_assignments.get('chat_enabled', meta_data.get('chatEnabled'))
        self['description_html'] = manual_assignments.get('description_html', meta_data.get('descriptionHtml'))
        self['downloadable'] = manual_assignments.get('downloadable', meta_data.get('downloadable'))
        self['duration'] = manual_assignments.get('duration', meta_data.get('duration'))
        self['m3u_url'] = manual_assignments.get('m3u_url', meta_data.get('m3uUrl'))

class VideoAsset(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    fps = scrapy.Field()

    def __init__(self, meta_data = {}, manual_assignments = {}, *args, **kwargs):
        super(VideoAsset, self).__init__(*args, **kwargs)

        self['id'] = uuid4()
        self['url'] = manual_assignments.get('url', meta_data.get('url'))
        self['width'] = manual_assignments.get('width', meta_data.get('width'))
        self['height'] = manual_assignments.get('height', meta_data.get('height'))
        self['fps'] = manual_assignments.get('fps', meta_data.get('fps'))