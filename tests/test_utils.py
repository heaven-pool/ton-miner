# -*- coding: utf-8 -*-
from pathlib import Path

import pytest
from app.libs import utils

DATA_PATH = Path(__file__).parent.resolve() / "data"


@pytest.mark.parametrize("test_input, expected", [
    ("VERSION_ID="18.04"\n", "ubuntu18"),
    ("VERSION_ID="20.04"\n", "ubuntu20")
])
def test_get_ubuntu_version(test_input, expected):
    assert expected == utils.get_ubuntu_version(test_input)


@pytest.mark.parametrize("test_input, expected", [
    ("VERSION_ID="win"\n", "Error"),
    ("VERSION_ID="not match"\n", "Error")
])
def test_get_ubuntu_version_throw_error(test_input, expected):
    with pytest.raises(NotImplementedError):
        utils.get_ubuntu_version(test_input)


@pytest.mark.parametrize("os_type, binfile, expected", [
    ("windows", "cuda", "win-cuda.exe"),
    ("windows", "opencl", "win-opencl.exe"),
    ("ubuntu18", "cuda", "ubuntu18-cuda"),
    ("ubuntu18", "opencl", "ubuntu18-opencl"),
    ("hiveos", "cuda", "ubuntu18-cuda"),
    ("hiveos", "opencl", "ubuntu18-opencl"),
    ("ubuntu20", "cuda", "ubuntu20-cuda"),
    ("ubuntu20", "opencl", "ubuntu20-opencl"),
])
def test_get_bin_path(os_type, binfile, expected):
    assert expected in str(utils.get_bin_path(os_type, binfile))


@pytest.mark.parametrize("test_input, expected", [
    ("NVIDIA CUDA GeForce GTX 1050 Ti on PCI bus 3 slot 0", "cuda"),
    ("AMD OPENCL GeForce GTX 1050 Ti on PCI bus 3 slot 0", "opencl")
])
def test_get_gpu_vender(test_input, expected):
    assert expected == utils.get_gpu_vender(test_input)


@pytest.mark.parametrize("test_input, expected", [
    (b"[ GPU #0: SM 6.1 GeForce GTX 1050 Ti ]\x1b[0m\n", ""),
    (b"\x1b[1;36m[ 3][t 0][2022-02-05 14:57:03.329795978][Miner.cpp:105]\t[ mining in progress, passed: 10.0s, hashes computed: 3615490048, instant speed: 368.285 Mhash/s, average speed: 361.073 Mhash/s ]\x1b[0m\n", "361.073"),
    (b"\x1b[1;36m[ 3][t 0][2022-02-05 14:56:58.323761700][Miner.cpp:105]\t[ mining in progress, passed: 5006.4ms, hashes computed: 1769996288, instant speed: 365.831 Mhash/s, average speed: 353.546 Mhash/s ]\x1b[0m\n", "353.546"),
])
def test_parse_log_to_hashrate(test_input, expected):
    assert expected == utils.parse_log_to_hashrate(test_input)


@pytest.mark.parametrize("test_input, expected", [
    (b"[ GPU #0: SM 6.1 GeForce GTX 1050 Ti ]\x1b[0m\n", ""),
    (b"\x1b[1;36m[ 3][t 0][2022-02-05 14:56:58.323761700][Miner.cpp:105]\t[ mining in progress, passed: 5006.4ms, hashes computed: 1769996288, instant speed: 365.831 Mhash/s, average speed: 353.546 Mhash/s ]\x1b[0m\n", ""),
    (b"[ 3][t 0][2022-02-07 17:50:02.6306916][Miner.cpp:105]\t[ done, passed: 71.6s, hashes computed: 100394860544, instant speed: 1385.999 Mhash/s, average speed: 1402.768 Mhash/s ]\n", "done"),

])
def test_parse_log_to_hashrate(test_input, expected):
    assert expected == utils.parse_log_to_done(test_input)


@pytest.mark.parametrize("test_input, expected", [
    (str(Path(DATA_PATH, "miner.boc")),
        "b5ee9c724101020100a100014589ff4923ac7e0f74fddf69973ed0a9099d2113ab575d92f82b0b0445e0994b2553580c010"
        + "0f24d696e650061bb618e5690d2aacc203003dbe333046683b698ef945ff250723c0f73297a2a1a41e2f1e0af0082da653"
        + "22d1b2ce87eca953a4d74f96cea303b34d6497980c136d82144acda33755876665780bae9be8a4d6385e0af0082da65322"
        + "d1b2ce87eca953a4d74f96cea303b34d6497980c136d82144eb712649"),
])
def test_readfile_to_hexstring(test_input, expected):
    assert expected == utils.readfile_to_hexstring(test_input)
