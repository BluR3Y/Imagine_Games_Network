import scrapy
import json
from imagine_games_scraper.items import Article, Reporter
from . import element_methods

@classmethod
def parse_article_page(self, response, recursion_level = 0):
    # Creating an Article item instance to store the scraped data
    article_item = Article({ 'url': response.url })

    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    with open('ign_scraping_game_review.json', 'w') as f:
        json.dump(page_json_data, f)
    
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
    article_item['contributors'] = []
    article_item['objects'] = []

    # article_item['contributors'] = [self.parse_article_contributor(page_json_data, contributor['id']) for contributor in page_json_data['props']['pageProps']['page']['contributors']]
    for contributor in page_data['contributors']:
        uri = "/person/" + contributor['nickname']
        article_item['contributors'].append(contributor['id'])
        yield scrapy.Request(url="https://www.ign.com" + uri, callback=self.parse_contributor_page)
    
    # article_item['objects'] = [self.parse_article_object(page_json_data, f'Object:{object['id']}') for object in page_data['objects']]
    for object in page_data['objects']:
        article_item['objects'].append(object['id'])
        yield scrapy.Request(url="https://www.ign.com" + object['url'], callback=self.parse_object_page)

    # * Missing: Move this to shared_methods.scrape_object_page()

    # slideshow_keys = [key for key in page_json_data['props']['apolloState']['ROOT_QUERY'] if 'slideshow' in key]
    # article_item['slideshows'] = [self.parse_article_slideshow(page_json_data, key) for key in slideshow_keys]

    # poll_keys = [key for key in page_json_data['props']['apolloState']['ROOT_QUERY'] if 'poll' in key]
    # article_item['polls'] = [self.parse_object_poll(page_json_data, key) for key in poll_keys]

    if recursion_level < 1:
        for recommendation in article_item['recommendations']:
            recommendation_url = 'https://www.ign.com' + recommendation['url']
            yield scrapy.Request(url=recommendation_url, callback=self.parse_article_page, cb_kwargs={ 'recursion_level': recursion_level + 1 })

    # Yielding the Article Item for further processing or storage
    yield article_item

# Missing: Embeded HTML Content
@classmethod
def parse_html_content(self, page_json_data):
    pass

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