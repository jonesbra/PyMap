class TcpScanner(object):
    def __init__(self, hosts=list()):
        self.hosts = hosts

    def scan(self):
        pass

def TcpScannerHandler(hosts):
    return TcpScanner(hosts=hosts)
