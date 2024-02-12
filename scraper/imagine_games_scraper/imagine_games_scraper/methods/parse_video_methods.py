import scrapy
import json
import re

from imagine_games_scraper.items.video import Video, VideoMetadata, VideoAsset
from imagine_games_scraper.items.misc import Image
from imagine_games_scraper.items.user import User, Author
from imagine_games_scraper.items.content import Content, ContentCategory, Attribute, TypedAttribute, Brand
from imagine_games_scraper.items.object import Object


@classmethod
def parse_video_page(self, response, video_item = Video(), recursion_level = 0):
    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    page_data = page_json_data['props']['pageProps']['page']
    apollo_state = page_json_data['props']['apolloState']

    modern_video_ref = apollo_state['ROOT_QUERY'].get("videoBySlug({\"slug\":\"%s\"})" % page_data.get('slug'))
    modern_video_data = page_json_data['props']['apolloState'][modern_video_ref['__ref']]

    # *********************** Parse Video Content **************************

    modern_content_ref = apollo_state.get('content')
    if modern_content_ref:
        content_item = Content(apollo_state[modern_content_ref.get('__ref')])
        yield self.parse_modern_content(page_json_data, modern_content_ref, content_item)

        video_item['content'] = content_item.get('id')

    # ****************************** Parse Video Metadata *********************************
    video_meta_data = modern_video_data.get('videoMetadata')
    if video_meta_data:
        video_meta_data_item = VideoMetadata(video_meta_data)
        video_item['metadata'] = video_meta_data_item.get('id')
        yield video_meta_data_item

    # ***************************** Parsing Video Assets **********************************
    for asset in modern_video_data['assets']:
        asset_item = VideoAsset(asset)
        video_item['assets'].append(asset_item.get('id'))
        yield asset_item

    if recursion_level < 1:
        for recommendation in modern_video_data.get('recommendations'):
            recommendation_url = 'https://www.ign.com' + recommendation['url']
            yield scrapy.Request(url=recommendation_url, callback=self.parse_video_page, cb_kwargs={ 'recursion_level': recursion_level })

    yield video_item