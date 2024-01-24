import scrapy
import json
from imagine_games_scraper.items import Video

class VideoSpiderSpider(scrapy.Spider):
    name = "video_spider"
    allowed_domains = ["ign.com"]
    start_urls = ["https://ign.com/videos?endIndex=61"]
    # Custom settings for the spider
    custom_settings = {
        'FEEDS': {
            'video_data.json': {
                'format': 'json',
                'encoding': 'utf8',
                'overwrite': True,
                'store_empty': False,
                'indent': 4
            }
        }
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):
        # Extracting video content elements from the response
        video_content = response.xpath(
            # Search for a <div> element whose's class attribute contains "content-item"
            "//div[contains(@class, 'content-item')]" + 
            # From those previous elements, select those that have a child of type <a> with an href attribute that includes "/videos/"
            "/a[contains(@href, '/videos/')]" + 
            # From the previous elements, provide the ancestor element of type <div> whose class attribute contains 'content-item'
            "/ancestor::div[contains(@class, 'content-item')]"
        )

        # Iterate over each content element
        for video in video_content:
            video_uri = video.css('a.item-body ::attr(href)').get()
            video_url = 'https://www.ign.com' + video_uri

            # Following the link to the content's page and calling parsing function
            # Pass a callback argument called "recursive_level" whose value indicates the level of recursion each request has created and prevent extensive scraping
            yield scrapy.Request(url=video_url, callback=self.parse_video_page, cb_kwargs={ 'recursion_level': 0 })

    def parse_video_page(self, response, recursion_level = 0):
        # Creating a Video item instance to store the scraped data
        video_item = Video({ 'url': response.url })

        page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
        page_json_data = json.loads(page_script_data)
        
        # Selection of page meta data from json object
        page_data = page_json_data['props']['pageProps']['page']
        video_item['thumbnail'] = page_data['image']
        video_item['title'] = page_data['title']
        video_item['description'] = page_data['description']
        video_item['slug'] = page_data['slug']
        video_item['published_date'] = page_data['publishDate']
        video_item['category'] = page_data['category']
        video_item['duration'] = page_data['video']['videoMetadata']['duration']
        video_item['vertical'] = page_data['vertical']
        video_item['contributors'] = [{
            'name': contributor['name'],
            'nickname': contributor['nickname']
        } for contributor in page_data['contentForGA']['contributors']]

        # Selection of object data from json object
        object_data = page_data['contentForGA']['primaryObject']
        object_id = object_data['id']
        additional_object_data = page_json_data['props']['apolloState'][f'Object:{object_id}']
        video_item['object'] = {
            'url': object_data['url'],
            'slug': object_data['slug'],
            'type': object_data['type'],
            'platforms': page_data['platforms'],
            'names': {
                'primary': object_data['metadata']['names']['name'],
                'alt': object_data['metadata']['names']['alt'],
                'short': object_data['metadata']['names']['short']
            },
            'franchise': [{ 'name': franchise['name'], 'slug': franchise['slug'] } for franchise in additional_object_data['franchises']],
            'features': [{ 'name': feature['name'], 'slug': feature['slug'] } for feature in additional_object_data['features']],
            'genres': [{ 'name': genre['name'], 'slug': genre['slug'] } for genre in additional_object_data['genres']],
            'producers':[{ 'name': producer['name'], 'slug': producer['slug'] } for producer in  additional_object_data['producers']],
            'publishers': [{ 'name': publisher['name'], 'slug': publisher['slug'] } for publisher in additional_object_data['publishers']]
        }

        # Selection of video assets from json object
        video_assets = page_data['video']['assets']
        video_asset_keys = ['url', 'width', 'height', 'fps']
        # Loop through every dictionary in video_assets and extract every key=value pair whose's key appears in video_asset_keys
            # which will be stored in a list
        video_item['assets'] = [{ key: asset[key] for key in video_asset_keys } for asset in video_assets]

        if recursion_level < 1:
            for recommendation in page_data['video']['recommendations']:
                recommendation_url = 'https://www.ign.com' + recommendation['url']
                yield scrapy.Request(url=recommendation_url, callback=self.parse_video_page, cb_kwargs={ 'recursion_level': recursion_level + 1 })

        # Yielding the Video Item for further processing or storage
        yield video_item