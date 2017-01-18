"""
    I0011 - inline pylint disables
    C0103 - variables should b named in constants convention
    C0111 - no docstring present
"""
# pylint: disable=I0011,C0103,C0111

import socket
from logging.handlers import logging, SysLogHandler

from config import PAPERTRAIL_PORT, PAPERTRAIL_SERVER

class ContextFilter(logging.Filter):
    hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = ContextFilter.hostname
        return True

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logging_filter = ContextFilter()
logger.addFilter(logging_filter)

syslog = SysLogHandler(address=(PAPERTRAIL_SERVER, PAPERTRAIL_PORT))
formatter = logging.Formatter('%(asctime)s POLLEASE: %(message)s', \
    datefmt='%b %d %H:%M:%S')

syslog.setFormatter(formatter)
logger.addHandler(syslog)
