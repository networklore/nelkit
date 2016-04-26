"""nk-snmp-deviceinfo - command line tool."""
from nelkit.args.snmp import SnmpArgs
from nelkit.snmp.handler import NelkitSnmp
from nelsnmp.hostinfo.device import HostInfo

description = 'Collects Device info using SNMP'


def main():
    """run nk-snmp-deviceinfo."""
    argparser = SnmpArgs(description)
    args = argparser.parser.parse_args()
    snmp = NelkitSnmp(args)
    hostinfo = HostInfo(snmp)
    hostinfo.get_all()
    print('OS: %s' % hostinfo.os)
    print('Version: %s' % hostinfo.version)
    print('Vendor: %s' % hostinfo.vendor)
    print('Description: %s' % hostinfo.description)


if __name__ == "__main__":
    main()
