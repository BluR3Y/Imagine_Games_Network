import scrapy
import json
import re

from imagine_games_scraper.items.user import User, Author
from imagine_games_scraper.items.object import Object, Region, HowLongToBeat, Release, AgeRating, ObjectAttributeConnection
from imagine_games_scraper.items.misc import Attribute, TypedAttribute
from imagine_games_scraper.items.content import ContentAttributeConnection, ObjectConnection, Contributor, Content, ContentCategory, Brand, UserReview, UserReviewTag
from imagine_games_scraper.items.wiki import WikiObject
from imagine_games_scraper.items.media import Image

def parse_contributor_page(self, response, author_item = Author(), recursion_level = 0):
    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    page_data = page_json_data['props']['pageProps']['page']
    author_data = page_data['author']
    # Missing: Contributor related Articles

    author_item['legacy_id'] = author_data.get('authorId')
    author_url = author_data.get('profileUrl')
    author_item['url'] = author_url.replace("https://www.ign.com", "")
    author_item['position'] = author_data.get('position')
    author_item['bio'] = author_data.get('bio')
    author_item['location'] = author_data.get('location')
    author_item['socials'] = author_data.get('socials')

    cover_ref = author_data.get('backgroundImageUrl')
    if cover_ref:
        cover_image_item = Image()
        cover_image_item['url'] = cover_ref

        yield cover_image_item
        author_item['cover_id'] = cover_image_item.get('id')

    yield author_item

def parse_object_page(self, response, object_item = Object(), recursion_level = 0):
    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    page_data = page_json_data['props']['pageProps']['page']
    apollo_state = page_json_data['props']['apolloState']
    object_data = apollo_state[f'Object:{page_data.get('id')}']

    object_item['legacy_id'] = object_data.get('id')
    object_item['url'] = object_data.get('url')
    object_item['slug'] = object_data.get('slug')
    object_item['wiki_slug'] = object_data.get('wikiSlug')
    object_item['type'] = object_data.get('type')

    object_item['names'] = {
        'primary': object_data['metadata']['names'].get('name'),
        'alt': object_data['metadata']['names'].get('alt'),
        'short': object_data['metadata']['names'].get('short')
    }
    object_item['descriptions'] = {
        'long': object_data['metadata']['descriptions'].get('long'),
        'short': object_data['metadata']['descriptions'].get('short')
    }

    object_image_ref = object_data.get('primaryImage')
    if object_image_ref:
        object_cover_item = Image()
        object_cover_item['url'] = object_image_ref.get('url')

        yield object_cover_item
        object_item['cover_id'] = object_cover_item.get('id')

    hl2b_data = object_data.get('hl2bData')
    if hl2b_data:
        hl2b_item = HowLongToBeat()
        hl2b_item['legacy_id'] = hl2b_data.get('id')
        hl2b_item['legacy_ign_object_id'] = hl2b_data.get('ign_object_id')
        hl2b_item['steam_id'] = hl2b_data.get('steam_id')
        hl2b_item['itch_id'] = hl2b_data.get('itch_id')
        hl2b_item['platforms'] = hl2b_data.get('platforms')
        hl2b_item['list'] = hl2b_data.get('list')
        hl2b_item['review'] = hl2b_data.get('review')
        hl2b_item['time'] = hl2b_data.get('time')
        
        yield hl2b_item
        object_item['how_long_to_beat_id'] = hl2b_item.get('id')

    all_attributes = []
    all_attributes.extend([{
        'type': 'franchise',
        'name': attr.get('name'),
        'short_name': attr.get('shortName'),
        'slug': attr.get('slug', attr.get('name').replace(' ', '-').lower())
    } for attr in object_data.get('franchises')])
    all_attributes.extend([{
        'type': 'genre',
        'name': attr.get('name'),
        'short_name': attr.get('shortName'),
        'slug': attr.get('slug', attr.get('name').replace(' ', '-').lower())
    } for attr in object_data.get('genres')])
    all_attributes.extend([{
        'type': 'feature',
        'name': attr.get('name'),
        'short_name': attr.get('shortName'),
        'slug': attr.get('slug', attr.get('name').replace(' ', '-').lower())
    } for attr in object_data.get('features')])
    all_attributes.extend([{
        'type': 'producer',
        'name': attr.get('name'),
        'short_name': attr.get('shortName'),
        'slug': attr.get('slug', attr.get('name').replace(' ', '-').lower())
    } for attr in object_data.get('producers')])
    all_attributes.extend([{
        'type': 'publisher',
        'name': attr.get('name'),
        'short_name': attr.get('shortName'),
        'slug': attr.get('slug', attr.get('name').replace(' ', '-').lower())
    } for attr in object_data.get('publishers')])

    for attr in all_attributes:
        attribute_item = Attribute()
        attribute_item['name'] = attr.get('name')
        attribute_item['short_name'] = attr.get('short_name')
        attribute_item['slug'] = attr.get('slug')
        yield attribute_item

        typed_attribute_item = TypedAttribute()
        typed_attribute_item['type'] = attr.get('type')
        typed_attribute_item['attribute_id'] = attribute_item.get('id')
        yield typed_attribute_item

        object_attribute_connection = ObjectAttributeConnection()
        object_attribute_connection['attribute_id'] = typed_attribute_item.get('id')
        object_attribute_connection['object_id'] = object_item.get('id')
        yield object_attribute_connection

    # Missing: Region
    # Missing: User Reviews
    # Missing: galleries

    yield object_item

def parse_modern_content(self, page_json_data, modern_content_key, content_item = Content(), recursion_level = 0):
    apollo_state = page_json_data['props']['apolloState']
    modern_content_data = apollo_state[modern_content_key]

    content_item['legacy_id'] = modern_content_data.get('id')
    content_item['url'] = modern_content_data.get('url')
    content_item['slug'] = modern_content_data.get('slug')
    content_item['type'] = modern_content_data.get('type')
    content_item['vertical'] = modern_content_data.get('vertical')
    content_item['title'] = modern_content_data.get('title')
    content_item['subtitle'] = modern_content_data.get('subtitle')
    content_item['feed_title'] = modern_content_data.get('feedTitle')
    content_item['excerpt'] = modern_content_data.get('excerpt')
    content_item['description'] = modern_content_data.get('description') # possibly unnecessary
    content_item['state'] = modern_content_data.get('state')
    content_item['publish_date'] = modern_content_data.get('publishDate')
    content_item['modify_date'] = modern_content_data.get('updatedAt')
    content_item['events'] = modern_content_data.get('events')

    header_image = modern_content_data.get('headerImageUrl')
    if header_image:
        header_image_item = Image()
        # Image fields
        content_item['header_image_id'] = header_image_item.get('id')

    feed_image = modern_content_data.get('feedImage')
    if feed_image:
        feed_image_item = Image()
        # Image fields
        yield feed_image_item
        content_item['feed_image_id'] = feed_image_item.get('id')

    article_contributors = []
    for user_data in [apollo_state[contributor_ref.get('__ref')] for contributor_ref in modern_content_data.get('contributorsOrBylines', [])]:
        user_item = User()
        user_item['legacy_id'] = user_data.get('id')
        user_item['name'] = user_data.get('name')
        user_item['nickname'] = user_data.get('nickname')

        user_avatar = user_data.get('avatarImageUrl')
        if user_avatar:
            user_avatar_item = Image()
            user_avatar_item['url'] = user_avatar_item

            yield user_avatar_item
            user_item['avatar_id'] = user_avatar_item.get('id')
        
        author_item = Author()
        author_item['user_id'] = user_item.get('id')
        article_contributors.append(user_item.get('id'))

        yield user_item
        yield scrapy.Request(url="https://www.ign.com/person/" + user_data.get('nickname'), callback=self.parse_contributor_page, cb_kwargs={ 'author_item': author_item, 'recursion_level': recursion_level })

    for contributor_ref in article_contributors:
        contributor_item = Contributor()
        contributor_item['user_id'] = contributor_ref
        contributor_item['content_id'] = content_item.get('id')

        yield contributor_item

    brand_ref = modern_content_data.get('brand')
    if brand_ref:
        brand_item = Brand()
        
        if brand_ref.get('__ref') is not None:
            brand_data = apollo_state[brand_ref.get('__ref')]
            brand_item = Brand()
            brand_item['legacy_id'] = brand_data.get('id')
            brand_item['slug'] = brand_data.get('slug')
            brand_item['name'] = brand_data.get('name')
            brand_item['logo_light'] = brand_data.get('logoLight')
            brand_item['logo_dark'] = brand_data.get('logoDark')
        else:
            brand_item['legacy_id'] = brand_ref.get('id')
            brand_item['slug'] = brand_ref.get('slug')
            brand_item['name'] = brand_ref.get('name')
            brand_item['logo_light'] = brand_ref.get('logoLight')
            brand_item['logo_dark'] = brand_ref.get('logoDark')

        yield brand_item
        content_item['brand_id'] = brand_item.get('id')

    primary_object_ref = modern_content_data.get('primaryObject')
    article_objects = []
    if primary_object_ref:
        primary_object_data = apollo_state[primary_object_ref.get('__ref')]
        primary_object_item = Object()

        yield scrapy.Request(url="https://www.ign.com" + primary_object_data.get('url'), callback=self.parse_object_page, cb_kwargs={ 'object_item': primary_object_item, 'recursion_level': recursion_level })
        content_item['primary_object_id'] = primary_object_item.get('id')
        article_objects.append(primary_object_item.get('id'))

    object_regex = re.compile(r"objects\({.*}\)")
    object_key = next((key for key in modern_content_data if object_regex.search(key)), None)
    if object_key:
        for object in [apollo_state[object_ref.get('__ref')] for object_ref in modern_content_data.get(object_key)[1:]]:
            object_item = Object()

            yield scrapy.Request(url="https://www.ign.com" + object_item.get('url'), callback=self.parse_object_page, cb_kwargs={ 'object_item': object_item, 'recursion_level': recursion_level })
            article_objects.append(object_item.get('id'))

    for object_ref in article_objects:
        object_connection_item = ObjectConnection()
        object_connection_item['object_id'] = object_ref
        object_connection_item['content_id'] = content_item.get('id')

        yield object_connection_item

    content_category_ref = modern_content_data.get('contentCategory')
    if content_category_ref:
        content_category_data = apollo_state[content_category_ref.get('__ref')]
        content_category_item = ContentCategory()
        content_category_item['legacy_id'] = content_category_data.get('id')
        content_category_item['name'] = content_category_data.get('name')

        yield content_category_item
        content_item['category_id'] = content_category_item.get('id')

    for attribute in modern_content_data.get('attributes', []):
        attribute_item = Attribute()
        attribute_item['name'] = attribute.get('name')
        attribute_item['short_name'] = attribute.get('short_name')
        attribute_item['slug'] = attribute.get('slug')
        yield attribute_item

        typed_attribute_item = TypedAttribute()
        typed_attribute_item['type'] = attribute.get('type')
        typed_attribute_item['attribute_id'] = attribute_item.get('id')
        yield typed_attribute_item

        attribute_connection = ContentAttributeConnection()
        attribute_connection['attribute_id'] = typed_attribute_item.get('id')
        attribute_connection['content_id'] = content_item.get('id')
        yield attribute_connection

    yield content_item

def parse_wiki_page():
    pass