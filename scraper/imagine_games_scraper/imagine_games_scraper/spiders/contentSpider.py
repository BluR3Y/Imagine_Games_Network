import scrapy
from imagine_games_scraper.items import Article, Video


class ContentspiderSpider(scrapy.Spider):
    name = "contentSpider"
    allowed_domains = ["ign.com"]
    start_urls = ["https://ign.com/news?endIndex=10"]
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

    # Last Here **
    def identify_category(self, response):
        valid_categories = ['games', 'movies', 'tv', 'comics', 'tech']
        
        first_category_identification_attempt = response.xpath("//meta[@name='vertical']/@content").getall()
        for vertical in first_category_identification_attempt:
            if vertical in valid_categories:
                return vertical
            
        second_category_identification_attempt = response.css("div.card.box.object-box a.title5 ::attr(href)").get()
        return second_category_identification_attempt if second_category_identification_attempt in valid_categories else 'unknown'

    # Main parse function for the spider
    def parse(self, response):
        # Extracting content elements from the response
        page_content = response.css('div.content-item')

        # Iterate over each content element
        for content_item in page_content:
            # Construct absolute URL of the item
            item_url = 'https://www.ign.com' + content_item.css('a.item-body ::attr(href)').get()
            # Determine the appropriate callback function based on the type of content
            callback_function = self.parse_article_page if 'video' not in item_url else self.parse_video_page
            # Following the link to the content's page and calling parsing function
            yield scrapy.Request(url=item_url, callback=callback_function)
        
    # Parsing function for article pages
    def parse_article_page(self, response):
        # Creating an Article instance to store the scraped data
        article_item = Article({ 'url': response.url })

        # Populating the item fields with scraped data
        article_item['thumbnail'] = response.xpath("//meta[@property='og:image']/@content").get()
        article_item['headline'] = response.xpath("//h1[@data-cy='article-headline']/text()").get()
        article_item['sub_headline'] = response.xpath("//h2[@data-cy='article-sub-headline']/text()").get()
        article_item['reporter'] = response.xpath("//meta[@property='article:author']/@content").get(),
        article_item['published_date'] = response.xpath("//meta[@property='article:published_time']/@content").get()
        article_item['modified_date'] = response.xpath("//meta[@property='article:modified_time']/@content").get()
        article_item['tags'] = response.xpath("//a[@data-cy='object-breadcrumb']/text()").getall()
        article_item['category'] = self.identify_category(response)

        print(article_item)

    # Parsing function for video pages
    def parse_video_page(self, response):
        pass