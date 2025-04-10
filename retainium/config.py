# Compute project root relative to this script
# (protect against symlinks using realpath())
import os
root = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))

# Import required modules
import configparser
from retainium.diagnostics import Diagnostics

# Load configuration
def load_config(config_path: str = os.path.join(root, "etc", "config.ini")):
    """Load configuration settings from config.ini."""
    config = configparser.ConfigParser()
    if os.path.exists(config_path):
        Diagnostics.note(f"loading configuration from \"{config_path}\"")
        config.read(config_path)
    else:
        Diagnostics.warning(f"missing configuration file \"{config_path}\"")
    return config

