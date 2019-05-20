import platform
import subprocess


class PingScanner(object):
    def __init__(self, hosts=list()):
        self.hosts = hosts


class PingScannerDarwin(PingScanner):
    def __init__(self, hosts=list()):
        super(PingScannerDarwin, self).__init__(hosts)

    def scan_host(self, host):
        cmd = ' '.join(['ping', '-c', '3', '-W', '1', str(host.ip)])
        try:
            out = subprocess.check_output(cmd, shell=True)
            setattr(host, 'pingable', True)
            setattr(host, 'state', True)
        except subprocess.CalledProcessError:
            setattr(host, 'pingable', False)

    def scan(self):
        for host in self.hosts:
            self.scan_host(host)


class PingScannerWindows(PingScanner):
    def __init__(self, hosts=list()):
        super(PingScannerWindows, self).__init__(hosts)

    def scan(self, host):
        pass


PingScannerMap = {
    'darwin': PingScannerDarwin,
    'windows': PingScannerWindows
}


def PingScannerHandler(hosts):
    return PingScannerMap.get(platform.system().lower())(hosts=hosts)
