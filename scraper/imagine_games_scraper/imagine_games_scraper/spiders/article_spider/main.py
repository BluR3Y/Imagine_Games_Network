import scrapy
from dotenv import dotenv_values
from . import parse_methods

class ArticleSpiderSpider(scrapy.Spider):
    name = "article_spider"
    allowed_domains = ["ign.com"]
    start_urls = ["https://ign.com/news?endIndex=0"]
    # Custom settings for the spider
    custom_settings = {
        'FEEDS': {
            'article_data.json': {
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
        yield scrapy.Request(url='https://www.ign.com/articles/the-last-of-us-part-2-review', callback=self.parse_article_page, cb_kwargs={ 'recursion_level': 1 })

    def parse(self, response):
        # Extracting article content elements from the response
        article_content = response.xpath(
            # Search for a <div> element whose's class attribute contains "content-item"
            "//div[contains(@class, 'content-item')]" + 
            # From those previous elements, select those that have a child of type <a> with an href attribute that includes "/articles/"
            "/a[contains(@href, '/articles/')]" + 
            # From the previous elements, provide the ancestor element of type <div> whose class attribute contains 'content-item'
            "/ancestor::div[contains(@class, 'content-item')]"
        )

        # Iterate over each content element
        for article in article_content:
            article_uri = article.css('a.item-body ::attr(href)').get()
            article_url = 'https://www.ign.com' + article_uri

            # Following the link to the content's page and calling parsing function
            yield scrapy.Request(url=article_url, callback=self.parse_article_page, cb_kwargs={ 'recursion_level': 0 })

ArticleSpiderSpider.parse_article_page = parse_methods.parse_article_page
ArticleSpiderSpider.parse_article_objects = parse_methods.parse_article_objects
ArticleSpiderSpider.parse_html_content = parse_methods.parse_html_content
ArticleSpiderSpider.parse_article_contributors = parse_methods.parse_article_contributors
ArticleSpiderSpider.parse_object_regions = parse_methods.parse_object_regions
ArticleSpiderSpider.parse_article_recommendations = parse_methods.parse_article_recommendations
ArticleSpiderSpider.parse_article_slideshows = parse_methods.parse_article_slideshows
ArticleSpiderSpider.parse_object_wiki = parse_methods.parse_object_wiki
ArticleSpiderSpider.parse_object_polls = parse_methods.parse_object_polls