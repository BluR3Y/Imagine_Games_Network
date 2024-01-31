import scrapy
import json
from imagine_games_scraper.items import Video

@classmethod
def parse_video_page(self, response, recursion_level = 0):
    # Creating a Video item instance to store the scraped data
    video_item = Video({ 'url': response.url })

    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    # Selection of page meta data from json object
    page_data = page_json_data['props']['pageProps']['page']
    video_data = page_json_data['props']['apolloState'][f'ModernContent:{page_data['videoId']}']
    video_metadata = page_data['video']['videoMetadata']

    video_item['legacy_id'] = page_data['videoId']
    video_item['description'] = page_data['description']
    video_item['slug'] = page_data['slug']
    video_item['category'] = page_data['category']
    video_item['vertical'] = page_data['vertical']
    video_item['publish_date'] = video_data['publishDate']
    video_item['modify_date'] = video_data['updatedAt']
    video_item['title'] = video_data['title']
    video_item['subtitle'] = video_data['subtitle']
    video_item['thumbnail'] = video_data['feedImage']['url']
    video_item['brand'] = video_data['brand']
    video_item['events'] = video_data['events']
    video_item['metadata'] = {
        'duration': video_metadata['duration'],
        'description_html': video_metadata['descriptionHtml'],
        'm3u': video_metadata['m3uUrl']
    }

    video_item['objects'] = [self.parse_video_object(page_json_data, object) for object in page_json_data['props']['pageProps']['page']['additionalDataLayer']['content']['objectIds']]

    video_item['contributors'] = [{
        'legacy_id': contributor['id'],
        'name': contributor['name'],
        'nickname': contributor['nickname']
    } for contributor in page_data['contentForGA']['contributors']]

    video_item['assets'] = [{
        'url': asset['url'],
        'width': asset['width'],
        'height': asset['height'],
        'fps': asset['fps']
    } for asset in page_data['video']['assets']]

    video_item['recommendations'] = [{
        'duration': recommendation['duration'],
        'title': recommendation['title'],
        'url': recommendation['url'],
        'legacy_id': recommendation['videoId'],
        'thumbnail': recommendation['thumbnailUrl'],
        'slug': recommendation['slug']
    } for recommendation in page_data['video']['recommendations']]

    if recursion_level < 1:
        for recommendation in page_data['video']['recommendations']:
            recommendation_url = 'https://www.ign.com' + recommendation['url']
            yield scrapy.Request(url=recommendation_url, callback=self.parse_video_page, cb_kwargs={ 'recursion_level': recursion_level + 1 })

    # Yielding the Video Item for further processing or storage
    yield video_item

@classmethod
def parse_video_object(self, page_json_data, object_key):
    object_data = page_json_data['props']['apolloState'][f'Object:{object_key}']

    return dict({
        'legacy_id': object_data.get('id'),
        'url': object_data.get('url'),
        'slug': object_data.get('slug'),
        'type': object_data.get('type'),
        'cover': object_data['primaryImage'].get('url'),
        'names': {
            'primary': object_data['metadata']['names'].get('name'),
            'alt': object_data['metadata']['names'].get('alt'),
            'short': object_data['metadata']['names'].get('short')
        },
        'descriptions': {
            'long': object_data['metadata']['descriptions'].get('long'),
            'short': object_data['metadata']['descriptions'].get('short')
        },
        'franchises': [{
            'name': franchise.get('name'),
            'slug': franchise.get('slug')
        } for franchise in object_data['franchises']],
        'genres': [{
            'name': genre.get('name'),
            'slug': genre.get('slug')
        } for genre in object_data['genres']],
        'features': [{
            'name': feature.get('name'),
            'slug': feature.get('slug')
        } for feature in object_data['features']],
        'producers': [{
            'name': producer.get('name'),
            'short_name': producer.get('shortName'),
            'slug': producer.get('slug')
        } for producer in object_data['producers']],
        'publishers': [{
            'name': publisher.get('name'),
            'short_name': publisher.get('shortName'),
            'slug': publisher.get('slug')
        } for publisher in object_data['publishers']],
        # 'regions': self.parse_object_regions(page_json_data, [region['__ref'] for region in object_data['objectRegions']])
        'regions': [self.parse_object_region(page_json_data, region['__ref']) for region in object_data['objectRegions']]
    })

@classmethod
def parse_object_region(self, page_json_data, region_key):
    region_object = page_json_data['props']['apolloState'][region_key]
    region_rating_ref = region_object['ageRating']['__ref'] if region_object.get('ageRating') else None
    region_rating_object = page_json_data['props']['apolloState'].get(region_rating_ref)

    parsed_region_object = {
        'legacy_id': region_object.get('id'),
        'name': region_object.get('name'),
        'region': region_object.get('region'),
        'releases': [],
        **({
            'age_rating': {
                'legacy_id': region_rating_object['id'],
                'name': region_rating_object['name'],
                'slug': region_rating_object['slug'],
                'type': region_rating_object['ageRatingType'],
                'descriptors': [descriptor['name'] for descriptor in region_object['ageRatingDescriptors']]
            }
        } if region_rating_ref is not None else {})
    }
    for region_release_key in [release['__ref'] for release in region_object['releases']]:
        region_release_object = page_json_data['props']['apolloState'][region_release_key]
        parsed_region_released_object = {
            'legacy_id': region_release_object.get('id'),
            'date': region_release_object.get('date'),
            'platform_attributes': []
        }
        for release_platform_key in region_release_object['platformAttributes']:
            release_platform_object = page_json_data['props']['apolloState'][release_platform_key['__ref']]
            parsed_region_released_object['platform_attributes'].append({
                'legacy_id': release_platform_object.get('id'),
                'name': release_platform_object.get('name')
            })
        parsed_region_object['releases'].append(parsed_region_released_object)
    return parsed_region_object