# -*- coding: utf-8 -*-
from app import package
import pytest

@pytest.mark.parametrize("test_input, expected", [
    ('VERSION_ID="18.04"\n', 'ubuntu18'),
    ('VERSION_ID="20.04"\n', 'ubuntu20')
])
def test_get_ubuntu_version(test_input, expected):
    assert expected == package.get_ubuntu_version(test_input)
