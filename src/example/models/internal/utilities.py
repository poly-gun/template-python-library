"""
General utilities.
"""
from __future__ import annotations

import re

import pydantic.fields

def pascal_to_train_case(s: str) -> str:
    """
    Converts a given string from PascalCase to train-case.

    This function takes a string written in PascalCase format and converts it
    to train-case by inserting a hyphen '-' before each uppercase character
    that is not at the beginning of the string. All uppercase letters are then
    converted to lowercase.

    :param s: A string in PascalCase format to be converted.
    :return: A new string in train-case format.
    """

    
    return re.sub(r"(?<!^)(?=[A-Z])", "-", s).lower()

def snake_case_to_train_case(snake: str) -> str:
    """
    Converts a snake_case string into train-case format.

    This function takes a string written in snake_case format, divides it by the
    underscore ('_') delimiter, converts all partial strings into lowercase, and
    concatenates them using a hyphen ('-'). The resulting format is known as
    train-case, commonly used in some programming contexts.

    Parameters
    ----------
    snake : str
        A string in snake_case format that needs to be converted into train-case.

    Returns
    -------
    str
        A string converted to train-case format.
    """

    partials = snake.split("_")

    return "-".join(partial.lower() for partial in partials).lower()

def snake_case_to_train_case_field_title_generator(field_name: str, info: pydantic.fields.FieldInfo | pydantic.fields.ComputedFieldInfo) -> str | None:
    partials = field_name.split("_")

    return "-".join(partial.lower() for partial in partials).lower()

def snake_case_to_train_case_model_title_generator(model: type) -> str | None:
    return pascal_to_train_case(model.__name__)

def snake_case_to_train_case_alias_generator(field_name: str) -> str | None:
    return snake_case_to_train_case(field_name)
