import os
import platform
import queue
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime

from libs import config, models, sender, utils
from loguru import logger


class Worker(threading.Thread):
    def __init__(self, worker: models.GPUWorkerSchema, job_queue, result_queue,):
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
                # get job
                job = models.JobSchema.parse_obj(self.job_queue.get())
                self.worker._add_job(job)

                # get bin path and argument
                power_argument = self.worker._cmd()
                miner_bin_path = utils.get_miner_bin_path(self.worker.gpu_device)
                logger.debug(self.worker.gpu_device)
                logger.debug(miner_bin_path)

                power_cmd = f"{miner_bin_path} {power_argument}".split(' ')
                self.process = subprocess.Popen(power_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                logger.info(f"Miner is Running!")
                logger.info(f"Worker {job}")
                hash_rate = ''
                try:
                    while self.process.poll() is None:
                        output = self.process.stderr.readline()
                        if output:
                            logger.debug(f'output: {output}')
                            hash_rate = utils.parse_log_to_hashrate(output)
                            if hash_rate:
                                logger.info(f'GPU{self.worker.gpu_id} - average hashrate: {hash_rate}')

                    result = self.worker._generate_job_result(hash_rate)
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
    def __init__(self, miner: models.MinerSchema, job_queue, result_queue, job_expiration):
        threading.Thread.__init__(self)
        self.miner = miner
        self.job_queue = job_queue
        self.result_queue = result_queue
        self.job_expiration = job_expiration

    def run(self):
        ts = datetime.now()
        while True:
            # get job
            if (datetime.now()-ts).total_seconds() > self.job_expiration:
                logger.debug(f"Job expiration")
                while not self.job_queue.empty():
                    self.job_queue.get()
                for i in range(len(self.miner.devices)):
                    self.job_queue.put(sender.job(self.miner))
                ts = datetime.now()
            elif self.job_queue.qsize() < len(self.miner.devices):
                logger.debug(f"Job amount is too low")
                for i in range(self.job_queue.qsize(), len(self.miner.devices)):
                    self.job_queue.put(sender.job(self.miner))
                ts = datetime.now()

            # submit
            if self.result_queue.qsize() > 0:
                for i in range(self.result_queue.qsize()):
                    result = self.result_queue.get()
                    logger.info(f"Result submit: {result}")
                    sender.submit(self.miner, result)

            logger.debug(f"Job/Result in queue: {self.job_queue.qsize()}/{self.result_queue.qsize()}")
            time.sleep(1)


def create_job_manager(
        miner: models.MinerSchema, job_queue: queue.Queue, result_queue: queue.Queue, job_expiration: int = 900):
    job_mgr = JobManager(miner, job_queue, result_queue, job_expiration)
    job_mgr.setDaemon(True)
    job_mgr.start()
    return job_mgr


def create_worker(miner: models.MinerSchema, job_queue: queue.Queue, result_queue: queue.Queue,):
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
