import scrapy
import json
import re
from imagine_games_scraper.items.user import User, UserReview, UserReviewTag, Reporter
from imagine_games_scraper.items.object import Object, Region, Rating, Attribute, HowLongToBeat, ObjectWiki, Release, MapObject, Map, WikiNavigation
from imagine_games_scraper.items.misc import Image

@classmethod
def parse_contributor_page(self, response):
    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    page_data = page_json_data['props']['pageProps']['page']
    author_data = page_data['author']
    # Missing: Reporter related Articles

    yield Reporter(author_data, { 'url': page_data.get('canonical') })

@classmethod
def parse_object_page(self, response):
    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    page_data = page_json_data['props']['pageProps']['page']
    apollo_state = page_json_data['props']['apolloState']
    object_data = apollo_state[f'Object:{page_data.get('id')}']

    parsed_object = Object(object_data, {
        'names': {
            'primary': object_data['metadata']['names'].get('name'),
            'alt': object_data['metadata']['names'].get('alt'),
            'short': object_data['metadata']['names'].get('short')
        },
        'descriptions': {
            'long': object_data['metadata']['descriptions'].get('long'),
            'short': object_data['metadata']['descriptions'].get('short')
        },
        'how_long_to_beat': (HowLongToBeat(object_data.get('hl2bData')) if object_data.get('hl2bData') is not None else None),
        'franchises': [Attribute(franchise, { 'type': 'franchise' }) for franchise in object_data.get('franchises')],
        'genres': [Attribute(genre, { 'type': 'genre' }) for genre in object_data.get('genres')],
        'features': [Attribute(feature, { 'type': 'feature' }) for feature in object_data.get('features')],
        'producers': [Attribute(producer, { 'type': 'producer' }) for producer in object_data.get('producers')],
        'publishers': [Attribute(publisher, { 'type': 'publisher' }) for publisher in object_data.get('publishers')],
        'regions': [Region(region,{
            'releases': [Release(release, {
                'platforms': [Attribute(platform, { 'type': 'platform' }) for platform in [apollo_state[platform_ref['__ref']] for platform_ref in release.get('platformAttributes')]]
            }) for release in [apollo_state[release_ref['__ref']] for release_ref in region.get('releases')]],
            'age_rating': (Rating(apollo_state[region['ageRating']['__ref']], {
                'descriptors': [Attribute(descriptor, { 'type': 'descriptor' }) for descriptor in region.get('ageRatingDescriptors')],
                'interactive_elements': [Attribute(element, { 'type': 'element' }) for element in region.get('interactiveElements')]
            }) if region.get('ageRating') is not None else None)
        }) for region in [apollo_state[region_ref['__ref']] for region_ref in filter((lambda x : x.get('__ref') is not None), object_data.get('objectRegions'))]],
        'reviews': []
    })

    user_review_key = next((key for key in apollo_state['ROOT_QUERY'] if 'userReviewSearch' in key), None)
    if user_review_key is not None:
        for user_review in [apollo_state[review_ref['__ref']] for review_ref in apollo_state['ROOT_QUERY'][user_review_key]['userReviews']]:
            parsed_object['reviews'].append({
                'user_info': User(apollo_state[f'User:{user_review.get('userId')}']),
                'user_review': UserReview(user_review, {
                    'tags': [UserReviewTag(tag) for tag in [apollo_state[tag_ref['__ref']] for tag_ref in user_review.get(next((key for key in user_review if 'userReviewObjectFeedback' in key), None))]],
                    'platform': (Attribute(user_review.get('platform', { 'type': 'platform' })) if user_review.get('platform') is not None else None)
                })
            })

    legacy_wiki_key = next((key for key in apollo_state['ROOT_QUERY'] if 'wiki' in key), None)
    if legacy_wiki_key is not None:
        wiki_data = apollo_state[apollo_state['ROOT_QUERY'][legacy_wiki_key]['__ref']]
        map_objects = {}
        for map in wiki_data.get('maps'):
            object_key = 'MapObject:' + map.get('objectSlug')
            if object_key not in map_objects:
                map_objects[object_key] = MapObject(apollo_state[object_key], { 'maps': [] })
            map_objects[object_key]['maps'].append(Map({ **map, **apollo_state[f'Map:{map.get('objectSlug')}:{map.get('mapSlug')}'] }))

        # Map image dimensions: 256 x 256
        # Smallest map magnification value: 254
        # Map zoom to coordinate increment: x2
        parsed_object['wiki'] = ObjectWiki(wiki_data, {
            'map_objects': [map_objects[object_key] for object_key in map_objects],
            'navigation': [WikiNavigation(nav) for nav in wiki_data.get('navigation')]
        })
    
    gallery_regex = re.compile(r"imageGallery:{.*}")
    object_gallery_key = next((key for key in object_data if gallery_regex.search(key)))
    if object_gallery_key is not None:
        parsed_object['gallery'] = [Image(image) for image in [apollo_state[img_ref['__ref']] for img_ref in object_data[object_gallery_key]['images']]]

    yield parsed_object


@classmethod
def parse_object_region(self):
    pass


        # recommendation_regex = re.compile(r"topPages\({.*}\)")
        # recommendation_key = next((key for key in apollo_state['ROOT_QUERY'] if recommendation_regex.search(key)))