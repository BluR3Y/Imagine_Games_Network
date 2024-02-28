import multiprocessing
import time
from scrapy.crawler import CrawlerProcess
from imagine_games_scraper.spiders.ign_content_spider import IgnContentSpiderSpider
from imagine_games_scraper.storeQueue import StoreQueue

# Function to run Scrapy Spider
def run_spider():
    process = CrawlerProcess()
    process.crawl(IgnContentSpiderSpider)
    process.start()

def run_queue():
    store_queue = StoreQueue({
        'REDIS_HOST': '127.0.0.1',
        'REDIS_PORT': '6379',
        'REDIS_ACCESS_PASSWORD': 'AdminPassword@1234',
        'POSTGRES_DATABASE': 'imagine_games_network',
        'POSTGRES_ACCESS_USER': 'admin',
        'POSTGRES_ACCESS_PASSWORD': 'AdminPassword@1234',
        'POSTGRES_HOST': '127.0.0.1',
        'POSTGRES_PORT': '5432'
    })

    store_queue.enqueue_task("hello there", 1)
    timeout = 20
    start_time = time.time()
    while True:
        if store_queue.is_idle():
            idle_time = time.time() - start_time
            if idle_time >= timeout:
                print("No queue jobs were added in the last %s seconds. Exiting." % timeout)
                break
            time.sleep(5)
        else:
            start_time = time.time()

if __name__ == "__main__":
    # Create separate processes for running spider and RQ worker
    spider_process = multiprocessing.Process(target=run_spider)
    queue_process = multiprocessing.Process(target=run_queue)

    # Start both processes
    spider_process.start()
    queue_process.start()

    # Wait for both processes to finish
    spider_process.join()
    queue_process.join()