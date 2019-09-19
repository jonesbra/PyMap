"""
Configuration for the PyMap Environment.
"""
import os
import yaml

from netaddr import IPNetwork

DEFAULT_CONFIG_PATH = os.path.join(os.getcwd(), 'pymap.yaml')


def parse_subnet(subnet):
    return [str(ip) for ip in IPNetwork('{0}/{1}'.format(subnet.get('network'), subnet.get('mask')))]


def parse_host(host):
    return host.get('ip')


class Target():
    """Represent a target on the network."""
    def __init__(self, ip):
        pass


class Config():
    """Contain the configuration for the PyMap environment."""
    def __init__(self, config_path):
        if config_path:
            self.config_path = config_path
        else:
            self.config_path = DEFAULT_CONFIG_PATH

        self.config = self.read(self.config_path)
        self._populate_attrs()

    def read(self, config_path):
        """Read the config and populate the object."""
        with open(config_path, 'r') as config_file:
            config = yaml.load(config_file.read(), Loader=yaml.FullLoader)
        return config

    def _populate_attrs(self):
        self.targets = list()
        for target in self.config.get('targets'):
            if target.get('type') == 'subnet':
                self.targets.extend(parse_subnet(target))
            elif target.get('type') == 'host':
                self.targets.append(parse_host(target))
