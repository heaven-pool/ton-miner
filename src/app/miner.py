import queue
import threading
import time
import sys
import signal
from loguru import logger
import config
import model
import sender


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
    def __init__(self, miner, queue, num):
        threading.Thread.__init__(self)
        logger.debug(sender.job(miner))
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


def create_job_manager(miner: model.MinerSchema, queue: queue.Queue):
    job_mgr = JobManager(miner, queue, 1)
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


class Graceful:
    rip = False

    def __init__(self):
        signal.signal(signal.SIGHUP, self.you_may_die)
        signal.signal(signal.SIGABRT, self.you_may_die)
        signal.signal(signal.SIGINT, self.you_may_die)
        signal.signal(signal.SIGQUIT, self.you_may_die)
        signal.signal(signal.SIGTERM, self.you_may_die)

    def you_may_die(self, *args):
        self.rip = True


if __name__ == '__main__':
    miner = config.init(sys.argv[1:])
    logger.debug(miner)

    task_queue = queue.Queue()
    job_manager = create_job_manager(miner, task_queue)
    work_pools = create_worker(len(miner.GPUs), task_queue)

    graceful = Graceful()
    while not graceful.rip:
        time.sleep(1)

    logger.info("Interrupted...")
    logger.info("Exiting...")
