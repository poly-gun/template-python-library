import json

import pydantic
import pytest
import logging

import example.models.configuration as module

logger = logging.getLogger(__name__)

def test_model_title(request: pytest.FixtureRequest):
    """
    Tests that the model's title is lowercase.
    """

    class Instance(pydantic.BaseModel):
        model_config = module.default()

    instance = Instance()

    schema = instance.model_json_schema()

    content = json.dumps(schema, indent=4)

    logger.info("[%s] Content: %s", request.node.name, content)

    assert schema["title"] == "instance"

def test_model_docstring(request: pytest.FixtureRequest):
    """
    Tests that the model's description is extracted from the docstring.
    """

    class Instance(pydantic.BaseModel):
        """
        Test Schema Description
        """

        model_config = module.default()

    instance = Instance()

    schema = instance.model_json_schema()

    content = json.dumps(schema, indent=4)

    logger.info("[%s] Content: %s", request.node.name, content)

    assert "description" in schema

    assert schema["description"] == "Test Schema Description"

def test_field_aliases(request: pytest.FixtureRequest):
    """
    Tests that the model's field aliases are correctly set to train-case, as well as their titles.
    """
    class Instance(pydantic.BaseModel):
        model_config = module.default()

        example_field_name: str = pydantic.Field(...)

    instance = Instance(example_field_name="test-value")

    schema = instance.model_json_schema()

    content = json.dumps(schema, indent=4)

    logger.info("[%s] Content: %s", request.node.name, content)

    assert "example-field-name" in schema["properties"]

    assert schema["properties"]["example-field-name"]["title"] == "example-field-name"
