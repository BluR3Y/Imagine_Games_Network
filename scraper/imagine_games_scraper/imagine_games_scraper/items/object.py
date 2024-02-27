import scrapy
from uuid import uuid4

class Object(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    url = scrapy.Field()
    slug = scrapy.Field()
    wiki_slug = scrapy.Field()
    how_long_to_beat_id = scrapy.Field()
    type = scrapy.Field()
    cover_id = scrapy.Field()
    gallery_id = scrapy.Field()
    names = scrapy.Field()
    descriptions = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(Object, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())

class ObjectAttributeConnection(scrapy.Item):
    id = scrapy.Field()
    object_id = scrapy.Field()
    attribute_id = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(ObjectAttributeConnection, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())

class HowLongToBeat(scrapy.Item):
    id = scrapy.Field()
    legacy_ign_object_id = scrapy.Field()
    steam_id = scrapy.Field()
    itch_id = scrapy.Field()
    platforms = scrapy.Field()
    list = scrapy.Field()
    review = scrapy.Field()
    time = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(HowLongToBeat, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())

class AgeRating(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    type = scrapy.Field()
    name = scrapy.Field()
    slug = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(AgeRating, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())

class Region(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    name = scrapy.Field()
    region = scrapy.Field()
    age_rating_id = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(Region, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())

class Release(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    date = scrapy.Field()
    estimated_date = scrapy.Field()
    time_frame_year = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(AgeRating, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())

class ReleasePlatformAttribute(scrapy.Item):
    id = scrapy.Field()
    release_id = scrapy.Field()
    attribute_id = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(ReleasePlatformAttribute, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())