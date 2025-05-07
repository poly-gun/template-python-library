import contextlib
import json
import logging
import os
import pathlib
import sys
import tempfile
import typing
import dataclasses
import configparser

import example.utilities.colors

from tqdm import tqdm

import boto3
from botocore.config import Config
from botocore.client import ClientError

import example.api.types

logger = logging.getLogger(__name__)

@contextlib.contextmanager
def disable_ssl_warnings():
    import warnings
    import urllib3

    with warnings.catch_warnings():
        # warnings.filterwarnings("ignore", message="Unverified HTTPS request")
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        yield None

def write_aws_configurations(session_token: str, session_token_expiration: str, access_key: str, secret_key: str, region: str, profile_name: typing.Optional[str] = "default"):
    """
    Writes both an AWS ~/.aws/config and ~/.aws/credentials file using provided functional parameters.

    Parameters
    ----------
    session_token
    session_token_expiration
    access_key
    secret_key
    region
    profile_name

    Returns
    -------

    """

    if profile_name is None: profile_name = "default"

    credentials_file: pathlib.Path = pathlib.Path("~/.aws/credentials").expanduser()
    configuration_file: pathlib.Path = pathlib.Path("~/.aws/config").expanduser()

    # Ensure aws_session_token has quotes wrapping the value
    if not session_token.startswith("\"") or session_token.endswith("\""):
        session_token = session_token.removeprefix("\"")
        session_token = session_token.removesuffix("\"")

        session_token = "\"{}\"".format(session_token)

    if not credentials_file.parent.exists():
        logger.info("Creating AWS Configuration Parent Directory: %s", str(credentials_file.parent))

        credentials_file.parent.mkdir(parents=True, exist_ok=False)

    credentials = configparser.ConfigParser()

    credentials[profile_name] = {
        "aws_access_key_id": access_key,
        "aws_secret_access_key": secret_key,
        "aws_session_token": session_token,
        "aws_expiration": session_token_expiration,
    }

    logger.info("Writing AWS Credentials, Configuration File: %s", str(credentials_file))

    with open(credentials_file, "w") as f:
        credentials.write(f)

    configuration = configparser.ConfigParser()

    configuration[profile_name] = {
        "region": region,
        "output": "json"
    }

    logger.info("Writing AWS Configuration File: %s", str(configuration_file))

    with open(configuration_file, "w") as f:
        configuration.write(f)

@dataclasses.dataclass(frozen=True)
class Settings:
    profile: typing.Optional[str] = None
    region: str = os.getenv("AWS_REGION", "us-east-2")

    def __post_init__(self):
        validations = {
            "regions": ["us-east-2"]
        }

        if self.region not in validations["regions"]:  # --> update if company regions ever are added
            logger.error("Received Invalid AWS Region Specification: %s", self.region)

            raise ValueError("Invalid Region Provided: {}. Valid Region(s): {}".format(self.region, json.dumps(validations["regions"])))

@dataclasses.dataclass(frozen=True)
class AWS:
    settings: Settings = Settings()

    def __post_init__(self):
        if type(self) != AWS and isinstance(self, AWS):  # --> if the instance is a child of AWS
            try:
                logger.debug("Instantiating an AWS Client with Service: \"%s\"", self.service)
            except Exception as e:
                logger.error("Received Invalid AWS Service Specification: %s", e)

                raise e

    @property
    def service(self) -> str:
        """
        The AWS-related class's service name or identifier (as used to instantiate a boto3 service client).

        Raises
        ------
        NotImplementedError
            Raises a NotImplementedError only when attempting to call cls.service from the AWS base class.

        Returns
        -------
        The AWS service identifier (e.g. "sts").
        """

        raise NotImplementedError("AWS Base Class Has No Valid Service Method or Property")

    @property
    def client(self):
        configuration = Config(
            region_name=self.settings.region,
            retries={
                "max_attempts": 3,
                "mode": "standard"
            }
        )

        session = boto3.session.Session(profile_name=self.settings.profile)

        credentials = session.get_credentials()

        # if credentials cannot be found, and a tty is available to standard-input, prompt the user
        if credentials is None and sys.stdin.isatty():
            print("")
            print(example.utilities.colors.red("No AWS Credentials Were Found"))
            print("")
            print(example.utilities.colors.underline("Credentials can be retrieved via the AWS-CLI" + ":"))
            print("")
            print(example.utilities.colors.dim("  $ ") + example.utilities.colors.bold("aws configure get aws_access_key_id"))
            print("")
            print(example.utilities.colors.dim("  $ ") + example.utilities.colors.bold("aws configure get aws_secret_access_key"))
            print("")
            print(example.utilities.colors.dim("  $ ") + example.utilities.colors.bold("aws configure get aws_session_token"))
            print("")
            print(example.utilities.colors.dim("  $ ") + example.utilities.colors.bold("aws configure get aws_expiration"))
            print("")
            print(example.utilities.colors.dim("  $ ") + example.utilities.colors.bold("aws configure get region"))
            print("")

            aws_access_key_id = input("AWS Access Key ID: ").strip()

            aws_secret_access_key = input("AWS Secret Access Key: ").strip()

            aws_session_token = input("AWS Session Token: ").strip()

            aws_session_token_timeout = input("AWS Session Expiration: ").strip()

            aws_region = input("AWS Region: ").strip()

            os.environ["AWS_DEFAULT_REGION"] = aws_region

            write_aws_configurations(aws_session_token, aws_session_token_timeout, aws_access_key_id, aws_secret_access_key, region=aws_region, profile_name=self.settings.profile)

            session = boto3.session.Session(
                profile_name=self.settings.profile
            )

            credentials = session.get_credentials()

            if credentials is None:
                raise ValueError("No AWS Credentials Were Found")

        instance = session.client(self.service, verify=True, config=configuration)

        return instance

@dataclasses.dataclass(frozen=True)
class STS(AWS):
    @property
    def service(self):
        return "sts"

    def get_caller_identity(self) -> dict:
        """
        Returns details about the IAM user or role whose credentials are used to call the operation.
        """

        logger.debug("Attempting to Call AWS Get-Caller-Identity")

        return self.client.get_caller_identity()

@dataclasses.dataclass(frozen=True)
class IAM(AWS):
    @property
    def service(self):
        return "iam"

@dataclasses.dataclass(frozen=True)
class S3(AWS):
    @property
    def service(self):
        return "s3"

    def access(self, bucket_name: str):
        """
        Verifies that the bucket exists and the client has access.

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/head_bucket.html

        Parameters
        ----------
        client
        bucket_name

        Returns
        -------

        """

        logger.debug("Attempting to Verify Access to Bucket \"%s\"", bucket_name)

        try:
            self.client.head_bucket(Bucket=bucket_name)
            # client.get_bucket_location(Bucket=bucket_name)
        except ClientError as e:
            if e.response['Error']['Code'] == "ExpiredToken":
                logger.error("Expired AWS Access Token")
                return False
            elif e.response['Error']['Code'] == "NoSuchBucket":
                logger.error("No Such Bucket \"%s\"", bucket_name)
                return False
            elif e.response['Error']['Code'] == "400" or e.response['Error']['Code'] == 400:
                logger.error("Bad Request - Likely Unauthenticated AWS Session: %s", e.response)
                return False

            logger.error("Unhandled Exception: %s", e)
            return False

        logger.info("Successfully Verified Access to Bucket \"%s\"", bucket_name)
        return True

    def list(self, configuration: example.api.types.S3.List):
        contents = []

        with disable_ssl_warnings():
            bucket_name = configuration.bucket_name

            prefix = configuration.key.removeprefix("/")
            # if not prefix.startswith("/"):
            #     prefix = "/" + prefix
            #
            # if not prefix.endswith("/"):
            #     prefix += "/"

            logger.debug("Attempting to List \"%s\" from \"%s\"", prefix, bucket_name)

            paginator = self.client.get_paginator("list_objects_v2")
            iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

            for page in iterator:
                if "Contents" in page:
                    for item in page["Contents"]:
                        item["LastModified"] = item["LastModified"].timestamp()
                        contents.append(item)

        return contents

    def download(self, configuration: example.api.types.S3.Download) -> pathlib.Path:
        """
        Attempts to download a file from an S3 bucket to a local directory. Ensures the file's
        existence and validity after download. Optionally utilizes a progress bar for manual
        execution in supported environments.

        Parameters
        ----------
        configuration : example.api.types.S3.Download
            Contains configuration details for the S3 download, including `key`, `bucket_name`,
            and optional `directory`.

        Returns
        -------
        pathlib.Path
            Local filesystem path to the downloaded file.

        Raises
        ------
        RuntimeError
            If the downloaded file does not exist or is not valid.
        """
        with disable_ssl_warnings():
            key = configuration.key
            bucket_name = configuration.bucket_name
            directory = configuration.directory

            logger.debug("Attempting to Download \"%s\" from \"%s\"", key, bucket_name)

            response = self.client.head_object(Bucket=bucket_name, Key=key.removeprefix("/"))

            size = response["ContentLength"]

            logger.debug("Total S3 Object Size (%s): %s", key, str(size))

            filename = os.path.basename(key)

            if directory is None:
                directory = tempfile.mkdtemp(prefix="{}-".format("aws-s3-bucket-objects"))
            else:
                # --> ensure the directory exists (@TODO Specify mode and permissions)
                os.makedirs(directory, exist_ok=True)

                logger.debug("Using User-Provided Directory: %s", directory)

            target = os.path.join(directory, filename)

            logger.debug("Downloading S3 Object: file://%s", target)

            # --> display progress bar if output device is capable, and environment isn't CI.
            if os.isatty(sys.stdout.fileno()) and (os.getenv("CI", default="") == "" or os.getenv("CI", default="") == "false"):
                with tqdm(total=size, unit="B", unit_scale=True) as progress:
                    with open(target, "wb") as file:
                        self.client.download_fileobj(bucket_name, key, file, Callback=progress.update)
            else:
                with open(target, "wb") as f:
                    self.client.download_fileobj(bucket_name, key.removeprefix("/"), f)

            if not (pathlib.Path(target).exists() and pathlib.Path(target).is_file()):
                raise RuntimeError("Local S3 Downloaded File Does Not Exist or Isn't a Valid File.")

            return pathlib.Path(target)

    def upload(self, configuration: example.api.types.S3.Upload) -> typing.Tuple[str, int]:
        """
        Uploads a file from a local source to an S3 bucket with optional progress bar
        display, verifying the source file's existence and validity before execution.
        Handles uploading large files and optimizes the user experience for capable
        output devices.

        Parameters
        ----------
        configuration : example.api.types.S3.Upload
            Configuration object containing details about the upload operation. It
            includes the key (S3 destination path), bucket_name (S3 bucket), and
            source (path to the local file being uploaded).

        Returns
        -------
        tuple of (str, int)
            A tuple where the first element is the key (S3 destination path) and the
            second element is the size of the uploaded file in bytes.

        Raises
        ------
        RuntimeError
            If the source file does not exist or is not a valid file.
        """

        with disable_ssl_warnings():
            key = configuration.key.removeprefix("/")
            bucket_name = configuration.bucket_name
            source = configuration.source
            extra_args = configuration.extra_arguments

            if not source.exists():
                raise RuntimeError("Source Does Not Exist.")
            if not source.is_file():
                raise RuntimeError("Source Isn't a Valid File.")

            logger.debug("Attempting to Upload \"%s\" from \"%s\" to \"%s\"", key, source, bucket_name)

            size: int = os.path.getsize(source)

            # --> display progress bar if output device is capable, and environment isn't CI.
            if os.isatty(sys.stdout.fileno()) and (os.getenv("CI", default="") == "" or os.getenv("CI", default="") == "false"):
                with tqdm(total=size, unit="B", unit_scale=True) as progress:
                    self.client.upload_file(source, bucket_name, key, ExtraArgs=extra_args, Callback=progress.update)
            else:
                self.client.upload_file(source, bucket_name, key, ExtraArgs=extra_args)

            return key, size

    def delete(self, configuration: example.api.types.S3.Delete):
        with disable_ssl_warnings():
            key = configuration.key
            bucket_name = configuration.bucket_name

            logger.debug("Attempting to Delete \"%s\" from \"%s\"", key, bucket_name)

            self.client.delete_object(Bucket=bucket_name, Key=key.removeprefix("/"))
