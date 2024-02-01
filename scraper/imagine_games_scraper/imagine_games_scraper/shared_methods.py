import json
import scrapy
from imagine_games_scraper.items import Reporter, Entertainment

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

    with open('ign_scraping_game_data.json', 'w') as f:
        json.dump(page_json_data, f)

    page_data = page_json_data['props']['pageProps']['page']
    parsed_object = Entertainment({
        'legacy_id': page_data.get('id'),
        'uri': page_data.get('url'),
        'slug': page_data.get('slug'),
        'type': page_data.get('type'),
        'wiki_slug': page_data.get('wikiSlug'),
        'cover': page_data['primaryImage'].get('url')
    })
    if 'names' in page_data['metadata']:
        parsed_object['names'] = {
            'primary': page_data['metadata']['names'].get('name'),
            'alt': page_data['metadata']['names'].get('alt'),
            'short': page_data['metadata']['names'].get('short')
        }
    if 'descriptions' in page_data['metadata']:
        parsed_object['descriptions'] = {
            'long': page_data['metadata']['descriptions'].get('long'),
            'short': page_data['metadata']['descriptions'].get('short')
        }
    if 'franchises' in page_data:
        parsed_object['franchises'] = [{
            'name': franchise.get('name'),
            'slug': franchise.get('slug')
        } for franchise in page_data['franchises']]
    if 'genres' in page_data:
        parsed_object['genres'] = [{
            'name': genre.get('name'),
            'slug': genre.get('slug')
        } for genre in page_data['genres']]
    if 'features' in page_data:
        parsed_object['features'] = [{
            'name': feature.get('name'),
            'slug': feature.get('slug')
        } for feature in page_data['features']]
    if 'producers' in page_data:
        parsed_object['producers'] = [{
            'name': producer.get('name'),
            'short_name': producer.get('shortName'),
            'slug': producer.get('slug')
        } for producer in page_data['producers']]
    if 'publishers' in page_data:
        parsed_object['publishers'] = [{
            'name': publisher.get('name'),
            'short_name': publisher.get('shortName'),
            'slug': publisher.get('slug')
        } for publisher in page_data['publishers']]
    parsed_object['regions'] = [self.parse_object_region(page_json_data, region) for region in page_data['objectRegions']]

    yield parsed_object

@classmethod
def parse_object_region(self, page_json_data, region):
    return dict({
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
            'age_rating': ({
                'legacy_id': region['ageRating'].get('id'),
                'name': region['ageRating'].get('name'),
                'slug': region['ageRating'].get('slug'),
                'age_rating_type': region['ageRating'].get('ageRatingType'),
                'rating_descriptors': [descriptor['name'] for descriptor in region['ageRatingDescriptors']]
            } if region['ageRating'] is not None else None)
        } for release in region['releases']],
    })