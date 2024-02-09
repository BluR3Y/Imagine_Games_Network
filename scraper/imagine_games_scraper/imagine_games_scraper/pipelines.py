import mysql.connector
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

class MySQLStore:
    # Method used to retrieve settings from Scrapy project settings
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        # Establish a connection to the MySQL database
        self.conn = mysql.connector.connect(
            host = settings.get('MYSQL_HOST'),
            user = settings.get('MYSQL_USER'),
            password = settings.get('MYSQL_PASSWORD'),
            database = settings.get('MYSQL_DATABASE')
        )
        # Create cursor, used to execute commands
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, Article):
            print('****** Article ******')
        elif isinstance(item, Video):
            print('******* Video *******')
        elif isinstance(item, Contributor):
            print('******* Reporter *******')
        else: print('******** other ************')
        return item

    def close_spider(self, spider):
        # Close cursor & connection to database when the spider is closed
        self.cur.close()
        self.conn.close()