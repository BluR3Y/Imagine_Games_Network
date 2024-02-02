import json
import scrapy
from imagine_games_scraper.items import Reporter, Entertainment, Attribute, Region, Rating, ReporterReview, UserReview, UserReviewTag, User

@classmethod
def parse_contributor_page(self, response):
    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    page_data = page_json_data['props']['pageProps']['page']
    author_data = page_data['author']
    reporter_item = Reporter({
        'legacy_id': author_data['id'],
        'legacy_author_id': author_data['authorId'],
        'uri': page_data['canonical'],
        'avatar': author_data['backgroundImageUrl'],
        'cover': author_data['thumbnailUrl'],
        'name': author_data['name'],
        'nickname': author_data['nickname'],
        'position': author_data['position'],
        'bio': author_data['bio'],
        'location': author_data['location'],
        'socials': author_data['socials']
    })
    # Data also includes Content created by reporter
    yield reporter_item

@classmethod
def parse_object_page(self, response):
    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)
    page_data = page_json_data['props']['pageProps']['page']
    object_data = page_json_data['props']['apolloState'][f'Object:{page_data['id']}']
    root_query = page_json_data['props']['apolloState']['ROOT_QUERY']

    # with open('ign_scraping_game_data.json', 'w') as f:
    #     json.dump(page_json_data, f)

    parsed_object = Entertainment({
        'legacy_id': page_data.get('id'),
        'uri': page_data.get('url'),
        'slug': page_data.get('slug'),
        'type': page_data.get('type'),
        'wiki_slug': page_data.get('wikiSlug'),
        'cover': page_data['primaryImage'].get('url'),
        'names': {
            'primary': page_data['metadata']['names'].get('name'),
            'alt': page_data['metadata']['names'].get('alt'),
            'short': page_data['metadata']['names'].get('short')
        },
        'descriptions': {
            'long': page_data['metadata']['descriptions'].get('long'),
            'short': page_data['metadata']['descriptions'].get('short')
        },
        'franchises': [Attribute({
            'type': 'franchise',
            'name': franchise.get('name'),
            'slug': franchise.get('slug')
        }) for franchise in page_data.get('franchises')],
        'genres': [Attribute({
            'type': 'genre',
            'name': genre.get('name'),
            'slug': genre.get('slug')
        }) for genre in page_data.get('genres')],
        'features': [Attribute({
            'type': 'feature',
            'name': feature.get('name'),
            'slug': feature.get('slug')
        }) for feature in page_data.get('features')],
        'producers': [Attribute({
            'type': 'producer',
            'name': producer.get('name'),
            'slug': producer.get('slug')
        }) for producer in page_data.get('producers')],
        'publishers': [Attribute({
            'type': 'publisher',
            'name': publisher.get('name'),
            'slug': publisher.get('slug')
        }) for publisher in page_data.get('publishers')],
        'regions': [self.parse_object_region(page_json_data, region) for region in page_data.get('objectRegions')],
        'reviews': dict({
            'primary_review': (ReporterReview({
                'legacy_id': page_data['primaryReview'].get('id'),
                'editors_choice': page_data['primaryReview'].get('editorsChoice'),
                'score': page_data['primaryReview'].get('score'),
                'score_text': page_data['primaryReview'].get('scoreText'),
                'score_summary': page_data['primaryReview'].get('scoreSummary'),
                'review_date': page_data['primaryReview'].get('reviewedOn')
            }) if page_data.get('primaryReview', None) is not None else None),
            'user_reviews': []
        })
    })

    gallery_key = next((key for key in object_data if 'imageGallery' in key), None)
    if gallery_key is not None:
        parsed_object['gallery'] = [{
            'legacy_id': image.get('id'),
            'caption': image.get('caption'),
            'url': image.get('url')
        } for image in [page_json_data['props']['apolloState'][image_ref['__ref']] for image_ref in object_data[gallery_key]['images']]]
    else:
        parsed_object['gallery'] = []

    wiki_key = next((key for key in root_query if 'wiki' in key), None)
    if wiki_key is not None:
        wiki_ref = root_query[wiki_key]['__ref']
        wiki_data = page_json_data['props']['apolloState'][wiki_ref]
        parsed_object['wiki'] = dict({
            'legacy_id': wiki_data.get('id'),
            'name': wiki_data.get('name'),
            # Map image dimensions: 256 x 256
            # Smallest map magnification value: 254
            # Map zoom to coordinate increment: x2
            'maps': [{
                'map_name': map.get('mapName'),
                'map_slug': map.get('mapSlug'),
                'width': map.get('width'),
                'height': map.get('height'),
                'map_type': map.get('mapType'),
                'initial_zoom': map.get('initialZoom'),
                'min_zoom': map.get('minZoom'),
                'max_zoom': map.get('maxZoom'),
                'initial_latitude': map.get('initialLat'),
                'initial_longitude': map.get('initialLng'),
                'tile_sets': map.get('tilesets'),
                'background_color': map.get('backgroundColor')
            } for map in wiki_data['maps']],
            'navigation': [{
                'label': nav.get('label'),
                'url': nav.get('url')
            } for nav in wiki_data['navigation']]
        })
    else:
        parsed_object['wiki'] = None

    user_review_key = next((key for key in root_query if 'userReviewSearch' in key), None)
    for review_ref in [review['__ref'] for review in (root_query[user_review_key]['userReviews'] if user_review_key is not None else [])]:
        review_data = page_json_data['props']['apolloState'][review_ref]
        parsed_review = UserReview({
            'legacy_id': review_data.get('id'),
            'legacy_user_id': review_data.get('userId'),
            'legacy_object_id': review_data.get('objectId'),
            'is_liked': review_data.get('liked'),
            'score': review_data.get('score'),
            'text': review_data.get('text'),
            'is_spoiler': review_data.get('isSpoiler'),
            'publish_date': review_data.get('createdAt'),
            'modify_date': review_data.get('updatedAt'),
            'tags': [UserReviewTag({
                'name': tag.get('name'),
                'is_positive': tag.get('isPositive')
            }) for tag in [page_json_data['props']['apolloState'][tag_ref['__ref']] for tag_ref in review_data.get(next((key for key in review_data if 'userReviewObjectFeedback' in key), None))]]  
        })

        platform_ref = review_data.get('platform')
        if platform_ref is not None:
            platform_data = page_json_data['props']['apolloState'][platform_ref['__ref']]
            parsed_review['platform'] = Attribute({
                'type': 'platform',
                'name': platform_data.get('name'),
                'slug': platform_data.get('slug')
            })
        else:
            parsed_review['platform'] = None

        user_data = page_json_data['props']['apolloState'][f'User:{review_data.get('userId')}']
        parsed_user = User({
            'legacy_id': user_data.get('id'),
            'avatar': user_data.get('avatarImageUrl'),
            'name': user_data.get('name'),
            'nickname': user_data.get('nickname'),
            'privacy': user_data['playlistSettings'].get('privacy')
        })
        parsed_object['reviews']['user_reviews'].append({
            'user': parsed_user,
            'review': parsed_review
        })

    yield parsed_object

@classmethod
def parse_object_region(self, page_json_data, region):
    return Region({
        'legacy_id': region.get('id'),
        'name': region.get('name'),
        'region': region.get('region'),
        'releases': [{
            'legacy_id': release.get('id'),
            'date': release.get('date'),
            'estimated_date': release.get('estimatedDate'),
            'platform_attributes': [{
                'legacy_id': attribute.get('id'),
                'name': attribute.get('name'),
                'slug': attribute.get('slug')
            } for attribute in release['platformAttributes']],
            'age_rating': (Rating({
                'legacy_id': region['ageRating'].get('id'),
                'name': region['ageRating'].get('name'),
                'slug': region['ageRating'].get('slug'),
                'type': region['ageRating'].get('ageRatingType'),
                'descriptors': [descriptor['name'] for descriptor in region['ageRatingDescriptors']]
            }) if region['ageRating'] is not None else None)
        } for release in region['releases']]
    })