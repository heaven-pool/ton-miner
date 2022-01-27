import platform
import requests
import zipfile
from pathlib import Path
import os
import glob
import re
import shutil
import tarfile
from loguru import logger

VERSION = '20211230.1'
BASE_URL = f'https://github.com/tontechio/pow-miner-gpu/releases/download/{VERSION}'

HIVEOS_VERSION = 'h.20211230.1'
HIVEOS_BASE_URL = f'https://github.com/tontechio/pow-miner-gpu-hiveos/releases/download/{HIVEOS_VERSION}'

MINER_TOOLS = {
    'windows': [
        f'{BASE_URL}/minertools-cuda-windows-x86-64.zip',
        f'{BASE_URL}/minertools-opencl-windows-x86-64.zip'
    ],
    'ubuntu18': [
        f'{BASE_URL}/minertools-cuda-ubuntu-18.04-x86-64.tar.gz',
        f'{BASE_URL}/minertools-opencl-ubuntu-18.04-x86-64.tar.gz'
    ],
    'ubuntu20': [
        f'{BASE_URL}/minertools-cuda-ubuntu-20.04-x86-64.tar.gz',
        f'{BASE_URL}/minertools-opencl-ubuntu-20.04-x86-64.tar.gz'
    ],
    'hiveos': [
        f'{HIVEOS_BASE_URL}/tonminer_opencl_hiveos_x86_64-{HIVEOS_VERSION}.tar.gz',
        f'{HIVEOS_BASE_URL}/tonminer_cuda_hiveos_x86_64-{HIVEOS_VERSION}.tar.gz'
    ]
}

IGNORE_PATTENS = ['*.sh', 'tonlib*', '*.service', 'release.json', '*.conf', '*.json', '*.md']

PROJECT_ROOT_PATH = Path(os.path.dirname(os.path.abspath(__file__))).parents[1]


def get_os_type():
    uname = platform.uname()
    if uname.system == 'Windows':
        return 'windows'
    elif uname.system == 'Linux':
        if uname.node == 'ubuntu':
            version_id = re.search('VERSION_ID=(.*)\\n', open('/etc/os-release', 'r').read()).group(0)
            if re.search('20', version_id):
                return 'ubuntu20'
            elif re.search('18', version_id):
                return 'ubuntu18'
            else:
                NotImplementedError(uname, version_id)
        elif 'hiveos' in uname.release:
            return 'hiveos'
        else:
            NotImplementedError(uname)
    else:
        NotImplementedError(uname)


def download_url(url, dst_folder, chunk_size=128):
    filename = Path(dst_folder, url.split('/')[-1])
    logger.info(f'Download {url}')
    r = requests.get(url)

    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def create_download_folder(os_type: str):
    folder = Path(PROJECT_ROOT_PATH, 'build', os_type)
    os.makedirs(folder, exist_ok=True)
    logger.info(f'Create {folder}')
    return folder


def create_bin_folder(os_type: str):
    folder = Path(PROJECT_ROOT_PATH, 'bin', os_type)
    os.makedirs(folder, exist_ok=True)
    logger.info(f'Create {folder}')
    return folder


def unzip_file(src_file: str, dst_folder: str):
    logger.info(f'Unzip {src_file}')
    with zipfile.ZipFile(src_file, 'r') as zf:
        for member in zf.namelist():
            filename = os.path.basename(member)
            if not filename:  # skip directories
                continue

            source = zf.open(member)
            target = open(os.path.join(dst_folder, filename), 'wb')
            with source, target:
                shutil.copyfileobj(source, target)


def untar_file(src_file: str, dst_folder: str):
    logger.info(f'Untar {src_file}')
    with tarfile.open(src_file, 'r') as tf:
        for member in tf.getmembers():
            if member.isreg():  # skip if the TarInfo is not files
                # remove the path by reset it
                member.name = os.path.basename(member.name)
                tf.extract(member, dst_folder)  # extract


def unarchive_each_files(src_folder: str, dst_folder: str):
    logger.info(f'Unarchive')
    files = glob.glob(f'{src_folder}/*.zip') + \
        glob.glob(f'{src_folder}/*.tar.gz')

    for file in files:
        if file.split('.')[-1] == 'zip':
            unzip_file(file, dst_folder)
        elif file.split('.')[-1] == 'gz':
            untar_file(file, dst_folder)
        else:
            logger.info('file type error')


def remove_patten_files(dst_folder: str, pattern: str = 'tonlib*'):
    files = glob.glob(f'{dst_folder}/{pattern}')
    for file in files:
        logger.info(f'Remove {file}')
        os.remove(file)


def download(os_type: str):
    folder = create_download_folder(os_type)
    for url in MINER_TOOLS[os_type]:
        logger.info(f'Download {url}')
        download_url(url, folder)


if __name__ == "__main__":
    for os_type in MINER_TOOLS:
        src_folder = create_download_folder(os_type)
        dst_folder = create_bin_folder(os_type)
        download(os_type)
        unarchive_each_files(src_folder, dst_folder)
        for remove_patten in IGNORE_PATTENS:
            remove_patten_files(dst_folder, remove_patten)
