import scrapy
from uuid import uuid4

# Scrapy Item used to define the structure of entertainment
class Object(scrapy.Item):
    id = scrapy.Field()
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
        
        self['id'] = str(uuid4())
        self['legacy_id'] = manual_assignments.get('id', object_data.get('id'))
        self['url'] = manual_assignments.get('url', object_data.get('url'))
        self['slug'] = manual_assignments.get('slug', object_data.get('slug'))
        self['how_long_to_beat'] = manual_assignments.get('how_long_to_beat', object_data.get('hl2bData'))
        self['wiki'] = manual_assignments.get('wiki', object_data.get('wiki'))
        self['wiki_slug'] = manual_assignments.get('wiki_slug', object_data.get('wikiSlug'))
        self['type'] = manual_assignments.get('type', object_data.get('type'))
        self['cover'] = manual_assignments.get('cover', object_data['primaryImage']['url'] if object_data.get('primaryImage') else None)
        self['gallery'] = manual_assignments.get('gallery', [])
        self['names'] = manual_assignments.get('names', object_data.get('names'))
        self['descriptions'] = manual_assignments.get('descriptions', object_data.get('descriptions'))
        self['franchises'] = manual_assignments.get('franchises', [])
        self['genres'] = manual_assignments.get('genres', [])
        self['features'] = manual_assignments.get('features', [])
        self['producers'] = manual_assignments.get('producers', [])
        self['publishers'] = manual_assignments.get('publishers', [])
        self['regions'] = manual_assignments.get('regions', [])
        self['reviews'] = manual_assignments.get('reviews', [])

class ObjectConnection(scrapy.Item):
    id = scrapy.Field()
    object = scrapy.Field()
    content = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(ObjectConnection, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())

class ObjectAttributeConnection(scrapy.Item):
    id = scrapy.Field()
    attribute = scrapy.Field()  # id referencing typed attribute

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self['id'] = str(uuid4())

class Region(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    name = scrapy.Field()
    region = scrapy.Field()
    age_rating = scrapy.Field()
    releases = scrapy.Field()

    def __init__(self, region_data= {}, manual_assignments={}, *args, **kwargs):
        super(Region, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())
        self['legacy_id'] = manual_assignments.get('id', region_data.get('id'))
        self['name'] = manual_assignments.get('name', region_data.get('name'))
        self['region'] = manual_assignments.get('region', region_data.get('region'))
        self['age_rating'] = manual_assignments.get('age_rating', region_data.get('ageRating'))
        self['releases'] = manual_assignments.get('releases', [])

class Release(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    date = scrapy.Field()
    estimated_date = scrapy.Field()
    time_frame_year = scrapy.Field()
    platforms = scrapy.Field()

    def __init__(self, release_data={}, manual_assignments = {}, *args, **kwargs):
        super(Release, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())
        self['legacy_id'] = manual_assignments.get('id', release_data.get('id'))
        self['date'] = manual_assignments.get('date', release_data.get('date'))
        self['estimated_date'] = manual_assignments.get('estimated_date', release_data.get('estimatedDate'))
        self['time_frame_year'] = manual_assignments.get('time_frame_year', release_data.get('timeframeYear'))
        self['platforms'] = manual_assignments.get('platforms', [])

class Rating(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    type = scrapy.Field()
    name = scrapy.Field()
    slug = scrapy.Field()
    descriptors = scrapy.Field()
    interactive_elements = scrapy.Field()

    def __init__(self, rating_data={}, manual_assignments={}, *args, **kwargs):
        super(Rating, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())
        self['legacy_id'] = manual_assignments.get('id', rating_data.get('id'))
        self['type'] = manual_assignments.get('type', rating_data.get('type'))
        self['name'] = manual_assignments.get('name', rating_data.get('name'))
        self['slug'] = manual_assignments.get('slug', rating_data.get('slug'))
        self['descriptors'] = manual_assignments.get('descriptors', [])
        self['interactive_elements'] = manual_assignments.get('interactive_elements', [])

class HowLongToBeat(scrapy.Item):
    id = scrapy.Field()
    legacy_ign_object_id = scrapy.Field()
    legacy_id = scrapy.Field()
    steam_id = scrapy.Field()
    platforms = scrapy.Field()
    list = scrapy.Field()
    time = scrapy.Field()
    review = scrapy.Field()

    def __init__(self, hltb_data = {}, manual_assignments={}, *args, **kwargs):
        super(HowLongToBeat, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())
        self['legacy_ign_object_id'] = manual_assignments.get('ign_object_id', hltb_data.get('ign_object_id'))
        self['legacy_id'] = manual_assignments.get('id', hltb_data.get('id'))
        self['steam_id'] = manual_assignments.get('steam_id', hltb_data.get('steam_id'))
        self['platforms'] = manual_assignments.get('platforms', hltb_data.get('platforms'))
        self['list'] = manual_assignments.get('list', hltb_data.get('list'))
        self['time'] = manual_assignments.get('time', hltb_data.get('time'))
        self['review'] = manual_assignments.get('review', hltb_data.get('review'))