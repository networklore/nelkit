"""This module contains exceptions available to nelkit."""

import sys
from nelkit.globals import NelkitGlobals


class NelkitException(Exception):
    """Base nelkit exception class.

    By default an exception will be raised, this can be overwritten using
    nelkit.globals.NelkitGlobals so that the error messages are printed out
    to the screen instead. This is done from the cli tools.
    """

    def __init__(self, message):
        """Base nelkit exception class."""
        if NelkitGlobals.FRIENDLY_EXCEPTION:
            print(message)
            sys.exit()
        else:
            super(NelkitException, self).__init__(message)


class ArgumentError(NelkitException):
    """Raised when passing invalid arguments using cli tools."""

    pass


class FileNotFound(NelkitException):
    """Raised when trying to open a file which doesn't exist."""

    pass


class ParsingError(NelkitException):
    """Raised when trying to parse a file with invalid formatting."""

    pass
