import multiprocessing
import time
import signal
import sys

from scrapy.crawler import CrawlerProcess
from imagine_games_scraper.spiders.ign_content_spider import IgnContentSpiderSpider
from imagine_games_scraper.queue import activeQueue
from scrapy.utils.project import get_project_settings

# Function to run Scrapy Spider
def run_spider(*args, **kwargs):
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(IgnContentSpiderSpider, *args, **kwargs)
    process.start()

# Function to run queue
def run_queue():
    # Start queue worker
    activeQueue.start()

    timeout = 20
    start_time = time.time()
    while True:
        if activeQueue.is_idle():
            idle_time = time.time() - start_time
            if idle_time >= timeout:
                print("No queue jobs were added in the last %s seconds. Exiting." % timeout)
                # Stop queue worker
                activeQueue.stop()
                break
            time.sleep(5)
        else:
            start_time = time.time()

def stop_processes(sig, frame):
    print("Keyboard interrupt received. Stopping processes...")
    queue_process.terminate()
    spider_process.terminate()
    sys.exit(0)

if __name__ == "__main__":
    # Create separate processes for running spider and RQ worker
    queue_process = multiprocessing.Process(target=run_queue)
    spider_process = multiprocessing.Process(target=run_spider)

    # Set up signal handler for keyboard interrupt
    signal.signal(signal.SIGINT, stop_processes)

    # Start both processes
    queue_process.start()
    spider_process.start()

    # Wait for both processes to finish
    queue_process.join()
    spider_process.join()