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
        # yield scrapy.Request(url=self.start_urls[0], callback=self.parse)
        yield scrapy.Request(url='https://www.ign.com/videos/everything-we-saw-at-ces-2024', callback=self.parse_video_page, cb_kwargs={ 'recursion_level': 1 })

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
        video_item['metadata'] = {
            'duration': video_metadata['duration'],
            'description_html': video_metadata['descriptionHtml'],
            'm3u': video_metadata['m3uUrl']
        }
        video_item['objects'] = self.parse_video_primary_object(page_json_data)

        video_item['contributors'] = [{
            'legacy_id': contributor['id'],
            'name': contributor['name'],
            'nickname': contributor['nickname']
        } for contributor in page_data['contentForGA']['contributors']]

        video_item['assets'] = [{
            'url': asset['url'],
            'width': asset['width'],
            'height': asset['height'],
            'fps': asset['fps']
        } for asset in page_data['video']['assets']]

        video_item['recommendations'] = [{
            'duration': recommendation['duration'],
            'title': recommendation['title'],
            'url': recommendation['url'],
            'legacy_id': recommendation['videoId'],
            'thumbnail': recommendation['thumbnailUrl'],
            'slug': recommendation['slug']
        } for recommendation in page_data['video']['recommendations']]

        if recursion_level < 1:
            for recommendation in page_data['video']['recommendations']:
                recommendation_url = 'https://www.ign.com' + recommendation['url']
                yield scrapy.Request(url=recommendation_url, callback=self.parse_video_page, cb_kwargs={ 'recursion_level': recursion_level + 1 })

        # Yielding the Video Item for further processing or storage
        yield video_item

    def parse_video_primary_object(self, page_json_data):
        parsed_objects = []

        for object_id in page_json_data['props']['pageProps']['page']['additionalDataLayer']['content']['objectIds']:
            object_data = page_json_data['props']['apolloState'][f'Object:{object_id}']

            parsed_objects.append({
                'legacy_id': object_data.get('id'),
                'url': object_data.get('url'),
                'slug': object_data.get('slug'),
                'type': object_data.get('type'),
                'cover': object_data['primaryImage'].get('url'),
                'names': {
                    'primary': object_data['metadata']['names'].get('name'),
                    'alt': object_data['metadata']['names'].get('alt'),
                    'short': object_data['metadata']['names'].get('short')
                },
                'descriptions': {
                    'long': object_data['metadata']['descriptions'].get('long'),
                    'short': object_data['metadata']['descriptions'].get('short')
                },
                'franchises': [{
                    'name': franchise.get('name'),
                    'slug': franchise.get('slug')
                } for franchise in object_data['franchises']],
                'genres': [{
                    'name': genre.get('name'),
                    'slug': genre.get('slug')
                } for genre in object_data['genres']],
                'features': [{
                    'name': feature.get('name'),
                    'slug': feature.get('slug')
                } for feature in object_data['features']],
                'producers': [{
                    'name': producer.get('name'),
                    'short_name': producer.get('shortName'),
                    'slug': producer.get('slug')
                } for producer in object_data['producers']],
                'publishers': [{
                    'name': publisher.get('name'),
                    'short_name': publisher.get('shortName'),
                    'slug': publisher.get('slug')
                } for publisher in object_data['publishers']],
                'regions': self.parse_object_regions(page_json_data, [region['__ref'] for region in object_data['objectRegions']])
            })
        return parsed_objects
    
    def parse_object_regions(self, page_json_data, region_keys):
        parsed_regions = []

        for region_key in region_keys:
            region_object = page_json_data['props']['apolloState'][region_key]
            region_rating_ref = region_object['ageRating']['__ref'] if region_object.get('ageRating') else None
            region_rating_object = page_json_data['props']['apolloState'].get(region_rating_ref)

            parsed_region_object = {
                'legacy_id': region_object.get('id'),
                'name': region_object.get('name'),
                'region': region_object.get('region'),
                'releases': [],
                **({
                    'age_rating': {
                        'legacy_id': region_rating_object['id'],
                        'name': region_rating_object['name'],
                        'slug': region_rating_object['slug'],
                        'type': region_rating_object['ageRatingType'],
                        'descriptors': [descriptor['name'] for descriptor in region_object['ageRatingDescriptors']]
                    }
                } if region_rating_ref is not None else {})
            }
            for region_release_key in [release['__ref'] for release in region_object['releases']]:
                region_release_object = page_json_data['props']['apolloState'][region_release_key]
                parsed_region_released_object = {
                    'legacy_id': region_release_object.get('id'),
                    'date': region_release_object.get('date'),
                    'platform_attributes': []
                }
                for release_platform_key in region_release_object['platformAttributes']:
                    release_platform_object = page_json_data['props']['apolloState'][release_platform_key['__ref']]
                    parsed_region_released_object['platform_attributes'].append({
                        'legacy_id': release_platform_object.get('id'),
                        'name': release_platform_object.get('name')
                    })
                parsed_region_object['releases'].append(parsed_region_released_object)
            parsed_regions.append(parsed_region_object)
        return parsed_regions