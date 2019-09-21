"""
Dispatcher for the PyMap Library.
"""
from pymap import Config, Scanner, Scraper
from pymap.models import NetboxTransport, Device, DeviceType, DeviceRole, Site, Manufacturer
from pymap.utils import get_netmiko_device_type


class PyMap():
    """Contain the configuration for the PyMap environment."""
    def __init__(self, config_path=None):
        self.config = Config(config_path)
        self.scanner = Scanner(self.config.targets)
        self.nmap_hosts = list()
        self.netbox_hosts = list()

    def get_config(self):
        """Return the current state of the PyMap configuration."""
        return self.config.config

    def scan(self):
        """Initiate the scanner."""
        self.nmap_hosts = self.scanner.scan()
        self.populate_scan()
        print('Scan Complete.')

    def populate_scan(self):
        """Populate the scan results."""
        transport = NetboxTransport(self.config.netbox_url, self.config.netbox_token)
        site = Site(self.config.site.get('name'), self.config.site.get('description'))
        transport.post(site)
        for host in self.nmap_hosts:
            if host.is_up():
                print('=' * 30 + host.address + '=' * 30)
                manufacturer = Manufacturer(host.pymap_os.vendor)
                transport.post(manufacturer)

                device_type = DeviceType(host.pymap_os.osfamily, manufacturer,
                                         host.pymap_os.osfamily)
                transport.post(device_type)

                device_role = DeviceRole(host.pymap_os.type)
                transport.post(device_role)

                scraper = Scraper(host.address, self.config.ssh_username, self.config.ssh_password,
                                  get_netmiko_device_type(host.pymap_os.vendor,
                                                          host.pymap_os.osfamily))

                device = Device(scraper.get_hostname(), device_type, device_role,
                                site, host.address)
                transport.post(device)

                self.netbox_hosts.append(device)
