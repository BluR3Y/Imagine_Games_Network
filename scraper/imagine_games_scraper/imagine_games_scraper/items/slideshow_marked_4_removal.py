import scrapy
from uuid import uuid4

class Slideshow(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    content = scrapy.Field()
    album = scrapy.Field()

    def __init__(self, slideshow_data = {}, manual_assignments = {}, *args, **kwargs):
        super(Slideshow, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())
        self['legacy_id'] = manual_assignments.get('legacy_id', slideshow_data.get('id'))
        self['content'] = manual_assignments.get('content', slideshow_data.get('content'))
        self['album'] = manual_assignments.get('album')