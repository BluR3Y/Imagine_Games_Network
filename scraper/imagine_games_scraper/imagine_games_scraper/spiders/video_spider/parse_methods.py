import scrapy
import json
from imagine_games_scraper.items.video import Video
from imagine_games_scraper.items.misc import Image


@classmethod
def parse_video_page(self, response, recursion_level = 0):
    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    page_data = page_json_data['props']['pageProps']['page']
    apollo_state = page_json_data['props']['apolloState']

    modern_video_ref = apollo_state['ROOT_QUERY'].get("videoBySlug({\"slug\":\"%s\"})" % page_data.get('slug'))
    modern_video_data = page_json_data['props']['apolloState'][modern_video_ref['__ref']]
    
    # video_content_item = self.parse_video_content(page_json_data, modern_video_data['content']['__ref'])
    # *********************** Parse Video Content **************************
    video_content_data = apollo_state[modern_video_data['content']['__ref']]
    # Last Here