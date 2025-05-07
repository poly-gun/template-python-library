import os

import logging

import example.utilities.colors

logger = logging.getLogger(__name__)

def test_bold():
    v = example.utilities.colors.bold("bold")

    logger.debug("Output: {}".format(v))

    assert v is not None
    assert v != ""

    if os.getenv("CI") == "true":
        assert v == "bold"

def test_dim():
    v = example.utilities.colors.dim("dim")

    logger.debug("Output: {}".format(v))

    assert v is not None
    assert v != ""

    if os.getenv("CI") == "true":
        assert v == "dim"

def test_italic():
    v = example.utilities.colors.italic("italic")

    logger.debug("Output: {}".format(v))

    assert v is not None
    assert v != ""

    if os.getenv("CI") == "true":
        assert v == "italic"

def test_underline():
    v = example.utilities.colors.underline("underline")

    logger.debug("Output: {}".format(v))

    assert v is not None
    assert v != ""

    if os.getenv("CI") == "true":
        assert v == "underline"

def test_strikethrough():
    v = example.utilities.colors.strikethrough("strikethrough")

    logger.debug("Output: {}".format(v))

    assert v is not None
    assert v != ""

    if os.getenv("CI") == "true":
        assert v == "strikethrough"

def test_red():
    v = example.utilities.colors.red("red")

    logger.debug("Output: {}".format(v))

    assert v is not None
    assert v != ""

    if os.getenv("CI") == "true":
        assert v == "red"

def test_blue():
    v = example.utilities.colors.blue("blue")

    logger.debug("Output: {}".format(v))

    assert v is not None
    assert v != ""

    if os.getenv("CI") == "true":
        assert v == "blue"

def test_green():
    v = example.utilities.colors.green("green")

    logger.debug("Output: {}".format(v))

    assert v is not None
    assert v != ""

    if os.getenv("CI") == "true":
        assert v == "green"

def test_yellow():
    v = example.utilities.colors.yellow("yellow")

    logger.debug("Output: {}".format(v))

    assert v is not None
    assert v != ""

    if os.getenv("CI") == "true":
        assert v == "yellow"

def test_magenta():
    v = example.utilities.colors.magenta("magenta")

    logger.debug("Output: {}".format(v))

    assert v is not None
    assert v != ""

    if os.getenv("CI") == "true":
        assert v == "magenta"

def test_cyan():
    v = example.utilities.colors.cyan("cyan")

    logger.debug("Output: {}".format(v))

    assert v is not None
    assert v != ""

    if os.getenv("CI") == "true":
        assert v == "cyan"

def test_white():
    v = example.utilities.colors.white("white")

    logger.debug("Output: {}".format(v))

    assert v is not None
    assert v != ""

    if os.getenv("CI") == "true":
        assert v == "white"

def test_default():
    v = example.utilities.colors.default("default")

    logger.debug("Output: {}".format(v))

    assert v is not None
    assert v != ""

    if os.getenv("CI") == "true":
        assert v == "default"

def test_black():
    v = example.utilities.colors.black("black")

    logger.debug("Output: {}".format(v))

    assert v is not None
    assert v != ""

    if os.getenv("CI") == "true":
        assert v == "black"

def test_purple():
    v = example.utilities.colors.purple("purple")

    logger.debug("Output: {}".format(v))

    assert v is not None
    assert v != ""

    if os.getenv("CI") == "true":
        assert v == "purple"

def test_gray():
    v = example.utilities.colors.gray("gray")

    logger.debug("Output: {}".format(v))

    assert v is not None
    assert v != ""

    if os.getenv("CI") == "true":
        assert v == "gray"
