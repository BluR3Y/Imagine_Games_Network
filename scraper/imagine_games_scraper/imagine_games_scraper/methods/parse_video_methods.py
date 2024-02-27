import scrapy
import json
import re

from imagine_games_scraper.items.video import Video, VideoMetadata, VideoAsset
from imagine_games_scraper.items.content import Content

def parse_video_page(self, response, video_item = Video(), recursion_level = 0):
    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    page_data = page_json_data['props']['pageProps']['page']
    apollo_state = page_json_data['props']['apolloState']

    modern_video_ref = apollo_state['ROOT_QUERY'].get("videoBySlug({\"slug\":\"%s\"})" % page_data.get('slug'))
    modern_video_data = page_json_data['props']['apolloState'][modern_video_ref['__ref']]

    # *********************** Parse Video Content **************************
    modern_content_ref = modern_video_data.get('content')
    if modern_content_ref:
        modern_content_item = Content()

        yield from self.parse_modern_content(page_json_data, modern_content_ref.get('__ref'), modern_content_item)
        video_item['content_id'] = modern_content_item.get('id')

    # ****************************** Parse Video Metadata *********************************
    video_metadata = modern_video_data.get('videoMetadata')
    if video_metadata:
        video_metadata_item = VideoMetadata()
        video_metadata_item['ad_breaks'] = video_metadata.get('adBreaks')
        video_metadata_item['chat_enabled'] = video_metadata.get('chatEnabled')
        video_metadata_item['description_html'] = video_metadata.get('descriptionHtml')
        video_metadata_item['downloadable'] = video_metadata.get('downloadable')
        video_metadata_item['duration'] = video_metadata.get('duration')
        video_metadata_item['m3u_url'] = video_metadata.get('m3uUrl')

        yield video_metadata_item
        video_item['metadata_id'] = video_metadata_item.get('id')

    # ***************************** Parsing Video Assets **********************************
    for asset in modern_video_data['assets']:
        asset_item = VideoAsset()
        asset_item['video_id'] = video_item.get('id')
        asset_item['url'] = asset.get('url')
        asset_item['width'] = asset.get('width')
        asset_item['height'] = asset.get('height')
        asset_item['fps'] = asset.get('fps')

        yield asset_item

    # *************************** Parsing Recommendation Content *****************************
    if recursion_level < 1:
        for recommendation in modern_video_data.get('recommendations'):
            existing_video = True   # Missing

            if existing_video is None:
                recommendation_url = 'https://www.ign.com' + recommendation['url']
                yield scrapy.Request(url=recommendation_url, callback=self.parse_video_page, cb_kwargs={ 'recursion_level': recursion_level })

    yield video_item