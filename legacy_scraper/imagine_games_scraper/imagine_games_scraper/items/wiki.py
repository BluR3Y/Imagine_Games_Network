import scrapy
from imagine_games_scraper.items.base_item import Item

class WikiObject(Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    name = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(WikiObject, self).__init__(*args, **kwargs)

class WikiNavigation(Item):
    id = scrapy.Field()
    wiki_object_id = scrapy.Field()
    label = scrapy.Field()
    url = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(WikiNavigation, self).__init__(*args, **kwargs)


class MapObject(Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    wiki_object_id = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(MapObject, self).__init__(*args, **kwargs)

class Map(Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    map_object_id = scrapy.Field()
    name = scrapy.Field()
    slug = scrapy.Field()
    cover_id = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    map_type = scrapy.Field()
    initial_zoom = scrapy.Field()
    min_zoom = scrapy.Field()
    max_zoom = scrapy.Field()
    initial_latitude = scrapy.Field()
    initial_longitude = scrapy.Field()
    marker_count = scrapy.Field()
    map_genie_game_id = scrapy.Field()
    tile_sets = scrapy.Field()
    background_color = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)