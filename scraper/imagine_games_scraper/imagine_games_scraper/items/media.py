import scrapy
from uuid import uuid4

class Image(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    legacy_url = scrapy.Field()
    url = scrapy.Field()
    link = scrapy.Field()
    caption = scrapy.Field()
    embargo_date = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(Image, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())

class ImageConnection(scrapy.Item):
    id = scrapy.Field()
    image_id = scrapy.Field()
    gallery_id = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(ImageConnection, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())

class Gallery(scrapy.Item):
    id = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(Gallery, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())

class Slideshow(scrapy.Item):
    id = scrapy.Field()
    content_id = scrapy.Field()
    gallery_id = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(Slideshow, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())

