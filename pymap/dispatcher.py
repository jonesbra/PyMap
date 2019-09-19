"""
Dispatcher for the PyMap Library.
"""
from pymap import Config, Scanner


class PyMap():
    """Contain the configuration for the PyMap environment."""
    def __init__(self, config_path=None):
        self.config = Config(config_path)
        self.scanner = Scanner()

    def get_config(self):
        """Return the current state of the PyMap configuration."""
        return self.config.config

    def scan(self):
        """Initiate the scanner."""
        self.scanner.scan(self.config.targets)
