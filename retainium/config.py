import configparser
import os

def load_config(config_path="etc/config.ini"):
    """Load configuration settings from config.ini."""
    config = configparser.ConfigParser()
    if os.path.exists(config_path):
        config.read(config_path)
    return config
