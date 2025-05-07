import dataclasses
import pathlib

@dataclasses.dataclass
class S3:
    """
    Represents an interface for Amazon S3-related operations.

    Provides structured data for organizing and managing Amazon S3 interaction,
    specifying configuration for various s3-specific operations.
    """

    @dataclasses.dataclass
    class Download:
        """
        Represents an s3 download configuration.

        This class holds metadata necessary for performing a download operation.
        It includes details such as the identifier for the resource, the storage
        bucket name, and the directory path where the downloaded data will be saved.

        Attributes
        ----------
        key : str
            Identifier for the resource to download, typically a file key or path.
        bucket_name : str
            Name of the storage bucket from which the resource is to be downloaded.
        directory : pathlib.Path
            Path to the local directory where the downloaded resources will be saved.

        Notes
        -----
        See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.S3Transfer.ALLOWED_DOWNLOAD_ARGS for
        additional arguments.
        """
        key: str
        bucket_name: str
        directory: pathlib.Path

    @dataclasses.dataclass
    class Upload:
        """
        Represents an s3 upload configuration.

        This class defines the essential details for uploading a file to an
        S3-compliant storage system. It contains information about the target
        bucket, the file key, and the local source file location. This can be
        used as part of a larger system to manage file uploads to cloud storage.

        Attributes
        ----------
        key : str
            The unique identifier for the file in the bucket.
        bucket_name : str
            Name of the bucket where the file will be uploaded.
        source : pathlib.Path
            Local path to the file that needs to be uploaded.

        Notes
        -----
        See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.S3Transfer.ALLOWED_UPLOAD_ARGS
        for additional arguements.
        """

        key: str
        bucket_name: str
        source: pathlib.Path

        extra_arguments: dict[str, any] = None

    @dataclasses.dataclass
    class Delete:
        key: str
        bucket_name: str

    @dataclasses.dataclass
    class List:
        key: str
        bucket_name: str
