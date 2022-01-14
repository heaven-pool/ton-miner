# -*- coding: utf-8 -*-
import os

import pyopencl as cl


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
