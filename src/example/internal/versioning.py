"""
The versioning module provides a dataclass for working with the auto-generated `__version__.py` file.
"""
import typing

import packaging
import packaging.version

import logging

import dataclasses


logger = logging.getLogger(__name__)

@dataclasses.dataclass
class Version:
    """
    Represents a version with major, minor, and micro components.

    This class is designed to parse a version string from an external module
    (if available) and provide utilities to work with version data, such as
    accessing the version in tuple form or converting it to a string.

    :ivar tuple: A tuple representing the version in the form (major, minor,
        micro). Defaults to (0, 0, 0) if no external version is found.
    :type tuple: tuple[int, int, int]

    :ivar literal: The literal version string imported from an external module.
        This may not be available if the module is not found.
    :type literal: str
    """

    tuple: typing.Tuple[int, int, int] = (0, 0, 0)

    def __post_init__(self):
        try:
            import example.internal.__version__

            string = example.internal.__version__.version

            self.literal = string

            v = packaging.version.parse(string)

            self.tuple = (v.major, v.minor, v.micro)
        except ModuleNotFoundError as e:
            logger.warning("Unable to import version information from __version__.py: %s", str(e))

    def __str__(self):
        return "%d.%d.%d" % self.tuple
