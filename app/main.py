import os
import platform
import queue
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime

import pydantic
import pyopencl
import requests
from libs import config, runner
from loguru import logger

if __name__ == "__main__":
    miner = config.init(sys.argv[1:])
    logger.debug(miner)

    task_queue = queue.Queue()
    result_queue = queue.Queue()
    job_manager = runner.create_job_manager(miner, task_queue, result_queue)
    work_pools = runner.create_worker(miner, task_queue, result_queue)

    graceful = runner.Graceful()
    while not graceful.rip:
        time.sleep(1)

    logger.info("Interrupted...")
    logger.info("Exiting...")
