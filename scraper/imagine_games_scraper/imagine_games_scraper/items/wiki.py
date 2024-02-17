import scrapy
from uuid import uuid4

class ObjectWiki(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    name = scrapy.Field()
    map_objects = scrapy.Field() #id referencing MapObject
    navigation = scrapy.Field() #id referencing WikiNavigation

    def __init__(self, wiki_data={}, manual_assignments={}, *args, **kwargs):
        super(ObjectWiki, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())
        self['legacy_id'] = manual_assignments.get('id', wiki_data.get('id'))
        self['name'] = manual_assignments.get('name', wiki_data.get('name'))
        self['map_objects'] = manual_assignments.get('map_objects', [])
        self['navigation'] = manual_assignments.get('navigation', [])

class WikiNavigation(scrapy.Item):
    id = scrapy.Field()
    label = scrapy.Field()
    url = scrapy.Field()

    def __init__(self, navigation_data={}, manual_assignments={}, *args, **kwargs):
        super(WikiNavigation, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())
        self['label'] = manual_assignments.get('label', navigation_data.get('label'))
        self['url'] = manual_assignments.get('url', navigation_data.get('url'))

class MapObject(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    object_name = scrapy.Field()
    maps = scrapy.Field()

    def __init__(self, object_data={}, manual_assignments={}, *args, **kwargs):
        super(MapObject, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())
        self['legacy_id'] = manual_assignments.get('id', object_data.get('id'))
        self['object_name'] = manual_assignments.get('object_name', object_data.get('objectName'))
        self['maps'] = manual_assignments.get('maps', object_data.get('maps'))

class Map(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    object_name = scrapy.Field()
    object_slug = scrapy.Field()
    map_name = scrapy.Field()
    map_slug = scrapy.Field()
    cover = scrapy.Field()
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

    def __init__(self, map_data={}, manual_assignments={}, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())
        self['legacy_id'] = manual_assignments.get('id', map_data.get('id'))
        self['object_name'] = manual_assignments.get('object_name', map_data.get('objectName'))
        self['object_slug'] = manual_assignments.get('object_slug', map_data.get('objectSlug'))
        self['map_name'] = manual_assignments.get('map_name', map_data.get('mapName'))
        self['map_slug'] = manual_assignments.get('map_slug', map_data.get('mapSlug'))
        self['cover'] = manual_assignments.get('cover', map_data.get('thumbnailUrl'))
        self['width'] = manual_assignments.get('width', map_data.get('width'))
        self['height'] = manual_assignments.get('height', map_data.get('height'))
        self['map_type'] = manual_assignments.get('map_type', map_data.get('mapType'))
        self['initial_zoom'] = manual_assignments.get('initial_zoom', map_data.get('initialZoom'))
        self['min_zoom'] = manual_assignments.get('min_zoom', map_data.get('minZoom'))
        self['max_zoom'] = manual_assignments.get('max_zoom', map_data.get('maxZoom'))
        self['initial_latitude'] = manual_assignments.get('initial_latitude', map_data.get('initialLat'))
        self['initial_longitude'] = manual_assignments.get('initial_longitude', map_data.get('initialLng'))
        self['marker_count'] = manual_assignments.get('marker_count', map_data.get('markerCount'))
        self['map_genie_game_id'] = manual_assignments.get('map_genie_game_id', map_data.get('mapGenieGameId'))
        self['tile_sets'] = manual_assignments.get('tile_sets', map_data.get('tilesets'))
        self['background_color'] = manual_assignments.get('background_color', map_data.get('backgroundColor'))