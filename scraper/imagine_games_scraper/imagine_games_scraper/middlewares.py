# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class ImagineGamesScraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ImagineGamesScraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

from urllib.parse import urlencode
from random import randint
import requests

# Middleware for dynamically assigning fake brwoser headers to requests
class ScrapeOpsFakeBrowserHeaderAgentMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    
    def __init__(self, settings):
        # Retrieve settings from Scrapy project settings
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT', 'http://headers.scrapeops.io/v1/browser-headers?')
        self.scrapeops_fake_browser_headers_active = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED', True)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        # List to store fetched browser headers
        self.headers_list = []
        # Initialize middleware
        self._get_headers_list()
        self._scrapeops_fake_browser_headers_enabled()

    def _get_headers_list(self):
        # Fetch browser headers from ScrapeOps API
        payload = { 'api_key': self.scrapeops_api_key }
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results 
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.headers_list = json_response.get('result', [])

    def _get_random_browser_header(self):
        # Get a random set of browser headers from the fetched list
        random_index = randint(0, len(self.headers_list) - 1)
        return self.headers_list[random_index]
    
    def _scrapeops_fake_browser_headers_enabled(self):
        # Check if ScrapeOps fake browser headers are enabled based on settings
        if self.scrapeops_api_key is None or self.scrapeops_api_key == '' or self.scrapeops_fake_browser_headers_active == False:
            self.scrapeops_fake_browser_headers_active = False
        else:
            self.scrapeops_fake_browser_headers_active = True
    
    def process_request(self, request, spider):
        # Assign a random set of browser headers to the request
        random_browser_header = self._get_random_browser_header()

        # Set individual headers in the request
        # request.headers['connection'] = "keep-alive"
        # request.headers['cache-control'] = "max-age=0"
        request.headers['sec-ch-ua'] = random_browser_header['sec-ch-ua']
        request.headers['sec-ch-ua-mobile'] = random_browser_header['sec-ch-ua-mobile']
        request.headers['sec-ch-ua-platform'] = random_browser_header['sec-ch-ua-platform']
        request.headers['upgrade-insecure-requests'] =random_browser_header['upgrade-insecure-requests']
        request.headers['user-agent'] = random_browser_header['user-agent']
        request.headers['accept'] = random_browser_header['accept']
        request.headers['sec-fetch-site'] = random_browser_header['sec-fetch-site']
        request.headers['sec-fetch-mode'] = random_browser_header['sec-fetch-mod']
        request.headers['sec-fetch-user'] = random_browser_header['sec-fetch-user']
        # request.headers['sec-fetch-dest'] = "document"
        request.headers['accept-encoding'] = random_browser_header['accept-encoding']
        request.headers['accept-language'] = random_browser_header['accept-language']

import base64

# Middleware used to set proxy routes to request
class MyProxyMiddleware(object):
    @classmethod
    # This method is called when creating an instance of the middleware
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    
    # Constructor initializes the middleware with proxy-related settings.
    # * __init__ is a method that closely behaves as a default constructor in C++
    def __init__(self, settings):
        # Retrieve proxy settings from Scrapy settings file
        self.user = settings.get('PROXY_USER')
        self.password = settings.get('PROXY_PASSWORD')
        self.protocol = settings.get('PROXY_PROTOCOL')
        self.endpoint = settings.get('PROXY_ENDPOINT')
        self.port = settings.get('PROXY_PORT')

    # This method is called for each request made by the spider
    def process_request(self, request, spider):
        # Create a basic authentication string using the provided username and password
        user_credentials = '{user}:{passw}'.format(user=self.user, passw=self.password)
        basic_authentication = 'Basic ' + base64.b64encode(user_credentials.encode()).decode()
        # Construct the proxy endpoint URL using the specified endpoint and port
        host = '{protocol}://{endpoint}:{port}'.format(protocol=self.protocol, endpoint=self.endpoint, port=self.port)
        # Set the proxy and add the Proxy-Authorization header to the request
        request.meta['proxy'] = host
        # request.headers['Proxy-Authorization'] = basic_authentication