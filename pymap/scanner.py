"""
Scanner for the PyMap Environment.
"""
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser


class Scanner():
    """Scan and populate device objects."""
    def __init__(self):
        pass

    def scan(self, targets):
        """Do a scan on the network."""
        nm = NmapProcess(targets, options='-A')
        rc = nm.run()
        nmap_report = NmapParser.parse(nm.stdout)

        for host in nmap_report.hosts:
            if host.is_up():
                print ('{0}    {1}    {0}'.format('=' * 30, host.address))
                for os in host.os_class_probabilities():
                    for key, value in os.__dict__.items():
                        print ('{0}\t:{1}'.format(key, value))

    def populate_netbox(self):
        """Send the data contained in the scanner to netbox."""
        pass
