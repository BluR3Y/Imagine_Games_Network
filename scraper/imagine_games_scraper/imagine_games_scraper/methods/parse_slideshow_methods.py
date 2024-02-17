import scrapy
import json
import re

from imagine_games_scraper.items.misc import Gallery, Image, ImageConnection, Slideshow
from imagine_games_scraper.items.content import Content

@classmethod
def parse_slideshow_page(self, response, slideshow_item = Slideshow(), recursion_level = 0):
    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    page_data = page_json_data['props']['pageProps']['page']
    apollo_state = page_json_data['props']['apolloState']
    
    slideshow_item = Slideshow()
    slideshow_key = next((key for key in apollo_state['ROOT_QUERY'] if page_data.get('slug') in key))
    slideshow_data = apollo_state['ROOT_QUERY'].get(slideshow_key)

    modern_content_ref = slideshow_data.get('content')
    if modern_content_ref:
        modern_content_item = Content(apollo_state[modern_content_ref.get('__ref')])
        yield self.parse_modern_content(page_json_data, modern_content_ref.get('__ref'), modern_content_item)

        slideshow_item['content'] = modern_content_item.get('id')
    
    image_regex = re.compile(r"slideshowImages:{.*}")
    image_key = next((key for key in slideshow_data if image_regex.search(key)))
    if image_key:
        gallery_item = Gallery()
        for image in [apollo_state[image_ref.get('__ref')] for image_ref in slideshow_data[image_key]['images']]:
            image_item = Image(image)
            gallery_connection = ImageConnection({
                'gallery_id': gallery_item.get('id'),
                'image_id': image_item.get('id')
            })
            yield image_item
            yield gallery_connection
        yield gallery_item