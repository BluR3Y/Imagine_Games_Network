import scrapy
import json
from . import html_methods
from imagine_games_scraper.items.content import Content, ContentCategory
from imagine_games_scraper.items.article import Article
from imagine_games_scraper.items.misc import Catalog, CommerceDeal, Slideshow, Image
from imagine_games_scraper.items.user import User

@classmethod
def parse_article_page(self, response, recursion_level = 0):
    # Creating an Article item instance to store the scraped data
    article_item = Article({ 'url': response.url })

    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    # with open('ign_scraping_article_data.json', 'w') as f:
    #     json.dump(page_json_data, f)
    
    # Select page metadata from json object
    page_data = page_json_data['props']['pageProps']['page']
    root_query = page_json_data['props']['apolloState']['ROOT_QUERY']
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
    article_item['contributors'] = []
    article_item['objects'] = []
    article_item['embedded_content'] = {
        'polls': [],
        'videos': [],
        'slideshows': [],
        'captioned_images': [],
        'commerce_deals': []
    }

    for contributor in page_data['contributors']:
        uri = "/person/" + contributor['nickname']
        # article_item['contributors'].append(contributor['id'])
        # yield scrapy.Request(url="https://www.ign.com" + uri, callback=self.parse_contributor_page, cb_kwargs={ 'contributor_item': User(contributor) })
    
    for object in page_data['objects']:
        article_item['objects'].append(object['id'])
        yield scrapy.Request(url="https://www.ign.com" + object['url'], callback=self.parse_object_page)
        
    html_data = html_methods.HTML_DOCUMENT(page_data.get('processedHtml'))
    element_filter = lambda x : x.get('data-transform', None) is not None
    embedded_elements = filter(element_filter, html_data.get_element_attributes())

    for element in embedded_elements:
        data_transform = element.get('data-transform')
        key_terms = lambda arr, str : all(sub_str in str for sub_str in arr)
        element_root_key = next((key for key in root_query if data_transform in ['slideshow', 'polls', 'ignvideo', 'image-with-caption', 'commerce-deal'] and key_terms([data_transform, element.get('data-slug')], key)), None)
        if element_root_key and data_transform == 'slideshow':
            article_item['embedded_content']['slideshows'].append(self.parse_slideshow(page_json_data, element, element_root_key))
        elif element_root_key and data_transform == 'polls':
            article_item['embedded_content']['polls'].append(self.parse_poll(page_json_data, element, element_root_key))
        elif element_root_key and data_transform == 'ignvideo':
            article_item['embedded_content']['videos'].append(self.parse_video(page_json_data, element, element_root_key))
        elif element_root_key and data_transform == 'image-with-caption':
            article_item['embedded_content']['captioned_images'].append(self.parse_captioned_image(page_json_data, element, element_root_key))
        elif element_root_key and data_transform == 'commerce-deal':
            article_item['embedded_content']['commerce_deals'].append(self.parse_slideshow(page_json_data, element, element_root_key))
        # else: print(element)

    if recursion_level < 1:
        for recommendation in article_item['recommendations']:
            recommendation_url = 'https://www.ign.com' + recommendation['url']
            yield scrapy.Request(url=recommendation_url, callback=self.parse_article_page, cb_kwargs={ 'recursion_level': recursion_level + 1 })

    # Yielding the Article Item for further processing or storage
    yield article_item

@classmethod
def parse_slideshow(self, page_json_data, element, element_root_key):
    element_root_data = page_json_data['props']['apolloState']['ROOT_QUERY'][element_root_key]
    element_content_data = page_json_data['props']['apolloState'][element_root_data['content']['__ref']]
    element_image_key = next((key for key in element_root_data if 'slideshowImages' in key), None)
    element_images = [page_json_data['props']['apolloState'][image_ref.get('__ref')] for image_ref in element_root_data[element_image_key]['images']]
    return Slideshow({
        'slug': element['data-slug'],
        'content': Content({
            # 'legacy_id': element_content_data.get('id'),
            # 'type': element_content_data.get('type', 'slideshow'),
            # 'vertical': element_content_data.get('vertical'),
            # 'url': element_content_data.get('url'),
            # 'title': element_content_data.get('title'),
            # 'subtitle': element_content_data.get('subtitle'),
            # 'feed_title': element_content_data.get('feedTitle'),
            # 'feed_image': (Image({
            #     'legacy_id': element_content_data['feedImage'].get('id'),
            #     'url': element_content_data['feedImage'].get('url'),
            #     'caption': element_content_data['feedImage'].get('caption'),
            #     'embargo_date': element_content_data['feedImage'].get('embargoDate')
            # }) if element_content_data.get('feedImage', None) is not None else None),
            # 'slug': element_content_data.get('slug'),
            # 'publish_date': element_content_data.get('publishDate'),
            # 'category': ContentCategory({
            #     'legacy_id': element_content_data.get('id', None),
            #     'name': element_content_data.get('name')
            # }),
            # 'events': element_content_data.get('events'),
            # 'attributes': element_content_data.get('attributes'),
            # Last Here
        }),
        'images': [Image({
            'legacy_id': image.get('id'),
            'url': image.get('url'),
            'caption': image.get('caption'),
            'embargo_date': image.get('embargoDate')
        }) for image in element_images]
    })

@classmethod
def parse_poll(self, page_json_data, element):
    pass

@classmethod
def parse_video(self, page_json_data, element):
    pass

@classmethod
def parse_captioned_image(self, page_json_data, element):
    pass

@classmethod
def parse_commerce_deal(self, page_json_data, element, element_root_key):
    element_root_data = page_json_data['props']['apolloState']['ROOT_QUERY'][element_root_key]
    element_content_data = page_json_data['props']['apolloState'][element_root_data['content']['__ref']]
    element_content_items = [page_json_data['props']['apolloState'][item['__ref']] for item in element_root_data['items']]
    return Catalog({
        'slug': element['data-slug'],
        'content': Content({
            'legacy_id': element_content_data.get('id'),
            'type': element_content_data.get('type', 'catalog'),
            'title': element_content_data.get('title'),
            'slug': element['data-slug'],
            'modify_date': element_content_data.get('updatedAt')
        }),
        'items': [CommerceDeal({
            'legacy_id': item.get('id'),
            'url': item.get('url'),
            'title': item.get('title'),
            'description': item.get('description'),
            'brand': item.get('brand'),
            'model': item.get('model'),
            'vendor': item.get('vendor'),
            'price': item.get('price'),
            'msrp': item.get('msrp'),
            'discount': item.get('discount'),
            'coupon_code': item.get('couponCode'),
            'is_large': item.get('large'),
            'region_code': item.get('regionCode'),
            'cover': item['image'].get('url')
        }) for item in element_content_items]
    })


# @classmethod
# def parse_article_slideshow(self, page_json_data, slideshow_key):
#     slideshow_object = page_json_data['props']['apolloState']['ROOT_QUERY'][slideshow_key]
#     slideshow_content = page_json_data['props']['apolloState'][slideshow_object['content']['__ref']]
#     gallery_key = next((key for key in slideshow_object if 'slideshowImages' in key), None)
#     image_keys = [image['__ref'] for image in slideshow_object[gallery_key]['images']]
#     image_objects = [page_json_data['props']['apolloState'][key] for key in image_keys]

#     return dict({
#         'legacy_id': slideshow_content['id'],
#         'url': slideshow_content['url'],
#         'slug': slideshow_content['slug'],
#         'title': slideshow_content['title'],
#         'subtitle': slideshow_content['subtitle'],
#         'publish_date': slideshow_content['publishDate'],
#         'vertical': slideshow_content['vertical'],
#         'brand': slideshow_content['brand'],
#         'category': slideshow_content['contentCategory']['name'],
#         'images': [{
#             'legacy_id': image['id'],
#             'url': image['url'],
#             'caption': image['caption']
#         } for image in image_objects]
#     })

# @classmethod
# def parse_object_wiki(self, page_json_data, wiki_key):
#     key_params_str = wiki_key[wiki_key.find('{'):wiki_key.find('}') + 1]
#     key_params_json = json.loads(key_params_str)
#     wiki_items = page_json_data['props']['apolloState']['ROOT_QUERY'][wiki_key]['navigation']
#     return dict({
#         **key_params_json,
#         'navigation': [{
#             'label': item.get('label'),
#             'url': item.get('url')
#         } for item in wiki_items]
#     })

# @classmethod
# def parse_object_poll(self, page_json_data, poll_key):
#     poll_ref = page_json_data['props']['apolloState']['ROOT_QUERY'][poll_key]['__ref']
#     poll_object = page_json_data['props']['apolloState'][poll_ref]
#     poll_content = page_json_data['props']['apolloState'][poll_object['content']['__ref']]
#     content_category = page_json_data['props']['apolloState'][poll_content['contentCategory']['__ref']]
#     poll_answers = [page_json_data['props']['apolloState'][key['__ref']] for key in poll_object['answers']]

#     return dict({
#         'legacy_id': poll_content['id'],
#         'url': poll_content['url'],
#         'title': poll_content['title'],
#         'subtitle': poll_content['subtitle'],
#         'slug': poll_content['slug'],
#         'publish_date': poll_content['publishDate'],
#         'category': content_category['name'],
#         'vertical': poll_content['vertical'],
#         'brand': poll_content['brand'],
#         'answers': [answer['answer'] for answer in poll_answers]
#     })