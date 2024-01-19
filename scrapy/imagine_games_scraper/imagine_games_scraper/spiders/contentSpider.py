import scrapy
from imagine_games_scraper.items import Article, Video

class ContentspiderSpider(scrapy.Spider):
    name = "contentSpider"
    allowed_domains = ["ign.com", "proxy.scrapeops.io"]
    start_urls = ["https://www.ign.com/news?endIndex=0"]
    custom_settings = {
        'FEEDS': {
            'contentdata.json': {
                'format': 'json',
                'overwrite': True
            }
        }
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    # Main parse function for the spider
    def parse(self, response):
        # Extracting content elements from the response
        content = response.css('div.content-item')

        # Iterate over each content item
        for contentItem in content:
            # Construct absolute URL of the item
            item_url = 'https://www.ign.com' + contentItem.css('a ::attr(href)').get()
            # Determine the appropraite callback function based on the type of content
            callback_function = self.parse_article_page if 'video' not in item_url else self.parse_video_page
            # Following the link to the content's page and calling parsing function
            yield scrapy.Request(url=item_url, callback=callback_function)
            # Debugging
            return

    # Parsing function for article pages
    def parse_article_page(self, response):
        # Creating an Article instance to store the scraped data
        article_item = Article({ 'url': response.url })
        
        # Populating the item instance fields with scraped data
        page_header = response.css('div.page-header.page-content')
        article_item['content_type'] = 
        article_item['content_category'] = 
        article_item['headline'] = page_header.css('h1.display-title ::text').get()
        article_item['sub_headline'] = page_header.css('')

        print(article_item)

    # Parsing function for video pages
    def parse_video_page(self, response):
        video_item = Video()