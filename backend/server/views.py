from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from scrapy.utils.log import configure_logging
from scraper.scraper.spiders.content_crawler import ContentCrawlerSpider

# Create your views here.
def say_hello(request):
    return HttpResponse('Hello World!')

def test_crawler(request):
    url = request.GET.get('url')
    if not url:
        return JsonResponse({'error': 'URL parameter is required'}, status=400)
    
    # Configure Scrapy loggin
    configure_logging()

    # Run the Scrapy Spider
    process = CrawlerProcess(get_project_settings())
    process.crawl(ContentCrawlerSpider, url="https://www.ign.com")
    process.start(stop_after_crawl=False)

    # Stop the Twisted reactor if it's running
    if reactor.running:
        reactor.stop()

    return JsonResponse({'status': 'Spider started for URL'})