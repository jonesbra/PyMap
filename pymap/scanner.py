"""
Scanner for the PyMap Environment.
"""
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser as LibNmapParser


class NmapParser(LibNmapParser):
    def __init__(self, stdout):
        self.nmap_report = LibNmapParser.parse(stdout)
        self.hosts = self.nmap_report.hosts
        for host in self.hosts:
            if host.is_up():
                setattr(host, 'pymap_os', self._get_pymap_os(host.os_match_probabilities()))
                setattr(host, 'hostname', self._parse_hostnames(host.hostnames))

    def _get_pymap_os(self, os_matches):
        if os_matches == []:
            response = None
        elif os_matches[0].osclasses == []:
            response = None
        else:
            response = os_matches[0].osclasses[0]
        return response

    def _parse_hostnames(self, hostnames):
        if hostnames == []:
            response = 'None'
        else:
            response = hostnames[0]
        return response


class Scanner():
    """Scan and populate device objects."""
    def __init__(self, targets):
        self.targets = targets

    def scan(self):
        """Do a scan on the network."""
        nmap_process = NmapProcess(self.targets, options='-A')
        nmap_process.run()
        nmap_report = NmapParser(nmap_process.stdout)
        return nmap_report.hosts
