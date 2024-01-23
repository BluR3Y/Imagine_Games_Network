import scrapy
from imagine_games_scraper.items import Video

class VideoSpiderSpider(scrapy.Spider):
    name = "video_spider"
    allowed_domains = ["ign.com"]
    start_urls = ["https://ign.com?endIndex=0"]
    # Custom settings for the spider
    custom_settings = {
        'FEEDS': {
            'content_data.json': {
                'format': 'json',
                'overwrite': True
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
            yield scrapy.Request(url=video_url, callback=self.parse_video_page)

    def parse_video_page(self, response):
        print('lmao')