import scrapy
import json
import re

from imagine_games_scraper.items.article import Article
from imagine_games_scraper.items.video import Video

from imagine_games_scraper.methods import parse_article_methods
from imagine_games_scraper.methods import parse_video_methods
from imagine_games_scraper.methods import parse_slideshow_methods
from imagine_games_scraper.methods import shared_methods


class IgnContentSpiderSpider(scrapy.Spider):
    name = "ign_content_spider"
    allowed_domains = ["ign.com"]
    start_urls = ["https://ign.com?endIndex=0"]
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

    def start_requests(self):
        # yield scrapy.Request(url=self.start_urls[0], callback=self.parse)
        yield scrapy.Request(url='https://www.ign.com/articles/best-ipad-deals', callback=self.parse_article_page, cb_kwargs={ 'recursion_level': 1 })
        # yield scrapy.Request(url='https://www.ign.com/videos/the-finals-official-season-1-update-150-trailer', callback=self.parse_video_page, cb_kwargs={ 'recursion_level': 1 })
        # yield scrapy.Request(url='https://www.ign.com/slideshows/the-finals-review-screenshots', callback=self.parse_slideshow_page, cb_kwargs={ 'recursion_level': 1 })

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

            if item_type == "ModernArticle":
                item_content = apollo_state[item['content']['__ref']]
                article_item = Article(item)
                yield scrapy.Request(url="https://www.ign.com" + item_content.get('url'), callback=self.parse_article_page, cb_kwargs={ 'article_item': article_item , 'recursion_level': 0 })
            elif item_type == "ModernVideo":
                item_content = apollo_state[item['content']['__ref']]
                video_item = Video(item)
                yield scrapy.Request(url="https://www.ign.com" + item_content.get('url'), callback=self.parse_video_page, cb_kwargs={ 'video_item': video_item, 'recursion_level': 0 })
            elif item_type == "Promotion":
                pass
            else:
                print(item)

IgnContentSpiderSpider.parse_article_page = parse_article_methods.parse_article_page
IgnContentSpiderSpider.parse_poll = parse_article_methods.parse_poll
IgnContentSpiderSpider.parse_captioned_image = parse_article_methods.parse_captioned_image
IgnContentSpiderSpider.parse_commerce_deal = parse_article_methods.parse_commerce_deal

IgnContentSpiderSpider.parse_video_page = parse_video_methods.parse_video_page

IgnContentSpiderSpider.parse_slideshow_page = parse_slideshow_methods.parse_slideshow_page

IgnContentSpiderSpider.parse_contributor_page = shared_methods.parse_contributor_page
IgnContentSpiderSpider.parse_object_page = shared_methods.parse_object_page
IgnContentSpiderSpider.parse_modern_content = shared_methods.parse_modern_content