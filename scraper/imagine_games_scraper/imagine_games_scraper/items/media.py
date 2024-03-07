import scrapy
from imagine_games_scraper.items.base_item import Item

class Image(Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    legacy_url = scrapy.Field()
    url = scrapy.Field()
    link = scrapy.Field()
    caption = scrapy.Field()
    embargo_date = scrapy.Field()

    __tablename__ = 'images'

    def __init__(self, *args, **kwargs):
        super(Image, self).__init__(*args, **kwargs)

class ImageConnection(Item):
    id = scrapy.Field()
    image_id = scrapy.Field()
    gallery_id = scrapy.Field()

    __tablename__ = 'image_connections'

    def __init__(self, *args, **kwargs):
        super(ImageConnection, self).__init__(*args, **kwargs)

class Gallery(Item):
    id = scrapy.Field()

    __tablename__ = 'galleries'

    def __init__(self, *args, **kwargs):
        super(Gallery, self).__init__(*args, **kwargs)

class Slideshow(Item):
    id = scrapy.Field()
    content_id = scrapy.Field()
    gallery_id = scrapy.Field()

    __tablename__ = 'slideshows'

    def __init__(self, *args, **kwargs):
        super(Slideshow, self).__init__(*args, **kwargs)

        


