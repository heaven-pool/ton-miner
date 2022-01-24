import platform
import requests
import zipfile
from pathlib import Path
import os
import glob
import shutil
import tarfile
# from logguru import logger

BASE_URL = 'https://github.com/tontechio/pow-miner-gpu/releases/latest/download'
WIN_MINER = [f'{BASE_URL}/minertools-cuda-windows-x86-64.zip',
             f'{BASE_URL}/minertools-opencl-windows-x86-64.zip']

UBUNTU_1804_MINER = [f'{BASE_URL}/minertools-cuda-ubuntu-18.04-x86-64.tar.gz',
                     f'{BASE_URL}/minertools-opencl-ubuntu-18.04-x86-64.tar.gz']
UBUNTU_2004_MINER = [f'{BASE_URL}/minertools-cuda-ubuntu-20.04-x86-64.tar.gz',
                     f'{BASE_URL}/minertools-opencl-ubuntu-20.04-x86-64.tar.gz']

HIVE_BASE_URL = 'https://github.com/tontechio/pow-miner-gpu-hiveos/releases/download'
HIVEOS_MINER = [f'{HIVE_BASE_URL}/h.20211230.1/tonminer_opencl_hiveos_x86_64-h.20211230.1.tar.gz',
                f'{HIVE_BASE_URL}/h.20211230.1/tonminer_cuda_hiveos_x86_64-h.20211230.1.tar.gz']

BUILD_PACK = ['window', 'ubuntu18', 'ubuntu20', 'hiveos']
REMOVE_PATTENS = ['*.sh', 'tonlib*', '*.service', 'release.json',  '*.conf']

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = Path(BASE_PATH).parents[1]
# steps
# 1. os
# 2. download files
# 3. unzip, overwrite file and rename
# 4. put binary or build exec


def os_type():
    os_name = platform.system()
    if os_name == 'Linux':
        return 'Linux'
    elif os_name == 'Windows':
        return 'Windows'
    elif os_name == 'Darwin':
        return 'Not support mac'
    else:
        return 'Not support OS'


def power_miner_url(os_type: str):
    if os_type == 'window':
        return WIN_MINER
    elif os_type == 'ubuntu18':
        return UBUNTU_1804_MINER
    elif os_type == 'ubuntu20':
        return UBUNTU_2004_MINER
    elif os_type == 'hiveos':
        return HIVEOS_MINER
    else:
        return null


def download_url(url, dst_folder, chunk_size=128):
    filename = Path(dst_folder, url.split('/')[-1])
    r = requests.get(url)

    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def download_folder(os_type: str):
    folder = Path(ROOT_PATH, 'build', os_type)
    os.makedirs(folder, exist_ok=True)
    print(f"create {folder}")
    return folder


def bin_folder(os_type: str):
    folder = Path(ROOT_PATH, 'bin', os_type)
    os.makedirs(folder, exist_ok=True)
    print(f"create {folder}")
    return folder


def unzip_each_file(src_file: str, dst_folder: str):
    with zipfile.ZipFile(src_file, 'r') as zf:
        for member in zf.namelist():
            filename = os.path.basename(member)
            if not filename:  # skip directories
                continue

            source = zf.open(member)
            target = open(os.path.join(dst_folder, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)


def untar_each_file(src_file: str, dst_folder: str):
    with tarfile.open(src_file, 'r') as tf:
        for member in tf.getmembers():
            if member.isreg():  # skip if the TarInfo is not files
                # remove the path by reset it
                member.name = os.path.basename(member.name)
                tf.extract(member, dst_folder)  # extract


def unzip_folder(src_folder: str, dst_folder: str):
    files = glob.glob(f"{src_folder}/*.zip") + \
        glob.glob(f"{src_folder}/*.tar.gz")

    for file in files:
        if file.split('.')[-1] == 'zip':
            unzip_each_file(file, dst_folder)
        elif file.split('.')[-1] == 'gz':
            untar_each_file(file, dst_folder)
        else:
            print('file type error')


def remove_patten_files(dst_folder: str, pattern: str = 'tonlib*'):
    files = glob.glob(f"{dst_folder}/{pattern}")
    for file in files:
        os.remove(file)


def downloader(os_type: str):
    if os_type in BUILD_PACK:
        folder = download_folder(os_type)
        urls = power_miner_url(os_type)
        for url in urls:
            download_url(url, folder)
    else:
        print('os_type error')


# os_type = 'ubuntu20'
# os_type = 'window'


for os_type in BUILD_PACK:
    src_folder = download_folder(os_type)
    dst_folder = bin_folder(os_type)
    downloader(os_type)
    unzip_folder(src_folder, dst_folder)

    [remove_patten_files(dst_folder, remove_patten)
     for remove_patten in REMOVE_PATTENS]
