import scrapy
import json
import re
import psycopg2
from scrapy.utils.project import get_project_settings
from urllib import parse

from imagine_games_scraper.methods import parse_video_methods
from imagine_games_scraper.methods import shared_methods

class IgnContentSpiderSpider(scrapy.Spider):
    name = "ign_content_spider"
    allowed_domains = ["ign.com"]
    start_urls = ["https://ign.com?endIndex=10"]
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
        },
        # Delay between consecutive requests to same domain (seconds)
        'DOWNLOAD_DELAY': 3
    }

    # Initialize the spider
    def __init__(self, *args, **kwargs):
        super(IgnContentSpiderSpider, self).__init__(*args, **kwargs)
        settings = get_project_settings()
        # Establish a connection to Postgres Database
        self.connection = psycopg2.connect(
            database = settings.get('POSTGRES_DATABASE'),
            user = settings.get('POSTGRES_ACCESS_USER'),
            password = settings.get('POSTGRES_ACCESS_PASSWORD'),
            host = settings.get('POSTGRES_HOST'),
            port = settings.get('POSTGRES_PORT')
        )
        self.cursor = self.connection.cursor()

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)
        # yield scrapy.Request(url='https://www.ign.com/articles/the-last-of-us-part-2-review', callback=self.parse_article_page, cb_kwargs={ 'recursion_level': 1 })
        # yield scrapy.Request(url='https://www.ign.com/videos/the-finals-official-season-1-update-150-trailer', callback=self.parse_video_page, cb_kwargs={ 'recursion_level': 1 })
        # yield scrapy.Request(url='https://www.ign.com/slideshows/the-finals-review-screenshots', callback=self.parse_slideshow_page, cb_kwargs={ 'recursion_level': 1 })
        # yield scrapy.Request(url="https://www.ign.com/wikis/fortnite", callback=self.parse_wiki_page, cb_kwargs={ 'recursion_level': 1 })

    def parse(self, response):
        page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
        page_json_data = json.loads(page_script_data)

        page_data = page_json_data['props']['pageProps']['page']
        apollo_state = page_json_data['props']['apolloState']

        homepage_ref = apollo_state['ROOT_QUERY'].get('homepage')
        homepage_data = apollo_state[homepage_ref.get('__ref')]

        content_regex = re.compile(r"contentFeed:{.*}")
        content_feed_key = next((key for key in homepage_data if content_regex.search(key)), None)
        feed_refs = homepage_data[content_feed_key]['feedItems']

        for item in [apollo_state[item_ref.get('__ref')] for item_ref in feed_refs]:
            item_type = item.get('__typename')

            if item_type == "ModernVideo":
                item_content = apollo_state[item['content']['__ref']]

                existing_video = self.cursor.execute("""
                    SELECT videos.*
                    FROM videos
                    INNER JOIN contents
                        ON videos.content_id = contents.id
                    WHERE contents.id = %s
                """, (item_content.get('id'),))
                
                if existing_video is None:
                    yield scrapy.Request(url="https://www.ign.com" + item_content.get('url'), callback=self.parse_video_page, cb_kwargs={ 'recursion_level': 0 })
            elif item_type == "ModernArticle":
                continue
                item_content = apollo_state[item['content']['__ref']]
                existing_article = self.cursor.execute("""
                    SELECT article.*
                    FROM articles
                    INNER JOIN contents
                        ON articles.content_id = contents.id
                    WHERE contents.id = %s
                """, (item_content.get('id'),))

                if existing_article is None:
                    yield scrapy.Request(url="https://www.ign.com" + item_content.get('url'), callback=self.parse_article_page, cb_kwargs={ 'recursion_level': 0 })
            elif item_type == "Promotion":
                pass

IgnContentSpiderSpider.parse_video_page = parse_video_methods.parse_video_page

IgnContentSpiderSpider.parse_modern_content = shared_methods.parse_modern_content
IgnContentSpiderSpider.parse_contributor_page = shared_methods.parse_contributor_page
IgnContentSpiderSpider.parse_object_page = shared_methods.parse_object_page