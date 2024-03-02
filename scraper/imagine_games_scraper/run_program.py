import multiprocessing
import time
from scrapy.crawler import CrawlerProcess
from imagine_games_scraper.spiders.ign_content_spider import IgnContentSpiderSpider
from imagine_games_scraper.queue.queue_class import StoreQueue
from scrapy.utils.project import get_project_settings

# Function to run Scrapy Spider
def run_spider(*args, **kwargs):
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(IgnContentSpiderSpider, *args, **kwargs)
    process.start()

# Function to run queue
def run_queue(queue_instance):
    # Start queue worker
    queue_instance.start()

    timeout = 20
    start_time = time.time()
    while True:
        if queue_instance.is_idle():
            idle_time = time.time() - start_time
            if idle_time >= timeout:
                print("No queue jobs were added in the last %s seconds. Exiting." % timeout)
                # Stop queue worker
                queue_instance.stop()
                break
            time.sleep(5)
        else:
            start_time = time.time()

if __name__ == "__main__":
    # Create separate processes for running spider and RQ worker
    queue_instance = StoreQueue(settings=get_project_settings())
    queue_process = multiprocessing.Process(target=run_queue, args=(queue_instance,))
    spider_process = multiprocessing.Process(target=run_spider, kwargs={ 'enqueue_task': queue_instance.enqueue_task })

    # Start both processes
    queue_process.start()
    spider_process.start()

    # Wait for both processes to finish
    queue_process.join()
    spider_process.join()