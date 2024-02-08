import scrapy
import json
import re
from . import html_methods
from imagine_games_scraper.items.content import Article, Content, ContentCategory, Brand
from imagine_games_scraper.items.user import User, ReporterReview

@classmethod
def parse_article_page(self, response, recursion_level = 0):
    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    page_data = page_json_data['props']['pageProps']['page']
    apollo_state = page_json_data['props']['apolloState']

    modern_article_ref = apollo_state['ROOT_QUERY'].get(f"article({{\"slug\":\"{page_data.get('slug')}\"}})")
    modern_article_data = page_json_data['props']['apolloState'][modern_article_ref['__ref']]
    article_content_data = apollo_state[modern_article_data['content']['__ref']]

    contributor_users = [User(apollo_state[contributor_ref['__ref']], { 'avatar': apollo_state[contributor_ref['__ref']]['thumbnailUrl'] }) for contributor_ref in article_content_data.get('contributorsOrBylines')] 
    for contributor in contributor_users:
        yield scrapy.Request(url="https://www.ign.com/person/"+contributor.get('nickname'), callback=self.parse_contributor_page)

    object_regex = re.compile(r"objects\({.*}\)")
    object_key = next((key for key in article_content_data if object_regex.search(key)))
    object_items = [apollo_state[object_ref['__ref']] for object_ref in article_content_data[object_key]]
    for obj in object_items:
        yield scrapy.Request(url="https://www.ign.com" + obj['url'], callback=self.parse_object_page)

    html_data = html_methods.HTML_DOCUMENT(modern_article_data['article'].get('processedHtml'))
    element_filter = lambda x : x.get('data-transform', None) is not None
    embedded_elements = filter(element_filter, html_data.get_element_attributes())
    embeds = {
        'polls': [],
        'videos': [],
        'slideshows': [],
        'captioned_images': [],
        'commerce_deals': []
    }
    for element in embedded_elements:
        data_transform = element.get('data-transform')
        key_terms = lambda arr, str : all(sub_str in str for sub_str in arr)
        element_root_key = next((key for key in apollo_state['ROOT_QUERY'] if data_transform in ['slideshow', 'polls', 'ignvideo', 'image-with-caption', 'commerce-deal'] and key_terms([data_transform, element.get('data-slug')], key)), None)

        if element_root_key and data_transform == 'slideshow':
            embeds['slideshows'].append(self.parse_slideshow(page_json_data, element, element_root_key))
        elif element_root_key and data_transform == 'polls':
            embeds['polls'].append(self.parse_poll(page_json_data, element, element_root_key))
        elif element_root_key and data_transform == 'ignvideo':
            embeds['videos'].append(self.parse_video(page_json_data, element, element_root_key))
        elif element_root_key and data_transform == 'image-with-caption':
            embeds['captioned_images'].append(self.parse_captioned_image(page_json_data, element, element_root_key))
        elif element_root_key and data_transform == 'commerce-deal':
            embeds['commerce_deals'].append(self.parse_slideshow(page_json_data, element, element_root_key))
        # else: print(element)
    # Last Here

    if recursion_level < 1:
        recommendation_regex = re.compile(r"topPages\({.*}\)")
        recommendation_key = next((key for key in apollo_state['ROOT_QUERY'] if recommendation_regex.search(key)))
        recommendation_refs = [ref['__ref'] for ref in apollo_state['ROOT_QUERY'][recommendation_key]]

        for modern_article in [apollo_state[ref] for ref in recommendation_refs]:
            article_content = apollo_state[modern_article['content']['__ref']]
            yield scrapy.Request(url="https://www.ign.com" + article_content.get('url'), callback=self.parse_article_page, cb_kwargs={ 'recursion_level': recursion_level + 1 })
   

    yield Article({
        'legacy_id': page_json_data.get('id'),
        'content': Content(article_content_data, {
            'category': ContentCategory(apollo_state[article_content_data['contentCategory']['__ref']]),
            'brand': Brand(apollo_state[article_content_data['brand']['__ref']]),
            'contributors': contributor_users,
            'objects': object_items
        }),
        'article': {
            'hero_video_content_id': modern_article_data['article'].get('heroVideoContentId'),
            'hero_video_content_slug': modern_article_data['article'].get('heroVideoContentSlug'),
            'processed_html': modern_article_data['article'].get('processedHtml')
        },
        'embeds': embeds,
        'review': (ReporterReview(apollo_state[f'Review:{page_data['review']['id']}']) if page_data.get('review', None) is not None else None)
    })

@classmethod
def parse_slideshow(self, page_json_data, element, element_root_key):
    pass

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
    pass