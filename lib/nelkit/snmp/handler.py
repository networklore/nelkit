"""Create an SNMP handler using nelsnmp."""
from nelkit.exceptions import ArgumentError
from nelsnmp.snmp import cmdgen, SnmpHandler


class NelkitSnmp(SnmpHandler):
    """Nelkit version of SnmpHandler from nelsnmp."""

    def __init__(self, args):
        """Return a nelsnmp SnmpHandler."""
        self._verify_snmp_arguments(args)
        self._set_snmp_parameters(args)

    def _set_snmp_parameters(self, args):
        self.version = args.P
        if args.P == "2c":
            self.snmp_auth = cmdgen.CommunityData(args.C)

        elif args.P == "3":
            self.username = args.U
            if args.a == "SHA":
                self.integrity = cmdgen.usmHMACSHAAuthProtocol
            elif args.a == "MD5":
                self.integrity = cmdgen.usmHMACMD5AuthProtocol

            if args.x == "AES":
                self.privacy = cmdgen.usmAesCfb128Protocol
            elif args.x == "DES":
                self.privacy = cmdgen.usmDESPrivProtocol

            self.authkey = args.A

            if args.L == "authPriv":
                self.privkey = args.X

        self.host = args.H
        self.port = int(args.p)

    def _verify_snmp_arguments(self, args):
        if args.P == "2c" and args.C is None:
            ArgumentError('Specify community when using SNMP 2c')
        if args.P == "3" and args.U is None:
            ArgumentError('Specify username when using SNMP 3')
        if args.P == "3" and args.L is None:
            ArgumentError('Specify security level when using SNMP 3')
        if args.L == "authNoPriv" and args.a is None:
            ArgumentError('Specify authentication protocol when using authNoPriv')
        if args.L == "authNoPriv" and args.A is None:
            ArgumentError('Specify authentication password when using authNoPriv')
        if args.L == "authPriv" and args.a is None:
            ArgumentError('Specify authentication protocol when using authPriv')
        if args.L == "authPriv" and args.A is None:
            ArgumentError('Specify authentication password when using authPriv')
        if args.L == "authPriv" and args.x is None:
            ArgumentError('Specify privacy protocol when using authPriv')
        if args.L == "authPriv" and args.X is None:
            ArgumentError('Specify privacy password when using authPriv')
