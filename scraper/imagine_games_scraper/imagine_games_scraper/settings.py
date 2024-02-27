import os
from dotenv import dotenv_values

env = os.environ.get("PYTHON_ENV")
environment_variables = os.environ if env == "production" else dotenv_values("../../../env/scraper/.env.development")

# ScrapeOps Credentials (Fake Browser Header API)
SCRAPEOPS_API_KEY = environment_variables.get("SCRAPEOPS_API_KEY")
SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = environment_variables.get("SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT")
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = environment_variables.get("SCRAPEOPS_FAKE_USER_AGENT_ENABLED")
SCRAPEOPS_NUM_RESULTS = environment_variables.get("SCRAPEOPS_NUM_RESULTS")

# Bright Data Credentials (Rotating/Backconnect Proxies)
PROXY_USER = environment_variables.get("PROXY_USER")
PROXY_PASSWORD = environment_variables.get("PROXY_PASSWORD")
PROXY_PROTOCOL = environment_variables.get("PROXY_PROTOCOL")
PROXY_ENDPOINT = environment_variables.get("PROXY_ENDPOINT")
PROXY_PORT = environment_variables.get("PROXY_PORT")

# Postgres Database Credentials
POSTGRES_HOST = environment_variables.get("POSTGRES_HOST")
POSTGRES_PORT = environment_variables.get("POSTGRES_PORT")
POSTGRES_DATABASE = environment_variables.get("POSTGRES_DATABASE")
POSTGRES_ACCESS_USER = environment_variables.get("POSTGRES_ACCESS_USER")
POSTGRES_ACCESS_PASSWORD = environment_variables.get("POSTGRES_ACCESS_PASSWORD")

# Redis Database Credentials
REDIS_HOST = environment_variables.get('REDIS_HOST')
REDIS_PORT = environment_variables.get('REDIS_PORT')
REDIS_ACCESS_PASSWORD = environment_variables.get('REDIS_ACCESS_PASSWORD')

# AWS Credentials
AWS_ACCESS_KEY = environment_variables.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = environment_variables.get("AWS_SECRET_KEY")
AWS_BUCKET = environment_variables.get("AWS_BUCKET")
AWS_REGION = environment_variables.get("AWS_REGION")
AWS_ENDPOINT = environment_variables.get("AWS_ENDPOINT")

# Scrapy settings for imagine_games_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "imagine_games_scraper"

SPIDER_MODULES = ["imagine_games_scraper.spiders"]
NEWSPIDER_MODULE = "imagine_games_scraper.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "imagine_games_scraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure Rotating/Backconnect Proxies
# ROTATING_PROXY_LIST = []
# ROTATING_PROXY_LIST_PATH = '/my/path/proxies.txt'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "imagine_games_scraper.middlewares.ImagineGamesScraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   "imagine_games_scraper.middlewares.ImagineGamesScraperDownloaderMiddleware": 543,
   "imagine_games_scraper.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware": 400,
#    "imagine_games_scraper.middlewares.MyProxyMiddleware": 350
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "imagine_games_scraper.pipelines.ImagineGamesScraperPipeline": 300,
    "imagine_games_scraper.pipelines.RedisStore": 400,
    # "imagine_games_scraper.pipelines.PostgresStore": 500
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
