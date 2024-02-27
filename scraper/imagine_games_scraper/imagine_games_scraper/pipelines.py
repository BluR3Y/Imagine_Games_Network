from imagine_games_scraper.storeQueue import StoreQueue

class ImagineGamesScraperPipeline:
    def process_item(self, item, spider):
        print(dict(item))
        return item


# Pipeline to enqueue the storing of data to postgres
class PostgresStore:
    # Method used to retrieve settings from Scrapy project settings
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.queue = StoreQueue(settings)

    def close_spider(self, spider):
        self.queue.close()

    def process_item(self, item, spider):
        self.queue.enqueue_task(item)

        return item