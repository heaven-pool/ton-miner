# -*- coding: utf-8 -*-
import pytest
from app.libs import utils


@pytest.mark.parametrize("test_input, expected", [
    ('VERSION_ID="18.04"\n', 'ubuntu18'),
    ('VERSION_ID="20.04"\n', 'ubuntu20')
])
def test_get_ubuntu_version(test_input, expected):
    assert expected == utils.get_ubuntu_version(test_input)


@pytest.mark.parametrize("test_input, expected", [
    ('VERSION_ID="win"\n', 'Error'),
    ('VERSION_ID="not match"\n', 'Error')
])
def test_get_ubuntu_version_throw_error(test_input, expected):
    with pytest.raises(NotImplementedError):
        utils.get_ubuntu_version(test_input)


@pytest.mark.parametrize("os_type, binfile, expected", [
    ('windows', 'cuda', 'win-cuda.exe'),
    ('windows', 'opencl', 'win-opencl.exe'),
    ('ubuntu18', 'cuda', 'ubuntu18-cuda'),
    ('ubuntu18', 'opencl', 'ubuntu18-opencl'),
    ('hiveos', 'cuda', 'ubuntu18-cuda'),
    ('hiveos', 'opencl', 'ubuntu18-opencl'),
    ('ubuntu20', 'cuda', 'ubuntu20-cuda'),
    ('ubuntu20', 'opencl', 'ubuntu20-opencl'),
])
def test_get_bin_path(os_type, binfile, expected):
    assert expected in str(utils.get_bin_path(os_type, binfile))


@pytest.mark.parametrize("test_input, expected", [
    ('NVIDIA CUDA GeForce GTX 1050 Ti on PCI bus 3 slot 0', 'cuda'),
    ('AMD OPENCL GeForce GTX 1050 Ti on PCI bus 3 slot 0', 'opencl')
])
def test_get_gpu_vender(test_input, expected):
    assert expected == utils.get_gpu_vender(test_input)


@pytest.mark.parametrize("test_input, expected", [
    (b'[ GPU #0: SM 6.1 GeForce GTX 1050 Ti ]\x1b[0m\n', ''),
    (b'\x1b[1;36m[ 3][t 0][2022-02-05 14:57:03.329795978][Miner.cpp:105]\t[ mining in progress, passed: 10.0s, hashes computed: 3615490048, instant speed: 368.285 Mhash/s, average speed: 361.073 Mhash/s ]\x1b[0m\n', '361.073'),
    (b'\x1b[1;36m[ 3][t 0][2022-02-05 14:56:58.323761700][Miner.cpp:105]\t[ mining in progress, passed: 5006.4ms, hashes computed: 1769996288, instant speed: 365.831 Mhash/s, average speed: 353.546 Mhash/s ]\x1b[0m\n', '353.546'),
])
def test_parse_log_to_hashrate(test_input, expected):
    assert expected == utils.parse_log_to_hashrate(test_input)
