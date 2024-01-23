import scrapy


class WikiSpiderSpider(scrapy.Spider):
    name = "wiki_spider"
    allowed_domains = ["ign.com"]
    start_urls = ["https://ign.com"]

    def parse(self, response):
        pass
