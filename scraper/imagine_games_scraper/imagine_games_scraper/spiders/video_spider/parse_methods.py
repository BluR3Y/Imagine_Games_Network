import scrapy
import json
import re

from imagine_games_scraper.items.video import Video, VideoMetadata, VideoAsset
from imagine_games_scraper.items.misc import Image
from imagine_games_scraper.items.user import User, Contributor
from imagine_games_scraper.items.content import Content, ContentCategory, Attribute, TypedAttribute, Brand
from imagine_games_scraper.items.object import Object


@classmethod
def parse_video_page(self, response, recursion_level = 0):
    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    page_data = page_json_data['props']['pageProps']['page']
    apollo_state = page_json_data['props']['apolloState']

    modern_video_ref = apollo_state['ROOT_QUERY'].get("videoBySlug({\"slug\":\"%s\"})" % page_data.get('slug'))
    modern_video_data = page_json_data['props']['apolloState'][modern_video_ref['__ref']]
    modern_video_item = Video()

    # *********************** Parse Video Content **************************
    video_content_data = apollo_state[modern_video_data['content']['__ref']]
    content_item = Content(video_content_data)

    content_feed_image = Image(video_content_data.get('feedImage'))
    content_item['feed_cover'] = content_feed_image.get('id')
    yield content_feed_image

    content_category_item = ContentCategory(video_content_data.get('contentCategory'))
    content_item['category'] = content_category_item.get('id')
    yield content_category_item

    primary_object_item = Object(apollo_state[video_content_data['primaryObject']['__ref']])
    content_item['primary_object'] = primary_object_item.get('id')
    yield scrapy.Request(url="https://www.ign.com" + primary_object_item.get('url'), callback=self.parse_object_page, cb_kwargs={ 'object_item': primary_object_item })

    brand = video_content_data.get('brand')
    if brand:
        brand_item = Brand(brand)
        content_item['brand'] = brand_item.get('id')
        yield brand_item

    for attribute in video_content_data.get('attributes'):
        attribute_item = Attribute(attribute)
        typed_attribute_item = TypedAttribute({
            'type': attribute.get('type'),
            'attribute': attribute_item.get('id')
        })
        content_item['attributes'].append(typed_attribute_item.get('id'))
        yield attribute_item, typed_attribute_item


    for contributor in [apollo_state[user_ref['__ref']] for user_ref in video_content_data.get('contributorsOrBylines')]:
        contributor_url = '/person/' + contributor.get('nickname')
        contributor_info = Contributor({ 'url': contributor_url })
        user_info = User(contributor, { 'contributor': contributor_info.get('id') })
        content_item['contributors'].append(user_info.get('id'))

        yield user_info
        yield scrapy.Request(url="https://www.ign.com" + contributor_info.get('url'), callback=self.parse_contributor_page, cb_kwargs={ 'contributor_item': contributor_info })

    modern_video_item['content'] = content_item.get('id')
    yield content_item

    # ****************************** Parse Video Metadata *********************************
    video_meta_data_item = VideoMetadata(modern_video_data['videoMetadata'])
    modern_video_item['metadata'] = video_meta_data_item.get('id')
    yield video_meta_data_item

    # ***************************** Parsing Video Assets **********************************
    for asset in modern_video_data['assets']:
        asset_item = VideoAsset(asset)
        modern_video_item['assets'].append(asset_item.get('id'))
        yield asset_item

    if recursion_level < 1:
        for recommendation in modern_video_data.get('recommendations'):
            recommendation_url = 'https://www.ign.com' + recommendation['url']
            yield scrapy.Request(url=recommendation_url, callback=self.parse_video_page, cb_kwargs={ 'recursion_level': recursion_level })

    yield modern_video_item