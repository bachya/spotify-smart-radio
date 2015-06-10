import os

from configobj import ConfigObj

CONFIG_DIR = os.path.expanduser('~/.ssr/')
CONFIG_FILE = os.path.expanduser('~/.ssr/config.yaml')
TOKENS_FILE = os.path.expanduser('~/.ssr/tokens.yaml')

class Config(object):
    def __init__(self):
        # Create our directory if it's not already there:
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)

        self.config_data = ConfigObj(CONFIG_FILE)
        self.token_data = ConfigObj(TOKENS_FILE)
        self.verbose = False
