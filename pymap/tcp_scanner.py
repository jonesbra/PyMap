class TcpScanner(object):
    def __init__(self, hosts=list()):
        self.hosts = hosts

    def scan_host(self, host):
        host.ports = list()

    def scan(self):
        for host in self.hosts:
            self.scan_host(host)


def TcpScannerHandler(hosts):
    return TcpScanner(hosts=hosts)
