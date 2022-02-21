import glob
import shutil
import tarfile
import zipfile
from pathlib import Path

import requests
from loguru import logger

VERSION = '20211230.1'
BASE_URL = f'https://github.com/tontechio/pow-miner-gpu/releases/download/{VERSION}'

HIVEOS_VERSION = 'h.20211230.1'
HIVEOS_BASE_URL = f'https://github.com/tontechio/pow-miner-gpu-hiveos/releases/download/{HIVEOS_VERSION}'

MINER_TOOLS = {
    'windows': [
        f'{BASE_URL}/minertools-cuda-windows-x86-64.zip',
        f'{BASE_URL}/minertools-opencl-windows-x86-64.zip',
    ],
    'ubuntu18': [
        f'{BASE_URL}/minertools-cuda-ubuntu-18.04-x86-64.tar.gz',
        f'{BASE_URL}/minertools-opencl-ubuntu-18.04-x86-64.tar.gz',
    ],
    'ubuntu20': [
        f'{BASE_URL}/minertools-cuda-ubuntu-20.04-x86-64.tar.gz',
        f'{BASE_URL}/minertools-opencl-ubuntu-20.04-x86-64.tar.gz',
    ],
    'hiveos': [
        f'{HIVEOS_BASE_URL}/tonminer_opencl_hiveos_x86_64-{HIVEOS_VERSION}.tar.gz',
        f'{HIVEOS_BASE_URL}/tonminer_cuda_hiveos_x86_64-{HIVEOS_VERSION}.tar.gz',
    ],
}

IGNORE_PATTENS = ['*.sh', 'tonlib*', '*.service', 'release.json', '*.conf', '*.json', '*.md']

PROJECT_ROOT_PATH = Path(__file__).parents[1].resolve()


def download_url(url, dst_folder, chunk_size=128):
    filename = Path(dst_folder, url.split('/')[-1])
    logger.info(f'Download {url}')
    r = requests.get(url)

    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def create_download_folder(os_type: str):
    folder = Path(PROJECT_ROOT_PATH, 'build', os_type)
    folder.mkdir(exist_ok=True)
    logger.info(f'Create {folder}')
    return folder


def create_bin_folder(os_type: str):
    folder = Path(PROJECT_ROOT_PATH, 'bin', os_type)
    folder.mkdir(exist_ok=True)
    logger.info(f'Create {folder}')
    return folder


def unzip_file(src_file: str, dst_folder: str):
    logger.info(f'Unzip {src_file}')
    with zipfile.ZipFile(src_file, 'r') as zf:
        for member in zf.namelist():
            filename = Path(memeber).name
            if not filename:  # skip directories
                continue

            with zf.open(memeber) as source, Path(dst_folder, filename).open('wb') as target:
                shutil.copyfileobj(source, target)


def untar_file(src_file: str, dst_folder: str):
    logger.info(f'Untar {src_file}')
    with tarfile.open(src_file, 'r') as tf:
        for member in tf.getmembers():
            if member.isreg():  # skip if the TarInfo is not files
                # remove the path by reset it
                member.name = Path(member.name).name
                tf.extract(member, dst_folder)  # extract


def unarchive_each_files(src_folder: str, dst_folder: str):
    logger.info('Unarchive')

    for file in Path(src_folder).glob('*.zip'):
        unzip_file(file, dst_folder)
    for file in Path(src_folder).glob('*.tar.gz'):
        untar_file(file, dst_folder)


def remove_patten_files(dst_folder: str, pattern: str = 'tonlib*'):
    for file in Path(dst_folder).glob(pattern):
        logger.info(f'Remove {file}')
        file.unlink()


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
