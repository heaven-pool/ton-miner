import os
import platform
import queue
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime

import config
import model
import package
import sender
from loguru import logger


class Worker(threading.Thread):
    def __init__(self, worker: model.GPUWorkerSchema, job_queue, result_queue,):
        threading.Thread.__init__(self)
        self.worker = worker
        self.job_queue = job_queue
        self.result_queue = result_queue
        self.id = worker.gpu_id

    def run(self):
        while True:
            if not self.job_queue.empty():
                job = model.JobSchema.parse_obj(self.job_queue.get())
                self.worker._add_job(job)
                power_argument = self.worker._cmd()
                logger.info(f"Worker {job}")

                logger.info(power_argument)
                logger.info(package.miner_cuda_path())
                logger.info(package.miner_opencl_path())
                logger.info(package.lite_client_path())
                power_cmd = package.miner_cuda_path() + power_argument

                try:
                    sub = subprocess.run(power_cmd, shell=True, check=True, stdout=subprocess.PIPE,)
                    result = self.worker._generate_job_result()
                    self.result_queue.put(result)
                    logger.info("try to submit result! ...")
                    logger.info(sub.stdout.decode("utf-8"))
                except subprocess.CalledProcessError as err:
                    logger.warning(f"Exit with error call! {err}")
                else:
                    logger.info("else condistion")
            else:
                logger.info(f"Worker Idle {self.id}")
            time.sleep(0.1)


class JobManager(threading.Thread):
    def __init__(self, miner: model.MinerSchema, job_queue, result_queue, job_expiration):
        threading.Thread.__init__(self)
        self.miner = miner
        self.job_queue = job_queue
        self.result_queue = result_queue
        self.job_expiration = job_expiration

    def run(self):
        ts = datetime.now()
        # TODO: handle result queue
        while True:
            if (datetime.now()-ts).total_seconds() > self.job_expiration:
                while not self.job_queue.empty():
                    self.job_queue.get()
                for i in range(len(self.miner.devices)):
                    self.job_queue.put(sender.job(self.miner))
                ts = datetime.now()
            elif self.job_queue.qsize() < len(self.miner.devices):
                for i in range(self.job_queue.qsize(), len(self.miner.devices)):
                    self.job_queue.put(sender.job(self.miner))
                ts = datetime.now()
            logger.info(f"Job in queue: {self.job_queue.qsize()}")

            if self.result_queue.qsize() > 0:
                for i in range(self.result_queue.qsize()):
                    result = self.result_queue.get()
                    sender.submit(self.miner, result)
                    logger.info(f"Result submit: {result}")

            logger.info(f"Result in queue: {self.result_queue.qsize()}")
            time.sleep(1)


def create_job_manager(
        miner: model.MinerSchema, job_queue: queue.Queue, result_queue: queue.Queue, job_expiration: int):
    job_mgr = JobManager(miner, job_queue, result_queue, job_expiration)
    job_mgr.setDaemon(True)
    job_mgr.start()
    return job_mgr


def create_worker(miner: model.MinerSchema, job_queue: queue.Queue, result_queue: queue.Queue,):
    worker_pools = []
    workers = miner._create_wokers()

    for worker in workers:
        wk = Worker(worker, job_queue, result_queue)
        wk.setDaemon(True)
        wk.start()
        worker_pools.append(wk)

    return worker_pools


class Graceful:
    rip = False

    def __init__(self):
        os_name = platform.system()
        if os_name == 'Linux' or os_name == 'Darwin':
            signal.signal(signal.SIGHUP, self.you_may_die)
            signal.signal(signal.SIGQUIT, self.you_may_die)
        signal.signal(signal.SIGABRT, self.you_may_die)
        signal.signal(signal.SIGINT, self.you_may_die)
        signal.signal(signal.SIGTERM, self.you_may_die)

    def you_may_die(self, *args):
        self.rip = True


if __name__ == "__main__":
    miner = config.init(sys.argv[1:])
    logger.debug(miner)

    task_queue = queue.Queue()
    result_queue = queue.Queue()
    job_manager = create_job_manager(miner, task_queue, result_queue, 10)
    work_pools = create_worker(miner, task_queue, result_queue)

    graceful = Graceful()
    while not graceful.rip:
        time.sleep(1)

    logger.info("Interrupted...")
    logger.info("Exiting...")
