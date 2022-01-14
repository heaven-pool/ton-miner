import argparse
import os
import sys
import pyopencl as cl
from datetime import datetime
from loguru import logger

VERSION: str = "0.1.0"


def arg_parser(run_args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', dest='DEBUG', action='store_true', help='Show all logs')
    parser.add_argument('--stats', dest='STATS', action='store_true', help='Dump stats to stats.json')
    parser.add_argument('pool', help='Pool URL')
    parser.add_argument('wallet', help='Your wallet address')
    return parser.parse_args(run_args)


def init_logger(run_params):
    now = datetime.now()
    if run_params.DEBUG:
        log_level = 'DEBUG'
    else:
        log_level = 'INFO'
    logger.remove()
    logger.add(sys.stdout, level=log_level)
    logger.add(f"miner_{now.strftime('%Y-%m-%dT%H-%M-%S')}.log", level=log_level)
    logger.add(f"miner_{now.strftime('%Y-%m-%dT%H-%M-%S')}.err", level="WARNING")


def get_device_id(device):
    name = device.name
    try:
        bus = device.get_info(0x4008)
        slot = device.get_info(0x4009)
        return name + ' on PCI bus %d slot %d' % (bus, slot)
    except cl.LogicError:
        pass
    try:
        topo = device.get_info(0x4037)
        return name + ' on PCI bus %d device %d function %d' % (topo.bus, topo.device, topo.function)
    except cl.LogicError:
        pass
    return name


def opencl_devices():
    try:
        platforms = cl.get_platforms()
    except cl.LogicError:
        logger.warning('Failed to get OpenCL platforms, check your graphics card drivers')
        os._exit(255)

    devices = []
    for i, platform in enumerate(platforms):
        logger.info('Platform %d:' % i)
        for j, device in enumerate(platform.get_devices()):
            logger.info('    Device %d: %s' % (j, get_device_id(device)))
            devices.append(device)

    return devices


def print_info(run_params):
    logger.info(f'Miner info: {VERSION}')
    logger.info(f'Debug mode: {run_params.DEBUG}')
    logger.info(f'Stats mode: {run_params.STATS}')
    logger.info(f'Pool URL: {run_params.pool}')
    logger.info(f'Wallet address: {run_params.wallet}')


def init(argv):
    params = arg_parser(argv)
    init_logger(params)
    devices = opencl_devices()
    print_info()

    miner = model.MinerSchema(pool_url=params.pool, miner_wallet=params.wallet, GPUs=devices)
    return miner
