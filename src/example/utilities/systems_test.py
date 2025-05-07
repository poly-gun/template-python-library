import os

import logging

import pytest

import example.utilities.systems

logger = logging.getLogger(__name__)

def test_descriptor(request: pytest.FixtureRequest):
    instance = example.utilities.systems.Descriptor("{}.test".format(request.node.name))

    assert instance.exists() is False

    assert isinstance(instance, example.utilities.systems.Descriptor)

def test_descriptor_file(request: pytest.FixtureRequest):
    instance = example.utilities.systems.Descriptor("{}.test".format(request.node.name))

    assert instance.exists() is False

    instance.touch()

    assert instance.exists() is True

    assert instance.is_file() is True

    instance.unlink(missing_ok=False)

    assert instance.exists() is False

def test_descriptor_directory(request: pytest.FixtureRequest):
    instance = example.utilities.systems.Descriptor("{}.test".format(request.node.name))

    assert instance.exists() is False

    instance.mkdir(parents=True, exist_ok=False)

    assert instance.exists() is True

    assert instance.is_file() is False
    assert instance.is_dir() is True

    instance.rmdir()

    assert instance.exists() is False

def test_directory_temporary(request: pytest.FixtureRequest):
    instance = example.utilities.systems.Directory.temporary()

    assert instance.exists() is True

    with instance as directory:
        assert directory.exists() is True

    assert directory.exists() is False

