import argparse
import os
import sys

import pyopencl as cl
from loguru import logger

version = "0.1.0"


def init(env):
    # log init
    if env.DEBUG:
        log_level = 'DEBUG'
    elif env.SILENT:
        log_level = 'WARNING'
    else:
        log_level = 'INFO'
    logger.add(sys.stderr, level=log_level)
    logger.add("mining.log")

    # GPUs info init
    try:
        platforms = cl.get_platforms()
    except cl.LogicError:
        logger.warning('Failed to get OpenCL platforms, check your graphics card drivers')
        os._exit(0)

    devices = platforms[0].get_devices()
    for i, device in enumerate(devices):
        logger.info('    Device %d: %s' % (i, get_device_id(device)))

    miner = model.MinerSchema(pool_url=env.pool, miner_wallet=env.wallet, GPUs=devices)
    return miner


def config(run_args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--stats', dest='STATS', action='store_true', help='Dump stats to stats.json')
    parser.add_argument('--debug', dest='DEBUG', action='store_true', help='Show all logs')
    parser.add_argument('pool', help='Pool URL')
    parser.add_argument('wallet', help='Your wallet address')
    return parser.parse_args(run_args)


def info():
    logger.info(f'Miner info: {version}')
    logger.info(f'runtime argument : {run_args}')
    try:
        platforms = cl.get_platforms()
    except cl.LogicError:
        logger.info('Failed to get OpenCL platforms, check your graphics card drivers')
        os._exit(0)
    for i, platform in enumerate(platforms):
        logger.info('Platform %d:' % i)
        for j, device in enumerate(platform.get_devices()):
            logger.info('    Device %d: %s' % (j, get_device_id(device)))

    logger.info('Usage: %s [pool url] [wallet address]' % args[0])


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


try:
    platforms = cl.get_platforms()
except cl.LogicError:
    print('failed to get OpenCL platforms, check your graphics card drivers')
    os._exit(0)
for i, platform in enumerate(platforms):
    print('Platform %d:' % i)
    for j, device in enumerate(platform.get_devices()):
        print('    Device %d: %s' % (j, get_device_id(device)))
