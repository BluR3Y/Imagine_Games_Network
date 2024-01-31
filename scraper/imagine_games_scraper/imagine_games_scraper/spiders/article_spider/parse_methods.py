import scrapy
import json
from imagine_games_scraper.items import Article

@classmethod
def parse_article_page(self, response, recursion_level = 0):
    # Creating an Article item instance to store the scraped data
    article_item = Article({ 'url': response.url })

    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)
    
    # Select page metadata from json object
    page_data = page_json_data['props']['pageProps']['page']
    article_item['legacy_id'] = page_data.get('id')
    article_item['cover'] = page_data.get('image')
    article_item['title'] = page_data.get('pageTitle')
    article_item['subtitle'] = page_data.get('subtitle')
    article_item['description'] = page_data.get('description')
    article_item['excerpt'] = page_data.get('excerpt')
    article_item['publish_date'] = page_data.get('publishDate')
    article_item['modify_date'] = page_data['schema'].get('dateModified')
    article_item['slug'] = page_data.get('slug')
    article_item['category'] = page_data.get('category')
    article_item['vertical'] = page_data.get('vertical')
    article_item['processedHtml'] = page_data.get('processedHtml')
    article_item['brand'] = page_data.get('brand')
    article_item['embeded_content'] = self.parse_html_content(page_json_data)

    article_item['contributors'] = [self.parse_article_contributor(page_json_data, contributor['id']) for contributor in page_json_data['props']['pageProps']['page']['contributors']]
    
    article_item['objects'] = [self.parse_article_object(page_json_data, f'Object:{object['id']}') for object in page_data['objects']]

    recommendation_key = next((key for key in page_json_data['props']['apolloState']['ROOT_QUERY'] if 'topPages' in key), None)
    article_item['recommendations'] = [self.parse_article_recommendation(page_json_data, recommendation['__ref']) for recommendation in page_json_data['props']['apolloState']['ROOT_QUERY'].get(recommendation_key, [])]

    slideshow_keys = [key for key in page_json_data['props']['apolloState']['ROOT_QUERY'] if 'slideshow' in key]
    article_item['slideshows'] = [self.parse_article_slideshow(page_json_data, key) for key in slideshow_keys]

    wiki_key = next((key for key in page_json_data['props']['apolloState']['ROOT_QUERY'] if 'wiki' in key), None)
    article_item['object_wiki'] = self.parse_object_wiki(page_json_data, wiki_key) if wiki_key is not None else None

    poll_keys = [key for key in page_json_data['props']['apolloState']['ROOT_QUERY'] if 'poll' in key]
    article_item['polls'] = [self.parse_object_poll(page_json_data, key) for key in poll_keys]

    review_data = page_data['review']
    article_item['review'] = None if review_data is None else {
        'legacy_id': review_data.get('id'),
        'title': page_data.get('feedTitle'),
        'score': review_data.get('score'),
        'score_text': review_data.get('scoreText'),
        'editors_choice': review_data.get('editorsChoice'),
        'score_summary': review_data.get('scoreSummary'),
        'verdict': review_data.get('verdict'),
        'review_date': review_data.get('reviewedOn')
    }

    if recursion_level < 1:
        for recommendation in article_item['recommendations']:
            recommendation_url = 'https://www.ign.com' + recommendation['url']
            yield scrapy.Request(url=recommendation_url, callback=self.parse_article_page, cb_kwargs={ 'recursion_level': recursion_level + 1 })

    # Yielding the Article Item for further processing or storage
    yield article_item

@classmethod
def parse_article_object(self, page_json_data, object_key):
    object_data = page_json_data['props']['apolloState'][object_key]
    parsed_item = {
        'legacy_id': object_data['id'],
        'url': object_data['url'],
        'slug': object_data['slug'],
        'type': object_data['type']
    }

    if 'names' in object_data['metadata']:
        parsed_item['names'] = {
            'primary': object_data['metadata']['names'].get('name'),
            'alt': object_data['metadata']['names'].get('alt'),
            'short': object_data['metadata']['names'].get('short')
        }
    if 'descriptions' in object_data['metadata']:
        parsed_item['descriptions'] = {
            'long': object_data['metadata']['descriptions'].get('long'),
            'short': object_data['metadata']['descriptions'].get('short')
        }
    if 'franchises' in object_data:
        parsed_item['franchises'] = [{
            'name': franchise.get('name'),
            'slug': franchise.get('slug')
        } for franchise in object_data['franchises']]
    if 'genres' in object_data:
        parsed_item['genres'] = [{
            'name': genre.get('name'),
            'slug': genre.get('slug')
        } for genre in object_data['genres']]
    if 'features' in object_data:
        parsed_item['features'] = [{
            'name': feature.get('name'),
            'slug': feature.get('slug')
        } for feature in object_data['features']]
    if 'producers' in object_data:
        parsed_item['producers'] = [{
            'name': producer.get('name'),
            'short_name': producer.get('shortName'),
            'slug': producer.get('slug')
        } for producer in object_data['producers']]
    if 'publishers' in object_data:
        parsed_item['publishers'] = [{
            'name': publisher.get('name'),
            'short_name': publisher.get('shortName'),
            'slug': publisher.get('slug')
        } for publisher in object_data['publishers']]

    region_key = next((key for key in object_data if 'objectRegions' in key))
    if region_key is not None:
        parsed_item['regions'] = [self.parse_object_region(page_json_data, region['__ref']) for region in object_data[region_key]]
    
    return parsed_item

# Missing: Embeded HTML Content
@classmethod
def parse_html_content(self, page_json_data):
    pass

@classmethod
def parse_article_contributor(self, page_json_data, contributor_id):
    contributor_data = page_json_data['props']['apolloState'][f'Contributor:{contributor_id}']

    contributor_object = {
        'legacy_author_id': contributor_data['authorId'],
        'legacy_id': contributor_id,
        'thumbnail_url': contributor_data['thumbnailUrl'],
        'name': contributor_data['name'],
        'nickname': contributor_data['nickname']
    }
    
    # Extracts related reviews by contributor if article is a review
    feed_partial_key = 'contentFeed'
    feed_complete_key = next((key for key in contributor_data if feed_partial_key in key), None)
    if (feed_complete_key):
        feed_params_str = feed_complete_key[len(feed_partial_key) + 1:]
        contributor_object['recommendation_feed'] = {
            **(json.loads(feed_params_str)),
            'feed_items': []
        }

        for feed_key in [feed_key['__ref'] for feed_key in contributor_data[feed_complete_key]['feedItems']]:
            feed_article_data = page_json_data['props']['apolloState'][feed_key]
            feed_content_data = page_json_data['props']['apolloState'][f'ModernContent:{feed_article_data['content']['id']}']
            feed_object_data = page_json_data['props']['apolloState'][feed_content_data['primaryObject']['__ref']]

            contributor_object['recommendation_feed']['feed_items'].append({
                'url': feed_content_data.get('url'),
                'slug': feed_content_data.get('slug'),
                'legacy_id': feed_content_data.get('id'),
                'type': feed_content_data.get('type'),
                'cover': feed_content_data['feedImage'].get('url'),
                'title': feed_content_data.get('title'),
                'subtitle': feed_content_data.get('subtitle'),
                'publish_date': feed_content_data.get('publishDate'),
                'category': page_json_data['props']['apolloState'][feed_content_data['contentCategory']['__ref']].get('name'),
                'review': {
                    'score': feed_article_data['review'].get('score')
                },
                'primary_object': {
                    'legacy_id': feed_object_data.get('id'),
                    'url': feed_object_data.get('url'),
                    'slug': feed_object_data.get('slug'),
                    'type': feed_object_data.get('type'),
                    'names': {
                        'primary': feed_object_data['metadata']['names'].get('name'),
                        'alt': feed_object_data['metadata']['names'].get('alt'),
                        'short': feed_object_data['metadata']['names'].get('short')
                    },
                    'franchises': feed_object_data.get('franchises'),
                    # 'regions': self.parse_object_regions(page_json_data, [region_item['__ref'] for region_item in feed_object_data[next((key for key in feed_object_data if 'objectRegions' in key), None)]])
                    'regions': [self.parse_object_region(page_json_data, region['__ref']) for region in feed_object_data[next((key for key in feed_object_data if 'objectRegions' in key), None)]]
                }
            })
    return contributor_object

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

@classmethod
def parse_article_recommendation(self, page_json_data, article_key):
    article_key = page_json_data['props']['apolloState'][article_key]['content']['__ref']
    article_object = page_json_data['props']['apolloState'][article_key]
    article_category = page_json_data['props']['apolloState'][article_object['contentCategory']['__ref']]
    article_primay_object = article_object['primaryObject']
        
    return dict({
        'legacy_id': article_object['id'],
        'url': article_object['url'],
        'slug': article_object['slug'],
        'type': article_object['type'],
        'title': article_object['title'],
        'subtitle': article_object['subtitle'],
        'publish_date': article_object['publishDate'],
        'cover': article_object['feedImage']['url'],
        'category': article_category['name'],
        'brand': article_object['brand'],
        # 'primary_object': self.parse_article_objects(page_json_data, [article_primay_object['__ref']])[0] if article_primay_object is not None else None,
        'primary_object': self.parse_article_object(page_json_data,article_primay_object['__ref'])
    })

@classmethod
def parse_article_slideshow(self, page_json_data, slideshow_key):
    slideshow_object = page_json_data['props']['apolloState']['ROOT_QUERY'][slideshow_key]
    slideshow_content = page_json_data['props']['apolloState'][slideshow_object['content']['__ref']]
    gallery_key = next((key for key in slideshow_object if 'slideshowImages' in key), None)
    image_keys = [image['__ref'] for image in slideshow_object[gallery_key]['images']]
    image_objects = [page_json_data['props']['apolloState'][key] for key in image_keys]

    return dict({
        'legacy_id': slideshow_content['id'],
        'url': slideshow_content['url'],
        'slug': slideshow_content['slug'],
        'title': slideshow_content['title'],
        'subtitle': slideshow_content['subtitle'],
        'publish_date': slideshow_content['publishDate'],
        'vertical': slideshow_content['vertical'],
        'brand': slideshow_content['brand'],
        'category': slideshow_content['contentCategory']['name'],
        'images': [{
            'legacy_id': image['id'],
            'url': image['url'],
            'caption': image['caption']
        } for image in image_objects]
    })

@classmethod
def parse_object_wiki(self, page_json_data, wiki_key):
    key_params_str = wiki_key[wiki_key.find('{'):wiki_key.find('}') + 1]
    key_params_json = json.loads(key_params_str)
    wiki_items = page_json_data['props']['apolloState']['ROOT_QUERY'][wiki_key]['navigation']
    return dict({
        **key_params_json,
        'navigation': [{
            'label': item.get('label'),
            'url': item.get('url')
        } for item in wiki_items]
    })

@classmethod
def parse_object_poll(self, page_json_data, poll_key):
    poll_ref = page_json_data['props']['apolloState']['ROOT_QUERY'][poll_key]['__ref']
    poll_object = page_json_data['props']['apolloState'][poll_ref]
    poll_content = page_json_data['props']['apolloState'][poll_object['content']['__ref']]
    content_category = page_json_data['props']['apolloState'][poll_content['contentCategory']['__ref']]
    poll_answers = [page_json_data['props']['apolloState'][key['__ref']] for key in poll_object['answers']]

    return dict({
        'legacy_id': poll_content['id'],
        'url': poll_content['url'],
        'title': poll_content['title'],
        'subtitle': poll_content['subtitle'],
        'slug': poll_content['slug'],
        'publish_date': poll_content['publishDate'],
        'category': content_category['name'],
        'vertical': poll_content['vertical'],
        'brand': poll_content['brand'],
        'answers': [answer['answer'] for answer in poll_answers]
    })