import pytest
import logging

import example.internal.versioning

logger = logging.getLogger(__name__)

def test_versioning_instance():
    instance = example.internal.versioning.Version()

    logger.debug("Version: %s", instance)

    assert instance

def test_versioning_tuple():
    assert isinstance(example.internal.versioning.Version().tuple, tuple)

def test_versioning_string_dunder_method():
    assert len(str(example.internal.versioning.Version()).split(".")) == 3
