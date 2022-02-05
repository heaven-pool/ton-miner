import re
import platform
from pathlib import Path
from loguru import logger

APP_ROOT_PATH = Path(os.path.dirname(os.path.abspath(__file__)))


def get_ubuntu_version(version_id: str):
    if re.search('20', version_id):
        return 'ubuntu20'
    elif re.search('18', version_id):
        return 'ubuntu18'
    else:
        NotImplementedError(version_id)


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
            NotImplementedError(uname)
    else:
        NotImplementedError(uname)


def get_bin_path(binfile: str) -> Path:
    os_type = get_os_type()

    if os_type == 'windows':
        return Path(APP_ROOT_PATH, 'assets', f'win-{binfile}.exe')
    elif os_type == 'ubuntu18' or os_type == 'hiveos':
        return Path(APP_ROOT_PATH, 'assets', f'ubuntu18-{binfile}')
    elif os_type == 'ubuntu20':
        return Path(APP_ROOT_PATH, 'assets', f'ubuntu20-{binfile}')
    else:
        logger.error(f'gpu does not be executable {binfile}')
        return ""


def lite_client_path() -> Path:
    return get_bin_path('lite-client')


def miner_cuda_path() -> Path:
    return get_bin_path('cuda')


def miner_opencl_path() -> Path:
    return get_bin_path('opencl')


def parse_bin_log(data: str):
    '''
        input:
            b'\x1b[1;36m[ 3][t 0][2022-02-05 13:20:50.976809507][Miner.cpp:105]\t[ mining in progress, passed: 5006.2ms, hashes computed: 1761607680, instant speed: 371.361 Mhash/s, average speed: 351.884 Mhash/s ]\x1b[0m\n'
        output:
    '''
    pass
