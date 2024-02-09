import pymongo
import urllib.parse
from imagine_games_scraper.items.article import Article
from imagine_games_scraper.items.video import Video
from imagine_games_scraper.items.user import Contributor
from imagine_games_scraper.items.object import Object

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ImagineGamesScraperPipeline:
    def process_item(self, item, spider):
        if isinstance(item, Article):
            print('****** Article ******')
        elif isinstance(item, Video):
            print('******* Video *******')
        elif isinstance(item, Contributor):
            print('******* Contributor *******')
        elif isinstance(item, Object):
            print('********** Object ***************')
        else: print(f'******** {type(item)} ************')
        return item

class MongoStore:
    # Method used to retrieve settings from Scrapy project settings
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        # Establish a connection to the MongoDB database
        self.mongo_uri = f"mongodb://{settings.get('MONGO_USER')}:{urllib.parse.quote_plus(settings.get('MONGO_PASSWORD'))}@{settings.get('MONGO_HOST')}:{settings.get('MONGO_PORT')}"
        self.mongo_db = settings.get('MONGO_DATABASE')
        print(self.mongo_uri)

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        # Close connection to database when the spider is closed
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, Article):
            print('****** Article ******')
        elif isinstance(item, Video):
            print('******* Video *******')
        elif isinstance(item, Contributor):
            print('******* Reporter *******')
        else: print('******** other ************')
        return item