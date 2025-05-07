import pytest

import os
import logging

import example.api.aws

logger = logging.getLogger(__name__)

@pytest.mark.description("Unit-Test that verifies the AWS settings dataclass object happy-path and default behavior.")
def test_settings_object():
    instance = example.api.aws.Settings()

    assert instance.region == "us-east-2"

    logger.info("Verified Default Settings Region Attribute")

@pytest.mark.description("Unit-Test that verifies the AWS settings dataclass object (class) __post_init__ constructor.")
def test_settings_object_post_initialization():
    try:
        example.api.aws.Settings(region="aws-invalid-region")
    except ValueError:
        logger.info("Successfully Caught ValueError Exception for Invalid AWS Region Specification")
    except Exception as e:
        pytest.fail("Expected ValueError - Received: {}".format(e))

@pytest.mark.description("Unit-Test that verifies runtime logic and variability of the AWS base class.")
def test_base_class():
    instance = example.api.aws.AWS()

    assert isinstance(instance.settings, example.api.aws.Settings)

    try:
        client = instance.client
    except NotImplementedError:
        logger.info("Successfully Caught NotImplementedError Exception for Base AWS Instance")
    except Exception as e:
        pytest.fail("Expected NotImplementedError - Received: {}".format(e))

    class Test(example.api.aws.AWS):
        ...

    logger.debug("Testing Subclass of AWS without Implementing Test.service Property Method")

    try:
        Test()
    except NotImplementedError:
        logger.info("Successfully Caught NotImplementedError For Invalid Instance of AWS Base Class")
    except Exception as e:
        pytest.fail("Expected NotImplementedError - Received: {}".format(e))

@pytest.mark.description("Unit-Test that verifies instantiation of the STS class, a subclass of AWS.")
def test_sts():
    instance: example.api.aws.STS | None = None

    try:
        instance = example.api.aws.STS()
    except Exception as e:
        pytest.fail("Expected Successful Instantiation - Received Exception: {}".format(e))

    assert instance is not None

    logger.info("Successfully Instantiated AWS Instance for Service: \"%s\"", instance.service)

@pytest.mark.description("Unit-Test that verifies instantiation of a boto3 client.")
@pytest.mark.skipif(os.getenv("CI") == "true", reason="AWS authentication isn't available in CI environment(s)")
def test_sts_client():
    instance = example.api.aws.STS()

    assert instance.client is not None
