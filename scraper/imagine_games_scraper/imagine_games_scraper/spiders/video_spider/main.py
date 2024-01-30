import scrapy
from dotenv import dotenv_values
from . import parse_methods

class VideoSpiderSpider(scrapy.Spider):
    name = "video_spider"
    allowed_domains = ["ign.com"]
    start_urls = ["https://ign.com/videos?endIndex=0"]
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
            yield scrapy.Request(url=video_url, callback=self.parse_video_page, cb_kwargs={ 'recursion_level': 1 })

VideoSpiderSpider.parse_video_page = parse_methods.parse_video_page
VideoSpiderSpider.parse_video_primary_object = parse_methods.parse_video_primary_object
VideoSpiderSpider.parse_object_regions = parse_methods.parse_object_regions