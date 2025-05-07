import pydantic

import example.models.configuration

class Model(pydantic.BaseModel):
    """
    Model class for defining models using Pydantic.

    This class serves as a foundational layer for building Pydantic models with
    custom configurations. It provides a standardized way to manage and validate
    data models, offering additional options for flexibility such as stripping
    whitespace from strings, enabling strict validation, and generating aliases.
    """

    model_config = example.models.configuration.default()

    def __str__(self) -> str:
        return self.jsonify()

    def __bytes__(self) -> bytes:
        return self.jsonify().encode("utf-8")

    def jsonify(self) -> str:
        """
        Converts the object into a JSON-formatted string.

        This method utilizes the `model_dump_json` method to serialize the object into
        a JSON format with a specified indentation for improved readability. It ensures
        the output string is properly formatted for JSON consumption.

        :return: A JSON-formatted string representation of the object.
        :rtype: str
        """

        return self.model_dump_json(indent=4)
