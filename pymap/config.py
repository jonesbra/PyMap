"""
Configuration for the PyMap Environment.
"""
import os
import yaml

from netaddr import IPNetwork

DEFAULT_CONFIG_PATH = os.path.join(os.getcwd(), 'pymap.yaml')
DEFAULT_OUTPUT_PATH = os.path.join(os.getcwd(), 'pymap-out')


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
    def __init__(self, config_path=None, output_path=None):
        if config_path:
            self.config_path = config_path
        else:
            self.config_path = DEFAULT_CONFIG_PATH

        if output_path:
            self.output_path = output_path
        else:
            self.output_path = DEFAULT_OUTPUT_PATH

        self.config = self.read(self.config_path)
        self.targets = list()

        self._populate_attrs()

    def read(self, config_path):
        """Read the config and populate the object."""
        with open(config_path, 'r') as config_file:
            config = yaml.load(config_file.read(), Loader=yaml.FullLoader)
        return config

    def _populate_attrs(self):
        self._populate_targets()
        self.site = self.config.get('site')
        self.netbox_url = self.config.get('netbox_url')
        self.netbox_username = self.config.get('netbox_username')
        self.netbox_password = self.config.get('netbox_password')
        self.netbox_token = self.config.get('netbox_token')
        self.ssh_username = self.config.get('ssh_username')
        self.ssh_password = self.config.get('ssh_password')

    def _populate_targets(self):
        for target in self.config.get('targets'):
            if target.get('type') == 'subnet':
                self.targets.extend(parse_subnet(target))
            elif target.get('type') == 'host':
                self.targets.append(parse_host(target))
