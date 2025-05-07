import typing

import pydantic

import example.models.internal.utilities

def default(title: typing.Optional[str] = None, metaschema: str = "https://json-schema.org/draft/2020-12/schema", **kwargs: typing.Any) -> pydantic.ConfigDict:
    """
    Creates a configuration dictionary for a Pydantic model with specified default
    settings, while allowing additional custom configurations to be passed.

    The configuration includes options to handle attribute naming, string
    whitespace stripping, default validations, and serialization rules suitable
    for strict and explicit data modeling requirements.

    Additional References
    -------------------
    - `Pydantic Configuration`_.

    .. _Pydantic Configuration: https://docs.pydantic.dev/1.10/usage/model_config/

    Parameters
    ----------
    kwargs : pydantic.ConfigDict
        Additional configurations to override or extend the default values of the
        configuration dictionary.

    Returns
    -------
    pydantic.ConfigDict
        A configuration dictionary containing merged default settings and custom
        configurations. This can be applied to Pydantic model configuration.
    """

    if "json_schema_extra" not in kwargs:
        kwargs["json_schema_extra"] = {}

    if "json_schema_extra" in kwargs:
        kwargs["json_schema_extra"]["$schema"] = metaschema

        if title is not None:
            kwargs["json_schema_extra"]["title"] = title

    instance = pydantic.ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_default=True,
        strict=True,
        use_enum_values=True,
        use_attribute_docstrings=True,
        alias_generator=example.models.internal.utilities.snake_case_to_train_case_alias_generator,
        model_title_generator=example.models.internal.utilities.snake_case_to_train_case_model_title_generator,
        field_title_generator=example.models.internal.utilities.snake_case_to_train_case_field_title_generator,
        json_schema_serialization_defaults_required=True,
    )

    instance.update(**kwargs)

    return instance
