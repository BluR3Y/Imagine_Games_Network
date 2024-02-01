import scrapy
import json
from imagine_games_scraper.items import Video

@classmethod
def parse_video_page(self, response, recursion_level = 0):
    # Creating a Video item instance to store the scraped data
    video_item = Video({ 'url': response.url })

    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    # Selection of page meta data from json object
    page_data = page_json_data['props']['pageProps']['page']
    video_data = page_json_data['props']['apolloState'][f'ModernContent:{page_data['videoId']}']
    video_metadata = page_data['video']['videoMetadata']

    video_item['legacy_id'] = page_data['videoId']
    video_item['description'] = page_data['description']
    video_item['slug'] = page_data['slug']
    video_item['category'] = page_data['category']
    video_item['vertical'] = page_data['vertical']
    video_item['publish_date'] = video_data['publishDate']
    video_item['modify_date'] = video_data['updatedAt']
    video_item['title'] = video_data['title']
    video_item['subtitle'] = video_data['subtitle']
    video_item['thumbnail'] = video_data['feedImage']['url']
    video_item['brand'] = video_data['brand']
    video_item['events'] = video_data['events']
    video_item['contributors'] = []
    video_item['objects'] = []
    video_item['metadata'] = {
        'duration': video_metadata['duration'],
        'description_html': video_metadata['descriptionHtml'],
        'm3u': video_metadata['m3uUrl']
    }

    for object_key in page_json_data['props']['pageProps']['page']['additionalDataLayer']['content']['objectIds']:
        object_data = page_json_data['props']['apolloState'][f'Object:{object_key}']
        video_item['objects'].append(object_data['id'])
        yield scrapy.Request(url="https://www.ign.com" + object_data['url'], callback=self.parse_object_page)

    for contributor in page_data['contentForGA']['contributors']:
        uri = "/person/" + contributor['nickname']
        video_item['contributors'].append(contributor['id'])
        yield scrapy.Request(url="https://www.ign.com" + uri, callback=self.parse_contributor_page)

    video_item['assets'] = [{
        'url': asset['url'],
        'width': asset['width'],
        'height': asset['height'],
        'fps': asset['fps']
    } for asset in page_data['video']['assets']]

    if recursion_level < 1:
        for recommendation in page_data['video']['recommendations']:
            recommendation_url = 'https://www.ign.com' + recommendation['url']
            yield scrapy.Request(url=recommendation_url, callback=self.parse_video_page, cb_kwargs={ 'recursion_level': recursion_level + 1 })

    # Yielding the Video Item for further processing or storage
    yield video_item