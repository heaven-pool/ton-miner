import platform
import queue
import shlex
import signal
import subprocess
import threading
import time
from datetime import datetime

from libs import models, sender, utils
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

    def bin_path(self):
        # get bin path and argument
        power_argument = self.worker._cmd()
        miner_bin_path = utils.get_miner_bin_path(self.worker.gpu_device)
        power_cmd = shlex.split(f"{miner_bin_path} {power_argument}", posix=False)
        return power_cmd

    def run(self):
        while True:
            if not self.job_queue.empty():
                logger.debug(self.worker.gpu_device)
                # get jobs
                job = self.job_queue.get()
                self.worker._add_job(job)
                self.process = subprocess.Popen(self.bin_path(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                logger.info(f"=========== Miner is Running! ===========")
                logger.info(f"Worker {job}")
                logger.debug(self.bin_path())
                hash_rate = ''
                task_done = ''
                try:
                    while self.process.poll() is None:
                        output = self.process.stderr.readline()
                        if output:
                            logger.debug(f'output: {output}')
                            if utils.parse_log_to_hashrate(output):
                                hash_rate = utils.parse_log_to_hashrate(output)
                                logger.info(f'GPU{self.worker.gpu_id} - average hashrate: {hash_rate} Mhash/s')
                            if utils.parse_log_to_done(output):
                                task_done = utils.parse_log_to_done(output)
                                logger.info(f'GPU{self.worker.gpu_id} - task {task_done}')

                    if task_done:
                        logger.info(f"Try to submit result! ... return code: {self.process.returncode}")
                        result = self.worker._generate_job_result(float(hash_rate))
                        self.result_queue.put(result)
                        logger.info(f"Submit result! ... {result}")
                    else:
                        logger.warning(f"Task fail to finish! ... return code: {self.process.returncode}")
                except FileNotFoundError:
                    outs, errs = self.process.communicate()
                    logger.info(f"Power doesn't generate boc file ... {outs}, {errs}")
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
        self.total_shares = 0

    def run(self):
        ts = datetime.now()
        while True:
            # get job
            if (datetime.now()-ts).total_seconds() > self.job_expiration:
                logger.debug(f"Job expiration")
                while not self.job_queue.empty():
                    self.job_queue.get()
                for i in range(len(self.miner.devices)):
                    job = sender.job(self.miner)
                    if job:
                        self.job_queue.put(job)
                ts = datetime.now()
            elif self.job_queue.qsize() < len(self.miner.devices):
                logger.debug(f"Job amount is too low")
                for i in range(self.job_queue.qsize(), len(self.miner.devices)):
                    job = sender.job(self.miner)
                    if job:
                        self.job_queue.put(job)
                ts = datetime.now()

            # submit
            if self.result_queue.qsize() > 0:
                for i in range(self.result_queue.qsize()):
                    result = self.result_queue.get()
                    count = sender.submit(self.miner, result)
                    self.total_shares += count
                    logger.info(f"Result submit: {result}, shares: {self.total_shares}")

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


# TODO:
# hiveos report
# json.dump({
#     'total': (b[1] - a[1]) / ct / 10**3,
#     'rates': rates,
#     'uptime': time.time() - start_time,
#     'accepted': shares_accepted,
#     'rejected': shares_count - shares_accepted,
# }, open('stats.json', 'w'))
