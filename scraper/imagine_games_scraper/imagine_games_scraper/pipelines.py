from imagine_games_scraper.storeQueue import StoreQueue

class ImagineGamesScraperPipeline:
    def process_item(self, item, spider):
        print(dict(item))
        return item


# Pipeline to enqueue the storing of data to postgres
class PostgresStore:
    # Method used to retrieve settings from Scrapy project settings
    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(enqueue_task=crawler.settings.get('enqueue_task'))
    
    # def __init__(self, enqueue_task):
    #     print('******* marker')
    #     self.enqueue_task = enqueue_task

    def process_item(self, item, spider):
        print('*********** marker')
        # self.enqueue_task(item)
        return item