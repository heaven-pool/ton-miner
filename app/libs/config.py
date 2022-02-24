import argparse
import os
import sys
from datetime import datetime

import pyopencl as cl
from libs import models
from loguru import logger

VERSION: str = "0.1.2"


def arg_parser(run_args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", default=False, action="store_true", help="Show all logs")
    parser.add_argument("--stats", default=False, action="store_true", help="Dump stats to stats.json")
    parser.add_argument("--pool", default="https://ton.heaven-pool.com", help="Pool URL")
    parser.add_argument("wallet", help="Your wallet address")
    return parser.parse_args(run_args)


def init_logger(run_params):
    now = datetime.now()
    if run_params.debug:
        log_level = "DEBUG"
    else:
        log_level = "INFO"
    logger.remove()
    logger.add(sys.stdout, level=log_level)
    logger.add(f"logs/miner_{now.strftime('%Y-%m-%dT%H-%M-%S')}.log", rotation="1 week", level=log_level)
    logger.add(f"logs/miner_{now.strftime('%Y-%m-%dT%H-%M-%S')}.err.log", rotation="1 week", level="WARNING")


def get_device_id(device):
    name = device.name
    bus = -1
    slot = -1
    try:
        bus = device.get_info(0x4008)
        slot = device.get_info(0x4009)
    except cl.LogicError:
        logger.warning("Failed to get bus and slot, default = 66")

    return name, bus, slot


def opencl_devices():
    try:
        platforms = cl.get_platforms()
    except cl.LogicError:
        logger.warning("Failed to get OpenCL platforms, check your graphics card drivers")
        os._exit(255)

    devices = []
    gpus = []
    for platform in platforms:
        logger.debug(f"Platform {platform.name}:")
        for j, device in enumerate(platform.get_devices()):
            name, bus, slot = get_device_id(device)
            logger.debug(f"    Device {j}: {name} on PCI bus {bus} slot {slot}")
            if slot != -1:
                devices.append(f"{platform.name} {name}")
                gpus.append(slot)
    return devices, gpus


def print_info(run_params):
    logger.info(f"Miner info: {VERSION}")
    logger.info(f"Debug mode: {run_params.debug}")
    logger.info(f"Stats mode: {run_params.stats}")
    logger.info(f"Pool URL: {run_params.pool}")
    logger.info(f"Wallet address: {run_params.wallet}")


def init(argv):
    params = arg_parser(argv)
    init_logger(params)
    print_info(params)

    devices, gpus = opencl_devices()
    logger.info(devices)
    logger.info(gpus)

    miner = models.MinerSchema(
        pool_url=params.pool,
        miner_wallet=params.wallet,
        devices=devices,
        gpus=gpus,
    )
    return miner
