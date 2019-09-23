"""
Scraper for the PyMap Environment.
"""
from netmiko import ConnectHandler
from ntc_templates.parse import parse_output

CMD_MAPPER = {
    'cisco_ios': {
        'interfaces': 'show interfaces'
    }
}
class Scraper():
    """Scrape the device for information."""
    def __init__(self, host, username, password, device_type):
        self.host = host
        self.username = username
        self.password = password
        self.device_type = device_type
        self.connection = ConnectHandler(**{
            'device_type': self.device_type,
            'host': self.host,
            'username': self.username,
            'password': self.password
        })

    def get_hostname(self):
        return self.connection.base_prompt

    def get_interfaces(self):
        cmd = CMD_MAPPER[self.device_type]['interfaces']
        return parse_output(platform=self.device_type, command=cmd, data=self.connection.send_command(cmd))
