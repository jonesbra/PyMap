"""
Author: Brandon Jones
"""
from pymap.host_parser import HostDefParserHandler


class PyMapException(Exception):
    pass


class Scanner(object):
    def __init__(self, host_defs=list()):
        self.hosts = [host for d in host_defs for host in HostDefParserHandler(d)(d).hosts]
