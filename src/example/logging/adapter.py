import logging

class Adapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        name = kwargs.get("name", None)
        if name is not None:
            return "[{}] {}".format(name, msg), kwargs

        return msg, kwargs
