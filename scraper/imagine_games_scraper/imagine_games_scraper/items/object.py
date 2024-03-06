import scrapy
from imagine_games_scraper.items.base_item import Item

class Object(Item):
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

    __tablename__ = 'objects'

    def __init__(self, *args, **kwargs):
        super(Object, self).__init__(*args, **kwargs)


class ObjectAttributeConnection(Item):
    id = scrapy.Field()
    object_id = scrapy.Field()
    attribute_id = scrapy.Field()

    __tablename__ = 'object_attribute_connections'

    def __init__(self, *args, **kwargs):
        super(ObjectAttributeConnection, self).__init__(*args, **kwargs)     


class HowLongToBeat(Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    legacy_ign_object_id = scrapy.Field()
    steam_id = scrapy.Field()
    itch_id = scrapy.Field()
    platforms = scrapy.Field()
    list = scrapy.Field()
    review = scrapy.Field()
    time = scrapy.Field()

    __tablename__ = 'how_long_to_beat'

    def __init__(self, *args, **kwargs):
        super(HowLongToBeat, self).__init__(*args, **kwargs)


class AgeRating(Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    type = scrapy.Field()
    name = scrapy.Field()
    slug = scrapy.Field()

    __tablename__ = 'age_ratings'

    def __init__(self, *args, **kwargs):
        super(AgeRating, self).__init__(*args, **kwargs)

        



class Region(Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    name = scrapy.Field()
    region = scrapy.Field()
    age_rating_id = scrapy.Field()
    object_id = scrapy.Field()

    __tablename__ = 'regions'

    def __init__(self, *args, **kwargs):
        super(Region, self).__init__(*args, **kwargs)

        

class AgeRatingDescriptor(Item):
    id = scrapy.Field()
    region_id = scrapy.Field()
    attribute_id = scrapy.Field()

    __tablename__ = 'age_rating_descriptors'

    def __init__(self, *args, **kwargs):
        super(AgeRatingDescriptor, self).__init__(*args, **kwargs)

        

class AgeRatingInteractiveElement(Item):
    id = scrapy.Field()
    region_id = scrapy.Field()
    attribute_id = scrapy.Field()

    __tablename__ = 'age_rating_interactive_elements'

    def __init__(self, *args, **kwargs):
        super(AgeRatingInteractiveElement, self).__init__(*args, **kwargs)

        

class Release(Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    date = scrapy.Field()
    estimated_date = scrapy.Field()
    time_frame_year = scrapy.Field()

    __tablename__ = 'releases'

    def __init__(self, *args, **kwargs):
        super(Release, self).__init__(*args, **kwargs)

        

class ReleasePlatformAttribute(Item):
    id = scrapy.Field()
    release_id = scrapy.Field()
    attribute_id = scrapy.Field()

    __tablename__ = 'release_platform_attributes'

    def __init__(self, *args, **kwargs):
        super(ReleasePlatformAttribute, self).__init__(*args, **kwargs)

        