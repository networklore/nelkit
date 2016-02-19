
class NelkitGlobals(object):

    FRIENDLY_EXCEPTION = None

    def __init__(self, **kwargs):

        for key in kwargs:
            if key == 'FRIENDLY_EXCEPTION':
                NelkitGlobals.FRIENDLY_EXCEPTION = kwargs[key]
