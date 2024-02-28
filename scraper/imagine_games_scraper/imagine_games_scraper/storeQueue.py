from rq import Queue, Worker, Connection
from redis import Redis
import psycopg2
import os
import signal

class StoreQueue:

    def __init__(self, settings):
        # Establish a connection to the redis database
        self.redis_connection = Redis(
            host=settings.get('REDIS_HOST'),
            port=settings.get('REDIS_PORT'),
            password=settings.get('REDIS_ACCESS_PASSWORD'),
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

        # Establish a connection to the Postgres database
        self.postgres_connection = psycopg2.connect(
            database = settings.get('POSTGRES_DATABASE'),
            user = settings.get('POSTGRES_ACCESS_USER'),
            password = settings.get('POSTGRES_ACCESS_PASSWORD'),
            host = settings.get('POSTGRES_HOST'),
            port = settings.get('POSTGRES_PORT')
        )
        if not self.postgres_connection.closed:
            print('Connection to postgres database established successfully.')
            self.cursor = self.postgres_connection.cursor()
        else:
            print('Error occured while attempting to connect to postgres database.')

    def start(self):
        with Connection(self.redis_connection):
            self.worker = Worker(self.queues, connection=self.redis_connection)
            self.worker.work()

    def stop(self):
        if self.worker:
            try:
                self.redis_connection.close()
                self.postgres_connection.close()
                print("Successfully closed connection to databases.")
                # Terminate the running program
                os.kill(self.worker.pid, signal.SIGTERM)
            except:
                print("Error occured when attempting to close connection to databases.")

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

    def job_function(self, item):
        print(item)

    def enqueue_task(self, item, priority = 1):
        print(item, priority)
        # 0 - high : 1 - default : 2 - low
        queue = self.queues[priority]
        queue.enqueue("storeQueue.job_function", item)

def job_function(item):
    print('lol')
    
if __name__ == '__main__':
    # Testing/Debuggin Purposes
    store_queue = StoreQueue()
    # start the worker
    store_queue.start()