import queue
import threading
import time

from loguru import logger

sleep_time = 1


class Worker(threading.Thread):
    def __init__(self, queue, num):
        threading.Thread.__init__(self)
        self.queue = queue
        self.num = num

    def run(self):
        while True:
            size = self.queue.qsize()
            if size > 0:
                msg = self.queue.get()
                logger.info("Worker %d: %s / queue %d" % (self.num, msg, size))
            else:
                logger.info("Worker Idle %d" % (self.num))
            time.sleep(1)


class JobManager(threading.Thread):
    def __init__(self, queue, num):
        threading.Thread.__init__(self)
        self.queue = queue
        self.num = num

    def run(self):
        while True:
            size = self.queue.qsize()
            if size < 4:
                for i in range(8):
                    task_queue.put("Data %d" % i)
                logger.info("JobManager Thread %d - queue size %d" % (self.num, size))

            time.sleep(1)


def create_job_manager(queue: queue.Queue):
    job_mgr = JobManager(queue, 1)
    job_mgr.setDaemon(True)
    job_mgr.start()
    return job_mgr


def create_worker(num: str, queue: queue.Queue):
    worker_pool = []
    for i in range(num):
        worker = Worker(queue, i)
        worker.setDaemon(True)
        worker.start()
        worker_pool.append(worker)

    return worker_pool


if __name__ == '__main__':
    env_args = init.config(sys.argv)
    # miner = init.init(env_args)
    # logger.debug(miner)

    # device_num = 4
    # task_queue = queue.Queue()
    # job_manager = create_job_manager(task_queue)
    # work_pools = create_worker(device_num, task_queue)

    # try:
    #     while True:
    #         time.sleep(sleep_time)
    # except Exception as e:
    #     logger.warning(f"Exception: {e}")
    # except KeyboardInterrupt:
    #     logger.info("Exit the program")
