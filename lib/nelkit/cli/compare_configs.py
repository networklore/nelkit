"""nk-compare-configs."""
from nelkit.args.base import BaseArgs
from nelkit.globals import NelkitGlobals
from nelkit.modules.compare_configs.settings import CompareConfigs

description = 'Compare configurations against a baseline'


def main():
    """Launch nk-compare-configs."""
    NelkitGlobals(FRIENDLY_EXCEPTION=True)

    argparser = BaseArgs(description)
    argparser.parser.add_argument(
        '-c',
        help='Configuration file',
        type=str,
        required=True)
    args = argparser.parser.parse_args()
    cc = CompareConfigs(settings_file=args.c)
    cc.output_diff()

if __name__ == "__main__":
    main()
