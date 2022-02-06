import os
import platform
import re
from pathlib import Path

from loguru import logger

APP_ROOT_PATH = Path(os.path.dirname(os.path.abspath(__file__))).parent


def get_ubuntu_version(version_id: str):
    if re.search('20', version_id):
        return 'ubuntu20'
    elif re.search('18', version_id):
        return 'ubuntu18'
    else:
        raise NotImplementedError(version_id)


def get_os_type():
    '''
        uname = platform.uname()
        uname.system -> windows, linux

        Linux
        uname.version
        know ubuntu by version
        uname_result(system='Linux', node='ip-172-31-2-187', release='5.11.0-1022-aws', version='#23~20.04.1-Ubuntu SMP Mon Nov 15 14:03:19 UTC 2021', machine='x86_64', processor='x86_64')

        know hiveos by version
        uname_result(system='Linux', node='Rig_4138467', release='5.4.0-hiveos', version='#140.hiveos.210813 SMP Fri Aug 13 11:40:32 UTC 2021', machine='x86_64', processor='x86_64')
    '''
    uname = platform.uname()
    if uname.system == 'Windows':
        return 'windows'
    elif uname.system == 'Linux':
        if 'Ubuntu' in uname.version:
            version_id = re.search('VERSION_ID=(.*)\\n', open('/etc/os-release', 'r').read()).group(0)
            return get_ubuntu_version(version_id)
        elif 'hiveos' in uname.version:
            return 'hiveos'
        else:
            raise NotImplementedError(uname)
    else:
        raise NotImplementedError(uname)


def get_bin_path(os_type: str, binfile: str) -> Path:
    if os_type == 'windows':
        return Path(APP_ROOT_PATH, 'assets', f'win-{binfile}.exe')
    elif os_type == 'ubuntu18' or os_type == 'hiveos':
        return Path(APP_ROOT_PATH, 'assets', f'ubuntu18-{binfile}')
    elif os_type == 'ubuntu20':
        return Path(APP_ROOT_PATH, 'assets', f'ubuntu20-{binfile}')
    else:
        logger.error(f'gpu does not be executable {binfile}')
        raise NotImplementedError(uname)


def get_gpu_vender(gpu_info: str):
    '''
        'NVIDIA CUDA GeForce GTX 1050 Ti on PCI bus 3 slot 0'
    '''
    if "NVIDIA" in gpu_info.upper():
        return "cuda"
    elif "AMD" in gpu_info.upper():
        return "opencl"


def get_miner_bin_path(gpu_info: str) -> Path:
    vender = get_gpu_vender(gpu_info)
    os_type = get_os_type()

    return get_bin_path(os_type=os_type, binfile=vender)


def parse_log_to_hashrate(data: str) -> str:
    '''
        input:
            b'[ GPU #0: SM 6.1 GeForce GTX 1050 Ti ]\x1b[0m\n'
            b'\x1b[1;36m[ 3][t 0][2022-02-05 14:56:53.316578448][pow-miner.cpp:388]\t[ expected required hashes for success: 29301469717946154 ]\x1b[0m\n'
            b'\x1b[1;33m[ 2][t 0][2022-02-05 14:56:53.494029473][credits.cu:29]\t[ START MINER, GPU ID: 0, boost factor: 16, throughput: 8388608 ]\x1b[0m\n'
            b'\x1b[1;36m[ 3][t 0][2022-02-05 14:56:58.323761700][Miner.cpp:105]\t[ mining in progress, passed: 5006.4ms, hashes computed: 1769996288, instant speed: 365.831 Mhash/s, average speed: 353.546 Mhash/s ]\x1b[0m\n'
            b'\x1b[1;36m[ 3][t 0][2022-02-05 14:57:03.329795978][Miner.cpp:105]\t[ mining in progress, passed: 10.0s, hashes computed: 3615490048, instant speed: 368.285 Mhash/s, average speed: 361.073 Mhash/s ]\x1b[0m\n'

            passed: 10.0s, hashes computed: 3615490048, instant speed: 368.285 Mhash/s, average speed: 361.073 Mhash/s
        output:
            hashrate
    '''

    try:
        info = re.search(r"mining in progress, (.*) ]\\x1b", str(data)).group(1)
        average_speed = re.search(r"average speed: (.*) Mhash/s", str(info)).group(1)
        return average_speed
    except:
        return ''
