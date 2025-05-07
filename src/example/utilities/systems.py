"""
This module contains a set of classes extending pathlib.Path to provide enhanced file-system 
descriptors and utilities for working with file and directory permissions.

The module is well-suited for scenarios requiring advanced permission handling, 
such as file and directory validations in system-level applications.
"""

from __future__ import annotations

import logging
import os
import pathlib
import platform
import shutil
import stat
import tempfile
import typing

import packaging.version

logger = logging.getLogger(__name__)

def append_file_stem(path: pathlib.Path, addition: str) -> pathlib.Path:
    """
    Append a string to the stem of a file name while retaining its original extension.

    This function modifies the stem of the file represented by the given path
    by appending an additional string to it without altering the file's extension.
    The resulting path with the modified stem is returned as a `Path` object.

    :param path: Path object representing the input file path. Must be an instance of `pathlib.Path`.
    :param addition: String that will be appended to the stem of the file name.
    :return: A new `Path` object with the stem modified by appending the provided string.
    :rtype: pathlib.Path
    """

    if not isinstance(path, pathlib.Path):
        raise TypeError("Expected a pathlib.Path object, got {}".format(type(path)))

    instance = path.resolve().parent.joinpath("{}.{}.{}}".format(path.stem, addition, path.suffix.removeprefix(".")))

    return instance

class Descriptor(pathlib.Path):
    """
    Represents a file descriptor with additional methods to inspect its properties.

    The Descriptor class extends pathlib.Path and introduces several utility
    methods to assess various permissions and properties of the file or directory
    it represents. These include methods to check readability, writability, and
    executability for users and groups. This enhanced functionality is useful for
    system file validations and permission checks in applications.
    """

    try:
        if packaging.version.parse(platform.python_version()) < packaging.version.parse("3.12"):
            _flavour = getattr(type(pathlib.Path()), "_flavour")
    except AttributeError as e:
        ...

    def __init__(self, *args, **kwargs):
        try:
            super().__init__(*args)
        except TypeError as e:
            super().__init__()

    def get_current_permissions(self):
        """
        Retrieves the current file permissions of a file.

        This method extracts and returns the permission bits of the file represented
        by the current object using the `os.stat` system call. The permissions are
        retrieved in the form of an octal representation that corresponds to the
        standard Unix file permission notation (e.g., 0o755).

        Returns:
            int: The octal representation of the file permissions.

        Raises:
            OSError: If the file statistics cannot be retrieved.
        """

        statistics = os.stat(self)

        # st_mode & 0o777 extracts the last 9 bits of the st_mode attribute, which represent the file permissions.
        return statistics.st_mode & 0o777

    def has_permissions(self, permissions: int):
        """
        Determines if the current permissions match the specified permissions.

        The method compares the current permissions of the object or
        user with the given permissions value and evaluates if they
        are equivalent.

        Parameters
        ----------
        permissions : int
            The permissions value to check against the current
            permissions.

        Returns
        -------
        bool
            True if the current permissions match the specified permissions,
            otherwise False.
        """

        return self.get_current_permissions() == permissions

    def is_user_readable(self):
        """
        Determines if the descriptor is readable by the group.

        This method checks the permission flags of a file to ascertain if it has
        read permissions for the group associated with the file. It evaluates
        the file's mode and identifies if the group-readable flag is set.

        Returns
        -------
        bool
            True if the group has read permissions, otherwise False.
        """

        statistics = os.stat(self)

        return bool(statistics.st_mode & stat.S_IRUSR)

    def is_group_readable(self):
        """
        Determines if the descriptor is readable by the group.

        This method checks the permission flags of a file to ascertain if it has
        read permissions for the group associated with the file. It evaluates
        the file's mode and identifies if the group-readable flag is set.

        Returns
        -------
        bool
            True if the group has read permissions, otherwise False.
        """

        statistics = os.stat(self)

        return bool(statistics.st_mode & stat.S_IRGRP)

    def is_readable(self) -> bool:
        """
        Check if the given file or directory is readable.

        Returns
        -------
        bool
            True if the file or directory is readable, False otherwise.
        """

        return os.access(self, os.R_OK)

    def is_writable(self) -> bool:
        """
        Check if the given file or directory is writable.

        Returns
        -------
        bool
            True if the file or directory is writable, False otherwise.
        """

        return os.access(self, os.W_OK)

    def is_executable(self) -> bool:
        """
        Check if the given file is executable.

        Returns
        -------
        bool
            True if the file is executable, False otherwise.

        Notes
        -----
        This function first verifies that the given path is a file,
        then checks for executable permissions.
        """

        return self.is_file() and os.access(self, os.X_OK)

    @staticmethod
    def make_executable(descriptor: os.PathLike) -> None:
        """
        Changes the file permissions of the given file path to make it executable.

        This makes it (more or less) respect the umask that was in effect when the file
        was created: Executable is only set for those that can read.

        This method modifies the file's mode to ensure that the execute (X)
        permissions are granted to the file if the read (R) permissions are
        already present. It reads the current mode of the file, adjusts the
        permissions using bitwise operations, and applies the new mode
        to the file.

        Parameters
        ----------
        descriptor : os.PathLike
            The path to the file whose permissions need to be changed.

        Returns
        -------
        None
        """

        mode = os.stat(descriptor).st_mode
        mode |= (mode & 0o444) >> 2  # copy R bits to X
        os.chmod(descriptor, mode)

    @property
    def path(self):
        """
        Provides a property to convert the instance into a pathlib.Path object.

        This property returns a `pathlib.Path` representation of the object it is
        called on. It offers a convenient way to work with file system paths by
        transforming the object directly into a Path object.

        :return: A `pathlib.Path` object representation of the instance.
        :rtype: pathlib.Path
        """
        return pathlib.Path(self).resolve()

class Executable(Descriptor):
    """
    Represents an executable descriptor, with functionality to validate and set executable permissions.

    This class extends the Descriptor class and is used for managing objects that need to ensure they are executable.
    It provides mechanisms to validate an executable state and modify permissions where necessary. This is particularly
    useful for file-like objects or descriptors where executability is a requirement for their functionality. The class
    also provides property access for retrieving default permissions based on custom or default system settings.
    """

    def __init__(self, *args):
        """
        Initializes a new instance of the class with given arguments. Validates whether the descriptor
        is executable. If not, attempts to change its permissions and verifies success of the operation.
        Raises an exception if permission modification fails.

        Parameters
        ----------
        *args:
            Variable length argument list for initializing the instance.

        Raises
        ------
        RuntimeError:
            If the descriptor fails to become executable after attempting to change its permissions.
        """

        super().__init__(*args)

        if not self.is_executable():
            logger.debug("Descriptor is not executable: %s. Attempting to change permission(s): %s.", str(self.path.resolve()), str(0o775))

            os.chmod(self, 0o775, follow_symlinks=True)

            if not self.is_executable():
                logger.error("Failed to change permission(s) on Descriptor: %s", str(self.path.resolve()))

                raise RuntimeError("Failed to change permission(s) on Descriptor: {}".format(str(self.path.resolve())))
            else:
                logger.debug("Successfully changed permission(s) on Descriptor: %s", str(self.path.resolve()))

class Directory(Descriptor):
    @staticmethod
    def temporary(suffix: typing.Optional[str] = None, prefix: typing.Optional[str] = None):
        """
        Create and return a temporary directory. This has the same
        behavior as mkdtemp but can be used as a context manager. For
        example:

            with Directory.temporary() as tmpdir:
                ...
        """

        return Directory(tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=None), create=True)

    def __init__(self, *args, create: bool = True):
        super().__init__(*args)

        if create and not self.exists():
            logger.debug("Directory doesn't exist. Attempting to create: %s", str(self.path.resolve()))
            self.mkdir(parents=True, exist_ok=True)
            logger.debug("Successfully created directory descriptor: %s", str(self.path.resolve()))
        elif not self.exists():
            logger.error("Descriptor doesn't exist: %s", str(self.path.resolve()))
            raise RuntimeError("Descriptor doesn't exist: {}".format(str(self.path.resolve())))
        if not self.is_dir():
            logger.error("Descriptor is not a directory: %s", str(self.path.resolve()))
            raise RuntimeError("Descriptor is not a directory: {}".format(str(self.path.resolve())))

    def cleanup(self):
        shutil.rmtree(self)

    def __enter__(self):
        if not self.exists():
            logger.debug("Directory doesn't exist. Attempting to create: %s", str(self))
            self.mkdir(parents=True, exist_ok=True)
            logger.debug("Successfully created directory descriptor: %s", str(self))

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Manages the exit process of a context manager by handling exceptions and cleanup tasks.

        The `__exit__` method is a special method used in context managers to define clean-up actions
        that need to be performed after the execution of a block of code within a `with` statement.
        It ensures proper resource cleanup, such as closing files or network connections, and can
        also suppress exceptions if required by returning `True`.

        Parameters
        ----------
        exc_type : type | None
            The exception class of the error that occurred, or `None` if no exception was raised.
        exc_val : BaseException | None
            The instance of the exception that was raised, or `None` if no exception was raised.
        exc_tb : TracebackType | None
            The traceback object that provides the information of where the exception occurred,
            or `None` if no exception was raised.

        Returns
        -------
        bool
            Indicates whether the exception was handled and suppressed. If `True` is returned,
            the exception is suppressed. Otherwise, the exception is propagated to the caller.
        """

        self.cleanup()

        return False

class File(Descriptor):
    def __init__(self, *args, create: bool = False):
        super().__init__(*args)

        if create and not self.exists():
            logger.debug("File doesn't exist. Attempting to create: %s", str(self.path.resolve()))
            self.touch(exist_ok=True)
            logger.debug("Successfully created file descriptor: %s", str(self.path.resolve()))
        elif not self.exists():
            logger.error("Descriptor doesn't exist: %s", str(self.path.resolve()))
            raise RuntimeError("Descriptor doesn't exist: {}".format(str(self.path.resolve())))

        if not self.is_file():
            logger.error("Descriptor is not a file: %s", str(self.path.resolve()))
            raise RuntimeError("Descriptor is not a file: {}".format(str(self.path.resolve())))
