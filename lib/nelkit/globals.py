"""This module contains the NelkitGlobals class used to override standard settings."""


class NelkitGlobals(object):
    """Nelkit global class to override standard settings."""

    FRIENDLY_EXCEPTION = None

    def __init__(self, **kwargs):
        """Override standard settings.

        :param FRIENDLY_EXCEPTION: (optional) Boolean value to control if errors are to be printed or raised.
        """
        for key in kwargs:
            if key == 'FRIENDLY_EXCEPTION':
                NelkitGlobals.FRIENDLY_EXCEPTION = kwargs[key]
