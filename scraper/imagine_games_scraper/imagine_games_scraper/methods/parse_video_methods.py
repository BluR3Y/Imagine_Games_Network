import scrapy
import json
import re

from imagine_games_scraper.alchemy.models.video import Video, VideoMetadata, VideoAsset
from imagine_games_scraper.alchemy.models.content import Content


def parse_video_page(self, response, video_item = Video(), recursion_level = 0):
    # self.session.add(video_item) # questionable
    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    page_data = page_json_data['props']['pageProps']['page']
    apollo_state = page_json_data['props']['apolloState']

    modern_video_ref = apollo_state['ROOT_QUERY'].get("videoBySlug({\"slug\":\"%s\"})" % page_data.get('slug'))
    modern_video_data = page_json_data['props']['apolloState'][modern_video_ref['__ref']]

    # *********************** Parse Video Content **************************
    
    modern_content_ref = modern_video_data.get('content')
    if modern_content_ref:
        # Check if content item already exists in database
        existing_modern_content = self.session.query(Content).filter_by(legacy_id=modern_content_ref.get('id')).first()
        if existing_modern_content is None:
            # content_item = Content()
            # yield self.parse_modern_content(page_json_data, modern_content_ref, content_item)
            content_id = self.parse_modern_content(page_json_data, modern_content_ref.get('__ref'))

            video_item.content_id = content_id

    # ****************************** Parse Video Metadata *********************************

    video_meta_data = modern_video_data.get('videoMetadata')
    if video_meta_data:
        video_meta_data_item = VideoMetadata()
        video_meta_data_item.ad_breaks = video_meta_data.get('adBreaks')
        video_meta_data_item.chat_enabled = video_meta_data.get('chatEnabled')
        video_meta_data_item.description_html = video_meta_data.get('descriptionHtml')
        video_meta_data_item.downloadable = video_meta_data.get('downloadable')
        video_meta_data_item.duration = video_meta_data.get('duration')
        video_meta_data_item.m3u_url = video_meta_data.get('m3uUrl')

        video_item.metadata_id = video_meta_data_item.id
        self.session.add(video_meta_data_item)
        self.session.commit()

    # ***************************** Parsing Video Assets **********************************
    
    for asset in modern_video_data['assets']:
        asset_item = VideoAsset()
        asset_item.video_id = video_item.id
        asset_item.url = asset.get('url')
        asset_item.width = asset.get('width')
        asset_item.height = asset.get('height')
        asset_item.fps = asset.get('fps')

        self.session.add(asset_item)
        self.session.commit(asset_item)

    # ************************** Parsing similar Videos ************************************
        
    if recursion_level < 1:
        for recommendation in modern_video_data.get('recommendations'):
            video_exists = self.session.query(Video).join(Content).filter(Content.legacy_id == recommendation.get('videoId')).first is not None
            if not video_exists:
                yield scrapy.Request(url="https://www.ign.com" + recommendation.get('url'), callback=self.parse_video_page, cb_kwargs={ 'recursion_level': recursion_level + 1 })

    self.session.add(video_item)
    self.session.commit(video_item)
    yield video_item