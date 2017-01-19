"""
    I0011 - inline pylint disables
    C0103 - variables should b named in constants convention
    C0111 - no docstring present
"""
# pylint: disable=I0011,C0103,C0111

import socket
from logging.handlers import logging, SysLogHandler
from app.config.config import get_config

class ContextFilter(logging.Filter):
    hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = ContextFilter.hostname
        return True

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logging_filter = ContextFilter()
logger.addFilter(logging_filter)

server = get_config().get("LOGGING", "PAPERTRAIL_SERVER")
port = int(get_config().get("LOGGING", "PAPERTRAIL_PORT"))

syslog = SysLogHandler(address=(server, port))

formatter = logging.Formatter('%(asctime)s POLLEASE: %(message)s', \
    datefmt='%b %d %H:%M:%S')

syslog.setFormatter(formatter)
logger.addHandler(syslog)
