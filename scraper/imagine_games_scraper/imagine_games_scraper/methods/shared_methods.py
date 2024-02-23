import scrapy
import json
import re

from imagine_games_scraper.alchemy.models.content import Content, Brand, ContentCategory, ObjectConnection, Contributor, ContentAttributeConnection

def parse_modern_content(self, page_json_data, modern_content_key, recursion_level = 0):
    content_item = Content()
    apollo_state = page_json_data['props']['apolloState']
    modern_content_data = apollo_state[modern_content_key]

    content_item.legacy_id = modern_content_data.get('id')
    content_item.url = modern_content_data.get('url')
    content_item.slug = modern_content_data.get('slug')
    content_item.type = modern_content_data.get('type')
    content_item.vertical = modern_content_data.get('vertical')
    content_item.title = modern_content_data.get('title')
    content_item.subtitle = modern_content_data.get('subtitle')
    content_item.feed_title = modern_content_data.get('feedTitle')
    content_item.excerpt = modern_content_data.get('excerpt')
    content_item.description = modern_content_data.get('description') # possibly unnecessary
    content_item.state = modern_content_data.get('state')
    content_item.publish_date = modern_content_data.get('publishDate')
    content_item.modify_date = modern_content_data.get('updatedAt')
    content_item.events = modern_content_data.get('events')
    
    header_image = modern_content_data.get('headerImageUrl')
    if header_image:
        content_item.header_image_id = self.parse_image(legacy_url=header_image.get('url'))

    feed_image = modern_content_data.get('feedImage')
    if feed_image:
        content_item.feed_image_id = self.parse_image(legacy_url=feed_image.get('url'))

    for attribute in modern_content_data.get('attributes', []):
        # Last Here