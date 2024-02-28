

class ImagineGamesScraperPipeline:
    def process_item(self, item, spider):
        print(dict(item))
        return item
    
# Pipeline used to enqueue scraped data to redis-based queue
class RedisQueue:
    def process_item(self, item, spider):
        spider.enqueue_task(item)
        return item