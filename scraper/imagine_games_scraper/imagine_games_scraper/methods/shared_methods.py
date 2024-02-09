import scrapy
import json
import re
from imagine_games_scraper.items.user import User, UserReview, UserReviewTag, Contributor
from imagine_games_scraper.items.object import Object, Region, Rating, HowLongToBeat, ObjectWiki, Release, MapObject, Map, WikiNavigation
from imagine_games_scraper.items.misc import Image
from imagine_games_scraper.items.content import Attribute

@classmethod
def parse_contributor_page(self, response, contributor_item):
    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    page_data = page_json_data['props']['pageProps']['page']
    author_data = page_data['author']
    # Missing: Contributor related Articles

    contributor_item['legacy_id'] = author_data.get('id')
    contributor_item['legacy_author_id'] = author_data.get('authorId')
    contributor_item['cover'] = author_data.get('backgroundImageUrl')
    contributor_item['position'] = author_data.get('position')
    contributor_item['bio'] = author_data.get('bio')
    contributor_item['location'] = author_data.get('location')
    contributor_item['socials'] = author_data.get('socials')

    yield contributor_item

@classmethod
def parse_object_page(self, response, object_item):
    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    page_data = page_json_data['props']['pageProps']['page']
    apollo_state = page_json_data['props']['apolloState']
    object_data = apollo_state[f'Object:{page_data.get('id')}']

    object_item['names'] = {
        'primary': object_data['metadata']['names'].get('name'),
        'alt': object_data['metadata']['names'].get('alt'),
        'short': object_data['metadata']['names'].get('short')
    }
    object_item['descriptions'] = {
        'long': object_data['metadata']['descriptions'].get('long'),
        'short': object_data['metadata']['descriptions'].get('short')
    }

    hl2b_data = object_data.get('hl2bData')
    if hl2b_data:
        hl2b_item = HowLongToBeat(hl2b_data)
        object_item['how_long_to_beat'] = hl2b_item.get('id')
        yield hl2b_item

    for franchise in object_data.get('franchises'):
        franchise_item = Attribute(franchise)
        object_item['franchises'].append(franchise_item.get('id'))
        yield franchise_item

    for genre in object_data.get('genres'):
        genre_item = Attribute(genre)
        object_item['genres'].append(genre_item.get('id'))
        yield genre_item

    for feature in object_data.get('features'):
        feature_item = Attribute(feature)
        object_item['features'].append(feature_item.get('id'))
        yield feature_item

    for producer in object_data.get('producers'):
        producer_item = Attribute(producer)
        object_item['producers'].append(producer_item.get('id'))
        yield producer_item

    for publisher in object_data.get('publishers'):
        publisher_item = Attribute(publisher)
        object_item['publishers'].append(publisher_item.get('id'))
        yield publisher_item

    for region in [apollo_state[region_ref['__ref']] for region_ref in filter((lambda x : x.get('__ref') is not None), object_data.get('objectRegions'))]:
        region_item = Region(region)

        for release in [apollo_state[release_ref['__ref']] for release_ref in region.get('releases')]:
            release_item = Release(release)

            for platform in [apollo_state[platform_ref['__ref']] for platform_ref in release.get('platformAttributes')]:
                platform_item = Attribute(platform)
                release_item['platforms'].append(platform_item.get('id'))
                yield platform_item
            
            region_item['releases'].append(release_item.get('id'))
            yield release_item

        age_rating_data = region.get('agerating')
        if age_rating_data:
            age_rating_item = Rating(age_rating_data)

            for descriptor in region.get('ageRatingDescriptors'):
                descriptor_item = Attribute(descriptor)
                age_rating_item['descriptors'].append(descriptor_item.get('id'))
                yield descriptor_item

            for element in region.get('interactiveElements'):
                element_item = Attribute(element)
                age_rating_item['interactive_elements'].append(element_item.get('id'))
                yield element_item

            region_item['age_rating'] = age_rating_item.get('id')
            yield age_rating_item

        object_item['regions'].append(region_item.get('id'))
        yield region_item

    user_review_key = next((key for key in apollo_state['ROOT_QUERY'] if 'userReviewSearch' in key), None)
    if user_review_key:
        for user_review in [apollo_state[review_ref['__ref']] for review_ref in apollo_state['ROOT_QUERY'][user_review_key]['userReviews']]:
            user_data = apollo_state[user_review['user']['__ref']]
            user_item = User(user_data)
            user_review_item = UserReview(user_review, {
                'user_id': user_item.get('id'),
                'object_id': object_item.get('id')
            })
            yield user_item

            for tag in [apollo_state[tag_ref['__ref']] for tag_ref in user_review.get(next((key for key in user_review if 'userReviewObjectFeedback' in key), None))]:
                tag_item = UserReviewTag(tag)
                user_review_item['tags'].append(tag_item.get('id'))
                yield tag_item

            platform_data = user_review.get('platform')
            if platform_data:
                platform_item = Attribute(platform_data)
                user_review_item['platform'] = platform_item.get('id')
                yield platform_item

            object_item['reviews'].append(user_review_item.get('id'))
            yield user_review_item

    legacy_wiki_key = next((key for key in apollo_state['ROOT_QUERY'] if 'wiki' in key), None)
    if legacy_wiki_key:
        wiki_data = apollo_state[apollo_state['ROOT_QUERY'][legacy_wiki_key]['__ref']]
        wiki_item = ObjectWiki(wiki_data)

        # Map image dimensions: 256 x 256
        # Smallest map magnification value: 254
        # Map zoom to coordinate increment: x2
        map_objects = {}
        for map in wiki_data.get('maps'):
            object_key = 'MapObject:' + map.get('objectSlug')
            if object_key not in map_objects:
                map_objects[object_key] = MapObject(apollo_state[object_key], { 'maps': [] })

            map_item = Map({ **map, **apollo_state[f'Map:{map.get('objectSlug')}:{map.get('mapSlug')}'] })
            map_objects[object_key]['maps'].append(map_item.get('id'))
            yield map_item

        for object_key in map_objects:
            map_object_item = map_objects[object_key]
            wiki_item['map_objects'].append(map_object_item.get('id'))
            yield map_object_item

        for nav in wiki_data.get('navigation'):
            nav_item = WikiNavigation(nav)
            wiki_item['navigation'].append(nav_item.get('id'))
            yield nav_item

        object_item['wiki'] = wiki_item.get('id')
        yield wiki_item

    gallery_regex = re.compile(r"imageGallery:{.*}")
    object_gallery_key = next((key for key in object_data if gallery_regex.search(key)), None)
    if object_gallery_key:
        for image in [apollo_state[img_ref['__ref']] for img_ref in object_data[object_gallery_key]['images']]:
            image_item = Image(image)
            object_item['gallery'].append(image_item.get('id'))
            yield image_item

    yield object_item