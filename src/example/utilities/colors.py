import os
import sys

def bold(input: str) -> str:
    """Returns bold ANSI color escape sequence(s).

    Parameters
    ----------
    input: str

    Returns
    -------
    str
    """

    if os.isatty(sys.stdout.fileno()) and (os.getenv("CI", default="") == "" or os.getenv("CI", default="") == "false"):
        return f"\033[1m{input}\033[0m"

    return input

def dim(input: str) -> str:
    """Returns dim ANSI color escape sequence(s).

    Parameters
    ----------
    input: str

    Returns
    -------
    str
    """

    if os.isatty(sys.stdout.fileno()) and (os.getenv("CI", default="") == "" or os.getenv("CI", default="") == "false"):
        return f"\033[2m{input}\033[0m"

    return input

def italic(input: str) -> str:
    """Returns italic ANSI color escape sequence(s).

    Parameters
    ----------
    input: str

    Returns
    -------
    str
    """

    if os.isatty(sys.stdout.fileno()) and (os.getenv("CI", default="") == "" or os.getenv("CI", default="") == "false"):
        return f"\033[3m{input}\033[0m"

    return input

def underline(input: str) -> str:
    """Returns an underline ANSI color escape sequence(s).

    Parameters
    ----------
    input: str

    Returns
    -------
    str
    """

    if os.isatty(sys.stdout.fileno()) and (os.getenv("CI", default="") == "" or os.getenv("CI", default="") == "false"):
        return f"\033[4m{input}\033[0m"

    return input

def strikethrough(input: str) -> str:
    """Returns strikethrough ANSI color escape sequence(s). Warning, this is rarely available across TTYs.

    Parameters
    ----------
    input: str

    Returns
    -------
    str
    """

    if os.isatty(sys.stdout.fileno()) and (os.getenv("CI", default="") == "" or os.getenv("CI", default="") == "false"):
        return f"\033[9m{input}\033[0m"

    return input

def red(input: str) -> str:
    """Returns red ANSI color escape sequence(s).

    Parameters
    ----------
    input: str

    Returns
    -------
    str
    """

    if os.isatty(sys.stdout.fileno()) and (os.getenv("CI", default="") == "" or os.getenv("CI", default="") == "false"):
        return f"\033[91m{input}\033[0m"

    return input

def blue(input: str) -> str:
    """Returns blue ANSI color escape sequence(s).

    Parameters
    ----------
    input: str

    Returns
    -------
    str
    """

    if os.isatty(sys.stdout.fileno()) and (os.getenv("CI", default="") == "" or os.getenv("CI", default="") == "false"):
        return f"\033[34m{input}\033[0m"

    return input

def green(input: str) -> str:
    """Returns green ANSI color escape sequence(s).

    Parameters
    ----------
    input: str

    Returns
    -------
    str
    """

    if os.isatty(sys.stdout.fileno()) and (os.getenv("CI", default="") == "" or os.getenv("CI", default="") == "false"):
        return f"\033[32m{input}\033[0m"

    return input

def yellow(input: str) -> str:
    """Returns yellow ANSI color escape sequence(s).

    Parameters
    ----------
    input: str

    Returns
    -------
    str
    """

    if os.isatty(sys.stdout.fileno()) and (os.getenv("CI", default="") == "" or os.getenv("CI", default="") == "false"):
        return f"\033[33m{input}\033[0m"

    return input

def magenta(input: str) -> str:
    """Returns magenta ANSI color escape sequence(s).

    Parameters
    ----------
    input: str

    Returns
    -------
    str
    """

    if os.isatty(sys.stdout.fileno()) and (os.getenv("CI", default="") == "" or os.getenv("CI", default="") == "false"):
        return f"\033[35m{input}\033[0m"

    return input

def cyan(input: str) -> str:
    """Returns cyan ANSI color escape sequence(s).

    Parameters
    ----------
    input: str

    Returns
    -------
    str
    """

    if os.isatty(sys.stdout.fileno()) and (os.getenv("CI", default="") == "" or os.getenv("CI", default="") == "false"):
        return f"\033[36m{input}\033[0m"

    return input

def white(input: str) -> str:
    """Returns white ANSI color escape sequence(s). White is another reference to what is ANSI default color.

    Parameters
    ----------
    input: str

    Returns
    -------
    str
    """

    if os.isatty(sys.stdout.fileno()) and (os.getenv("CI", default="") == "" or os.getenv("CI", default="") == "false"):
        return f"\033[39m{input}\033[0m"

    return input

def default(input: str) -> str:
    """Returns default ANSI color escape sequence(s). White is another reference to what is ANSI white color, in most cases.

    Parameters
    ----------
    input: str

    Returns
    -------
    str
    """
    
    if os.isatty(sys.stdout.fileno()) and (os.getenv("CI", default="") == "" or os.getenv("CI", default="") == "false"):
        return f"\033[39m{input}\033[0m"

    return input

def black(input: str) -> str:
    """Returns gray-black ANSI color escape sequence(s).

    Parameters
    ----------
    input: str

    Returns
    -------
    str
    """

    if os.isatty(sys.stdout.fileno()) and (os.getenv("CI", default="") == "" or os.getenv("CI", default="") == "false"):
        return f"\033[90m{input}\033[0m"

    return input

def purple(input: str) -> str:
    """Returns purple ANSI color escape sequence(s).

    Parameters
    ----------
    input: str

    Returns
    -------
    str
    """

    if os.isatty(sys.stdout.fileno()) and (os.getenv("CI", default="") == "" or os.getenv("CI", default="") == "false"):
        return f"\033[95m{input}\033[0m"

    return input

def gray(input: str) -> str:
    """Returns gray ANSI color escape sequence(s).

    Parameters
    ----------
    input: str

    Returns
    -------
    str
    """

    if os.isatty(sys.stdout.fileno()) and (os.getenv("CI", default="") == "" or os.getenv("CI", default="") == "false"):
        return f"\033[37m{input}\033[0m"

    return input
