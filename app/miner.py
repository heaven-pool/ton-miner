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
import utils
import sender
from loguru import logger


class Worker(threading.Thread):
    def __init__(self, worker: model.GPUWorkerSchema, job_queue, result_queue,):
        threading.Thread.__init__(self)
        self.worker = worker
        self.job_queue = job_queue
        self.result_queue = result_queue
        self.id = worker.gpu_id
        self.process = None

    def __del__(self):
        if self.process:
            self.process.kill()

    def run(self):
        while True:
            if not self.job_queue.empty():

                job = model.JobSchema.parse_obj(self.job_queue.get())
                self.worker._add_job(job)
                power_argument = self.worker._cmd()

                logger.info(self.worker.gpu_device)
                miner_bin_path = utils.get_miner_bin_path(self.worker.gpu_device)
                logger.info(miner_bin_path)

                power_cmd = f"{miner_bin_path} {power_argument}".split(' ')
                self.process = subprocess.Popen(power_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                logger.info(f"Miner is Running!")
                logger.info(f"Worker {job}")
                try:
                    while self.process:
                        output = self.process.stderr.readline()
                        if output:
                            logger.info(output)

                    result = self.worker._generate_job_result()
                    self.result_queue.put(result)
                    logger.info(f"Try to submit result! ... {result}")
                except FileNotFoundError:
                    outs, errs = self.process.communicate()
                    logger.info(f"power doesn't generate boc file ... {outs}, {errs}")
                    self.process.terminate()
                    self.process.wait()
                except subprocess.TimeoutExpired:
                    outs, errs = self.process.communicate()
                    logger.warning(f"TimeoutExpired! ... {outs}, {errs}")
                    self.process.terminate()
                    self.process.wait()

            else:
                logger.debug(f"Worker Idle {self.id}")
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
            # get job
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

            # submit
            if self.result_queue.qsize() > 0:
                for i in range(self.result_queue.qsize()):
                    result = self.result_queue.get()
                    logger.info(f"Result submit: {result}")
                    sender.submit(self.miner, result)

            # logger.info(f"Job/Result in queue: {self.job_queue.qsize()}/{self.result_queue.qsize()}")
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
