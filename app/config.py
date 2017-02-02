"""
    Manages global configuration for pollease.
"""

from ConfigParser import SafeConfigParser
import os

# LOCAL_CONFIG_FILE = '/usr/src/app/config_local.ini'
PROD_CONFIG_FILE = '/usr/src/app/config.ini'

def create_config():
    """ Creates a config parser object from local config if present, or production config if not"""
    parser = SafeConfigParser(os.environ)
    parser.read(PROD_CONFIG_FILE)
    return parser

CONFIG = create_config()

def get_config():
    """ Returns configuration """
    return CONFIG
