from argparse import ArgumentParser, RawTextHelpFormatter


class NkArgumentParser(ArgumentParser):
    pass


class HelpText(object):

    def __init__(self, description, epilog):
        desc_prefix = '#' * 75
        desc_prefix += '\n'
        desc_suffix = '#' * 75
        self.description = desc_prefix + description + '\n' + desc_suffix
        epilog_suffix = '#' * 75
        epilog_suffix += '\n'
        epilog_suffix += 'This tool is part of Nelkit:\n'
        epilog_suffix += 'http://networklore.com/nelkit\n'
        epilog_suffix += '\n'
        self.epilog = epilog_suffix + epilog


class BaseArgs(object):

    def __init__(self, description, epilog=''):
        helptext = HelpText(description, epilog)
        self.parser = NkArgumentParser(
            description=helptext.description,
            epilog=helptext.epilog,
            formatter_class=RawTextHelpFormatter)

        self.parser.add_argument(
            '-V',
            help='Show version',
            action='store_true')
        self.parser.add_argument(
            '-O',
            help='Output format',
            choices=['standard', 'with_status'],
            default='standard'
        )

        self._add_local_args()

    def _add_local_args(self):
        pass
