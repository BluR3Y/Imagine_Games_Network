import scrapy
import json
import re

from imagine_games_scraper.items.media import Gallery, Image, ImageConnection, Slideshow
from imagine_games_scraper.items.content import Content

def parse_slideshow_page(self, response, slideshow_item = None, recursion_level = 0):
    if slideshow_item is None:
        slideshow_item = Slideshow()

    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    page_data = page_json_data['props']['pageProps']['page']
    apollo_state = page_json_data['props']['apolloState']

    slideshow_key = next((key for key in apollo_state['ROOT_QUERY'] if page_data.get('slug') in key))
    slideshow_data = apollo_state['ROOT_QUERY'].get(slideshow_key)

    modern_content_ref = slideshow_data.get('content')
    if modern_content_ref:
        content_data = apollo_state[modern_content_ref.get('__ref')]
        modern_content_item = Content(referrers=[f"{slideshow_item.__tablename__}:{slideshow_item.get('id')}"])

        yield from self.parse_modern_content(page_json_data, modern_content_ref.get('__ref'), modern_content_item)
        slideshow_item['content_id'] = { '__ref': f"{modern_content_item.__tablename__}:{modern_content_item.get('id')}" }

    image_regex = re.compile(r"slideshowImages:{.*}")
    image_key = next((key for key in slideshow_data if image_regex.search(key)))
    if image_key:
        gallery_item = Gallery(referrers=[f"{slideshow_item.__tablename__}:{slideshow_item.get('id')}"])
        for image in [apollo_state[image_ref.get('__ref')] for image_ref in slideshow_data[image_key]['images']]:
            image_connection = ImageConnection()
            image_connection['gallery_id'] = { '__ref': f"{gallery_item.__tablename__}:{gallery_item.get('id')}" }

            image_item = Image(referrers=[f"{image_connection.__tablename__}:{image_connection.get('id')}"])
            image_item['legacy_id'] = image.get('id')
            image_item['legacy_url'] = image.get('url')
            image_item['caption'] = image.get('caption')
            image_item['embargo_date'] = image.get('embargoDate')

            yield image_item
            image_connection['image_id'] = { '__ref': f"{image_item.__tablename__}:{image_item.get('id')}" }

            yield image_connection
            gallery_item['referrers'].append(f"{image_connection.__tablename__}:{image_connection.get('id')}")
        yield gallery_item
        slideshow_item['gallery_id'] = { '__ref': f"{gallery_item.__tablename__}:{gallery_item.get('id')}" }
    yield slideshow_item