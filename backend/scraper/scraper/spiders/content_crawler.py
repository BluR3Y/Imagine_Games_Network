import scrapy


class ContentCrawlerSpider(scrapy.Spider):
    name = "content_crawler"
    allowed_domains = ["ign.com"]
    start_urls = ["https://ign.com"]

    def parse(self, response):
        pass
