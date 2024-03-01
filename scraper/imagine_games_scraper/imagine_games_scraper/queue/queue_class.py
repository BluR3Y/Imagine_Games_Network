from rq import Queue, Worker, Connection, Retry
from redis import Redis
from datetime import timedelta

class StoreQueue:

    def __init__(self, settings):
        self.settings = settings
        # Establish a connection to the redis database
        self.redis_connection = Redis(
            host=self.settings.get('REDIS_HOST'),
            port=self.settings.get('REDIS_PORT'),
            password=self.settings.get('REDIS_ACCESS_PASSWORD'),
            db=0
        )
        try:
            # Validate connection by pinging to Redis
            self.redis_connection.ping()
            print('Connection to redis database established successfully.')
            # Create priority queues
            self.queues = [
                Queue('high',connection=self.redis_connection),
                Queue('default', connection=self.redis_connection),
                Queue('low', connection=self.redis_connection)]
        except:
            print('Error occured while attempting to connect to redis database.')

    def start(self):
        with Connection(self.redis_connection):
            self.worker = Worker(self.queues, connection=self.redis_connection)
            self.worker.work(with_scheduler=True)

    def stop(self):
        if self.worker:
            try:
                # Close connections to databases
                self.redis_connection.close()
                print("RQ successfully closed connection to databases.")
            except:
                print("RQ faced an error while attempting to close connection to databases.")

    def is_idle(self):
        all_queues_idle = True
        for queue in self.queues:
            if not queue.is_empty():
                all_queues_idle = False
                break
        return all_queues_idle

    def add_queue(self, queue):
        self.queues.append(queue)

    def remove_queue(self, queue):
        if queue in self.queues:
            self.queues.remove(queue)

    def enqueue_task(self, item, priority = 1, delay = 0, attempts=5, intervals = [5]):
        # 0 - high : 1 - default : 2 - low
        queue = self.queues[priority]
        # queue.enqueue("imagine_games_scraper.queue.queue_function.queue_function", item, retry=Retry(max=6, interval=5))
        queue.enqueue_in(timedelta(seconds=delay), "imagine_games_scraper.queue.queue_function.queue_function", item, retry=Retry(max=attempts, interval=intervals))


if __name__ == '__main__':
    # Testing/Debuggin Purposes
    store_queue = StoreQueue({})
    # start the worker
    store_queue.start()