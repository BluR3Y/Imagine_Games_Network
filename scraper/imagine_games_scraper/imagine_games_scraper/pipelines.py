import psycopg2
import redis

from urllib import parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from imagine_games_scraper.alchemy.models.video import Video
from .alchemy.models.video import Video

class ImagineGamesScraperPipeline:
    def process_item(self, item, spider):
        print(item)
        return item

# Pipeline that stores data temporarily in memory
# Used to delay storage of data in database until all aspects of data has been gathered
class RedisStore:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    
    def __init__(self, settings):
        # Establish a connection to the redis database
        self.redis_connection = redis.Redis(
            host=settings.get('REDIS_HOST'),
            port=settings.get('REDIS_PORT'),
            password=settings.get('REDIS_ACCESS_PASSWORD'),
            db=0
        )
        try:
            print('Connection to redis database established successfully.')
        except:
            print('Error occured while attempting to connect to redis database.')
    def process_item(self, item, spider):
        print(self.redis_connection.get('name'))

# Pipeline that stores data in postgres database
class PostgresStore:
    # Method used to retrieve settings from Scrapy project settings
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    
    def __init__(self, settings):
        # Establish a connection to the Postgres database
        engine = create_engine(
            url="postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
                settings.get('POSTGRES_ACCESS_USER'),
                parse.quote(settings.get('POSTGRES_ACCESS_PASSWORD')),
                settings.get('POSTGRES_HOST'),
                settings.get('POSTGRES_PORT'),
                settings.get('POSTGRES_DATABASE')
            )
        )
        self.sessionmaker = sessionmaker(bind=engine)

    def open_spider(self, spider):
        self.alchemy_connection = self.sessionmaker()
    
    def close_spider(self, spider):
        self.alchemy_connection.close()

    def process_item(self, item, spider):
        existing_item = self.alchemy_connection.query(Video).filter_by(content_id="53399408-02f8-467e-bc4a-bb79aa610055").first()
        print("existing_item: ", existing_item)