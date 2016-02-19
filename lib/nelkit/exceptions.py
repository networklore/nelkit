import sys
from nelkit.globals import NelkitGlobals


class NelkitException(Exception):

    def __init__(self, message):
        if NelkitGlobals.FRIENDLY_EXCEPTION:
            print (message)
            sys.exit()
        else:
            super(NelkitException, self).__init__(message)


class FileNotFound(NelkitException):
    pass


class ParsingError(NelkitException):
    pass
