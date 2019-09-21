"""
Scraper for the PyMap Environment.
"""
from netmiko import ConnectHandler


class Scraper():
    """Scrape the device for information."""
    def __init__(self, host, username, password, device_type):
        self.host = host
        self.username = username
        self.password = password
        self.device_type = device_type

    def get_hostname(self):
        connection = ConnectHandler(**{
            'device_type': self.device_type,
            'host': self.host,
            'username': self.username,
            'password': self.password
        })
        return connection.base_prompt
