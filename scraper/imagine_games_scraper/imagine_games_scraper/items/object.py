import scrapy

# Scrapy Item used to define the structure of entertainment
class Object(scrapy.Item):
    legacy_id = scrapy.Field()
    url = scrapy.Field()
    slug = scrapy.Field()
    how_long_to_beat = scrapy.Field()
    wiki = scrapy.Field()
    wiki_slug = scrapy.Field()
    type = scrapy.Field()
    cover = scrapy.Field()
    gallery = scrapy.Field()
    names = scrapy.Field()
    descriptions = scrapy.Field()
    franchises = scrapy.Field()
    genres = scrapy.Field()
    features = scrapy.Field()
    producers = scrapy.Field()
    publishers = scrapy.Field()
    regions = scrapy.Field()
    reviews = scrapy.Field()

    def __init__(self, object_data = {}, manual_assignments = {}, *args, **kwargs):
        super(Object, self).__init__(*args, **kwargs)

        self['legacy_id'] = manual_assignments.get('id', object_data.get('id'))
        self['url'] = manual_assignments.get('url', object_data.get('url'))
        self['slug'] = manual_assignments.get('slug', object_data.get('slug'))
        self['how_long_to_beat'] = manual_assignments.get('how_long_to_beat', object_data.get('hl2bData'))
        self['wiki'] = manual_assignments.get('wiki', object_data.get('wiki'))
        self['wiki_slug'] = manual_assignments.get('wiki_slug', object_data.get('wikiSlug'))
        self['type'] = manual_assignments.get('type', object_data.get('type'))
        self['cover'] = manual_assignments.get('cover', object_data['primaryImage']['url'] if object_data.get('primaryImage') else None)
        self['gallery'] = manual_assignments.get('gallery', object_data.get('gallery'))
        self['names'] = manual_assignments.get('names', object_data.get('names'))
        self['descriptions'] = manual_assignments.get('descriptions', object_data.get('descriptions'))
        self['franchises'] = manual_assignments.get('franchises', object_data.get('franchises'))
        self['genres'] = manual_assignments.get('genres', object_data.get('genres'))
        self['features'] = manual_assignments.get('features', object_data.get('features'))
        self['producers'] = manual_assignments.get('producers', object_data.get('producers'))
        self['publishers'] = manual_assignments.get('publishers', object_data.get('publishers'))
        self['regions'] = manual_assignments.get('regions', object_data.get('regions'))
        self['reviews'] = manual_assignments.get('reviews', object_data.get('reviews'))

class Region(scrapy.Item):
    legacy_id = scrapy.Field()
    name = scrapy.Field()
    region = scrapy.Field()
    age_rating = scrapy.Field()
    releases = scrapy.Field()

    def __init__(self, region_data= {}, manual_assignments={}, *args, **kwargs):
        super(Region, self).__init__(*args, **kwargs)

        self['legacy_id'] = manual_assignments.get('id', region_data.get('id'))
        self['name'] = manual_assignments.get('name', region_data.get('name'))
        self['region'] = manual_assignments.get('region', region_data.get('region'))
        self['age_rating'] = manual_assignments.get('age_rating', region_data.get('ageRating'))
        self['releases'] = manual_assignments.get('releases', region_data.get('releases'))

class Release(scrapy.Item):
    legacy_id = scrapy.Field()
    date = scrapy.Field()
    estimated_date = scrapy.Field()
    time_frame_year = scrapy.Field()
    platforms = scrapy.Field()

    def __init__(self, release_data={}, manual_assignments = {}, *args, **kwargs):
        super(Release, self).__init__(*args, **kwargs)

        self['legacy_id'] = manual_assignments.get('id', release_data.get('id'))
        self['date'] = manual_assignments.get('date', release_data.get('date'))
        self['estimated_date'] = manual_assignments.get('estimated_date', release_data.get('estimatedDate'))
        self['time_frame_year'] = manual_assignments.get('time_frame_year', release_data.get('timeframeYear'))
        self['platforms'] = manual_assignments.get('platforms', release_data.get('platformAttributes'))

class Rating(scrapy.Item):
    legacy_id = scrapy.Field()
    type = scrapy.Field()
    name = scrapy.Field()
    slug = scrapy.Field()
    descriptors = scrapy.Field()
    interactive_elements = scrapy.Field()

    def __init__(self, rating_data={}, manual_assignments={}, *args, **kwargs):
        super(Rating, self).__init__(*args, **kwargs)

        self['legacy_id'] = manual_assignments.get('id', rating_data.get('id'))
        self['type'] = manual_assignments.get('type', rating_data.get('type'))
        self['name'] = manual_assignments.get('name', rating_data.get('name'))
        self['slug'] = manual_assignments.get('slug', rating_data.get('slug'))
        self['descriptors'] = manual_assignments.get('descriptors', rating_data.get('descriptors'))
        self['interactive_elements'] = manual_assignments.get('interactive_elements', rating_data.get('interactive_elements'))

class Attribute(scrapy.Item):
    type = scrapy.Field()
    name = scrapy.Field()
    short_name = scrapy.Field()
    slug = scrapy.Field()

    def __init__(self, attribute_data={}, manual_assignments={}, *args, **kwargs):
        super(Attribute, self).__init__(*args, **kwargs)

        self['type'] = manual_assignments.get('type', attribute_data.get('type'))
        self['name'] = manual_assignments.get('name', attribute_data.get('name'))
        self['short_name'] = manual_assignments.get('short_name', attribute_data.get('shortName'))
        self['slug'] = manual_assignments.get('slug', attribute_data.get('slug'))

class HowLongToBeat(scrapy.Item):
    legacy_ign_object_id = scrapy.Field()
    id = scrapy.Field()
    steam_id = scrapy.Field()
    platforms = scrapy.Field()
    list = scrapy.Field()
    time = scrapy.Field()
    review = scrapy.Field()

    def __init__(self, hltb_data = {}, manual_assignments={}, *args, **kwargs):
        super(HowLongToBeat, self).__init__(*args, **kwargs)

        self['legacy_ign_object_id'] = manual_assignments.get('ign_object_id', hltb_data.get('ign_object_id'))
        self['id'] = manual_assignments.get('id', hltb_data.get('id'))
        self['steam_id'] = manual_assignments.get('steam_id', hltb_data.get('steam_id'))
        self['platforms'] = manual_assignments.get('platforms', hltb_data.get('platforms'))
        self['list'] = manual_assignments.get('list', hltb_data.get('list'))
        self['time'] = manual_assignments.get('time', hltb_data.get('time'))
        self['review'] = manual_assignments.get('review', hltb_data.get('review'))

class ObjectWiki(scrapy.Item):
    legacy_id = scrapy.Field()
    name = scrapy.Field()
    map_objects = scrapy.Field()
    navigation = scrapy.Field()

    def __init__(self, wiki_data={}, manual_assignments={}, *args, **kwargs):
        super(ObjectWiki, self).__init__(*args, **kwargs)

        self['legacy_id'] = manual_assignments.get('id', wiki_data.get('id'))
        self['name'] = manual_assignments.get('name', wiki_data.get('name'))
        self['map_objects'] = manual_assignments.get('map_objects', wiki_data.get('mapObjects'))
        self['navigation'] = manual_assignments.get('navigation', wiki_data.get('navigation'))

class WikiNavigation(scrapy.Item):
    label = scrapy.Field()
    url = scrapy.Field()

    def __init__(self, navigation_data={}, manual_assignments={}, *args, **kwargs):
        super(WikiNavigation, self).__init__(*args, **kwargs)

        self['label'] = manual_assignments.get('label', navigation_data.get('label'))
        self['url'] = manual_assignments.get('url', navigation_data.get('url'))

class MapObject(scrapy.Item):
    legacy_id = scrapy.Field()
    object_name = scrapy.Field()
    maps = scrapy.Field()

    def __init__(self, object_data={}, manual_assignments={}, *args, **kwargs):
        super(MapObject, self).__init__(*args, **kwargs)

        self['legacy_id'] = manual_assignments.get('id', object_data.get('id'))
        self['object_name'] = manual_assignments.get('object_name', object_data.get('objectName'))
        self['maps'] = manual_assignments.get('maps', object_data.get('maps'))

class Map(scrapy.Item):
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