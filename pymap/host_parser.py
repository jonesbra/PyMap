"""
Author: Brandon Jones
"""
import netaddr


class HostDefParserException(Exception):
    pass


class HostDefParser(object):
    def __init__(self, definition):
        self.definition = definition

        if not isinstance(self.definition, dict):
            raise PyMapException('host definitions must of type {}'.format(str(type(dict))))

        for property in self.properties:
            if isinstance(definition.get(property), type(None)):
                raise HostDefParserException('{0} must have property: {1}'.format(type(self), property))


class HostDefParserSubnet(HostDefParser):
    def __init__(self, definition):
        self.properties = ['ip', 'mask']
        super(HostDefParserSubnet, self).__init__(definition)

        self.hosts = [Host(ip) for ip in list(netaddr.IPNetwork('{0}/{1}'.format(self.definition.get('ip'), self.definition.get('mask'))))]


class HostDefParserRange(HostDefParser):
    def __init__(self, definition):
        self.properties = ['start', 'end']
        super(HostDefParserRange, self).__init__(definition)

        self.hosts = [Host(ip) for ip in list(netaddr.iter_iprange(self.definition.get('start'), self.definition.get('end')))]


class HostDefParserList(HostDefParser):
    def __init__(self, definition):
        self.properties = ['list']
        super(HostDefParserList, self).__init__(definition)

        self.hosts = [Host(ip) for ip in self.definition.get('list')]


class Host(object):
    def __init__(self, ip):
        self.ip = netaddr.IPAddress(ip)



HostDefParserMap = {
    'subnet': HostDefParserSubnet,
    'range': HostDefParserRange,
    'list': HostDefParserList
}


def HostDefParserHandler(definition):
    return HostDefParserMap.get(definition.get('type'))
