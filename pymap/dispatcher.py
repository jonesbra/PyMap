"""
Author: Brandon Jones
"""
import subprocess
import os
import platform
from pymap.host_parser import HostDefParserHandler
from pymap.ping_scanner import PingScannerHandler
from pymap.tcp_scanner import TcpScannerHandler
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser


class PyMapException(Exception):
    pass


class Scanner(object):
    def __init__(self, host_defs=list()):
        self.hosts = [host for d in host_defs for host in HostDefParserHandler(d)(d).hosts]

    def get_dict(self):
        return {'hosts': [{'ip': str(host.ip)} for host in self.hosts]}


class NMapScanner(Scanner):
    def __init__(self, host_defs=list()):
        super(NMapScanner, self).__init__(host_defs)

    def scan(self):
        nm = NmapProcess(targets=[str(host.ip) for host in self.hosts])
        nm.run()
        nmap_report = NmapParser.parse(nm.stdout)
        for host in nmap_report.hosts:
            self.add_host_data(host)

    def get_host(self, host_s):
        for host in self.hosts:
            if host_s == str(host.ip):
                return host
        raise PyMapException('Could not find host in scanner: {}'.format(host_s))

    def add_host_data(self, host_n):
        host = self.get_host(host_n.address)
        setattr(host, 'distance', host_n.distance)

    def get_dict(self):
        super(NMapScanner, self).get_dict()


class PyMapScanner(Scanner):
    def __init__(self, host_defs=list()):
        super(PyMapScanner, self).__init__(host_defs)
        self.pingScanner = PingScannerHandler(self.hosts)
        self.tcpScanner = TcpScannerHandler(self.hosts)

    def scan(self):
        self.pingScanner.scan()
        self.tcpScanner.scan()

    def get_dict(self):
        super(PyMapScanner, self).get_dict()


ScannerMap = {
    'nmap': NMapScanner,
    'pymap': PyMapScanner
}


def ScannerHandler(host_defs, method='pymap'):
    return ScannerMap.get(method)(host_defs=host_defs)
