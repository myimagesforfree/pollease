"""
    Manages global configuration for pollease.
"""

from ConfigParser import ConfigParser

LOCAL_CONFIG_FILE = 'config/config_local.ini'
PROD_CONFIG_FILE = 'config/config.ini'

import os
def create_config():
    """ Creates a config parser object from local config if present, or production config if not"""

    parser = ConfigParser()
    parser.read(LOCAL_CONFIG_FILE or PROD_CONFIG_FILE)
    return parser

CONFIG = create_config()

def get_config():
    """ Returns configuration """
    return CONFIG
