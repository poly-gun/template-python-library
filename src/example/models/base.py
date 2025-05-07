"""
The base module for fragrance models.
"""
import os
import tempfile
import typing
import pathlib
import logging

import pydantic

import example.models.internal.base
import example.models.configuration

from pydantic import Field, WithJsonSchema

logger = logging.getLogger(__name__)

class Base(example.models.internal.base.Model):
    """
    A base class representing a fragrance input-output model.
    """

    model_config = example.models.configuration.default()

    working_directory: typing.Annotated[pydantic.DirectoryPath, Field(strict=False), WithJsonSchema({})] = Field(default=".", description="The program's runtime working directory. Any other relative directories will be constructed using this option unless explicitly specified. Implementations executing subprocess(es) should set the PID's executing directory to such value. By default, this directory is not created. See the \"create-working-directory\" option for changing the default behavior.")
    create_working_directory: bool = Field(default=False, description="Whether to create the working directory if it doesn't already exist.")

    artifacts_directory: typing.Annotated[pathlib.Path, Field(strict=False), WithJsonSchema({})] = Field(default="artifacts", description="The parent directory that's used for storing output artifacts. If the value is relative, it will be resolved using the \"working-directory\". By default, the directory will not be created. See the \"create-artifacts-directory\" option for changing the default behavior.")
    create_artifacts_directory: bool = Field(default=False, description="Whether to create the artifacts directory if it doesn't already exist.")

    temporary_directory: typing.Annotated[pathlib.Path, Field(strict=False), WithJsonSchema({"x-external-documentation": "https://docs.python.org/3/library/tempfile.html#tempfile.gettempdir"})] = Field(default=tempfile.gettempdir(), description="The parent directory that's used for storing temporary files. By default, the value is computed using the operating system's temporary specification. If the user's specification is different than the OS' default, then changes to \"tempfile.tempdir\" will be directly applied. If the path doesn't exist, it will be created.")

    def model_post_init(self, __context: typing.Any) -> None:
        """
        Executes post-initialization tasks for a model instance.

        Parameters
        ----------
        __context : Any
            Contextual information or objects passed to the post-initialization
            routine. Specific usage may vary based on implementation requirements.

        Returns
        -------
        None
            This method does not return any value but performs operations as
            described in the summary section.
        """

        # Evaluate the temporary directory.
        default_tempdir = tempfile.gettempdir()

        logger.debug("Default Temporary Directory: %s", str(default_tempdir))

        # Resolve the temporary directory's full system path if applicable.
        if self.temporary_directory.is_absolute() is False:
            self.temporary_directory = self.temporary_directory.resolve()

        # Create the user-specified temporary directory if it differs from the default, and create it
        # if it doesn't already exist.
        if str(self.temporary_directory) != default_tempdir:
            logger.debug("Evaluating User-Specified Temporary Directory: %s", str(self.temporary_directory))
            if self.temporary_directory.exists() is False:
                logger.debug("Creating User-Specified Temporary Directory: %s", str(self.temporary_directory))

                self.temporary_directory.mkdir(parents=True, exist_ok=True)

            if self.temporary_directory.exists() is False:
                raise RuntimeError("Unable to create temporary directory: %s" % str(self.temporary_directory))

            # Update the tempfile.tempdir's global runtime variable
            tempfile.tempdir = str(self.temporary_directory)

            logger.debug("Updated tempfile.tempdir to: %s", str(tempfile.tempdir))

        logger.debug("Unevaluated Working Directory: %s", str(self.working_directory))
        # Set directory to the process's current working directory if default.
        if str(self.working_directory) == ".":
            self.working_directory = pathlib.Path(os.getcwd()).resolve()

        logger.debug("Resolved Working Directory: %s", str(self.working_directory))

        # Set the artifacts directory to a full system path, relative to the working directory, if the value is relative.
        if self.artifacts_directory.is_absolute() is False:
            self.artifacts_directory = self.working_directory.joinpath(self.artifacts_directory).resolve()

        # Verify the directory is a valid directory if already exists.
        if self.working_directory.exists() and self.working_directory.is_dir() is False:
            raise ValueError(f"Working directory '{self.working_directory}' is not a valid directory.")
        elif not self.working_directory.exists() and self.create_working_directory:
            self.working_directory.mkdir(parents=True, exist_ok=True)

        logger.debug("Verified Valid Working Directory: %s. Exists: %s", str(self.working_directory), str(self.working_directory.exists()))

        if self.artifacts_directory.exists() and self.artifacts_directory.is_dir() is False:
            raise ValueError(f"Artifacts directory '{self.artifacts_directory}' is not a valid directory.")
        elif not self.artifacts_directory.exists() and self.create_artifacts_directory:
            self.artifacts_directory.mkdir(parents=True, exist_ok=True)

        logger.debug("Verified Valid Artifacts Directory: %s. Exists: %s", str(self.artifacts_directory), str(self.artifacts_directory.exists()))
