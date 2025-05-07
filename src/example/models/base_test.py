import json
import pathlib
import shutil
import tempfile

import pytest
import logging

import example.models.base

logger = logging.getLogger(__name__)

def test_base_instance_working_directory(request: pytest.FixtureRequest):
    """
    Tests the working directory exists.
    """

    instance = example.models.base.Base()

    assert instance.working_directory.exists()
    assert instance.working_directory.is_absolute()

def test_base_instance_default_artifacts_directory(request: pytest.FixtureRequest):
    temporary = pathlib.Path(tempfile.gettempdir()).joinpath(request.node.name)

    temporary.mkdir(parents=True, exist_ok=True)

    instance = example.models.base.Base(working_directory=temporary)

    try:
        assert not instance.artifacts_directory.exists()

        assert not pathlib.Path("artifacts").exists()

        assert instance.artifacts_directory.is_absolute()

        assert instance.artifacts_directory.name == "artifacts"
    finally:
        shutil.rmtree(temporary, ignore_errors=True)

def test_base_instance_create_working_directory(request: pytest.FixtureRequest):
    temporary = pathlib.Path(tempfile.gettempdir()).joinpath(request.node.name)

    temporary.mkdir(parents=True, exist_ok=True)

    instance = example.models.base.Base(working_directory=temporary, create_working_directory=True)

    try:
        assert instance.working_directory.exists()
        assert instance.working_directory.is_absolute()
        assert instance.working_directory.name == request.node.name
    finally:
        shutil.rmtree(temporary, ignore_errors=True)

def test_base_instance_create_artifacts_directory(request: pytest.FixtureRequest):
    temporary = pathlib.Path(tempfile.gettempdir()).joinpath(request.node.name)

    temporary.mkdir(parents=True, exist_ok=True)

    instance = example.models.base.Base(working_directory=temporary, create_artifacts_directory=True)

    try:
        assert instance.artifacts_directory.exists()
        assert instance.artifacts_directory.is_absolute()
        assert instance.artifacts_directory.name == "artifacts"
    finally:
        shutil.rmtree(temporary, ignore_errors=True)

def test_base_instance_model(request: pytest.FixtureRequest):
    """
    Tests the functionality of the base instance model by checking the JSON
    dump output and cleaning up temporary files created during execution.
    """

    instance = example.models.base.Base()

    v = instance.model_dump_json(indent=4, by_alias=True)

    logger.debug("Model: %s", v)

def test_base_instance_model_schema(request: pytest.FixtureRequest):
    """
    Tests the model JSON schema of the Base instance.
    """

    instance = example.models.base.Base()

    v = instance.model_json_schema()
    content = json.dumps(v, indent=4, sort_keys=False)

    logger.debug("Schema: %s", content)
