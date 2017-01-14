"""
    I0011 - inline pylint disables
    C0111 - Module docstrings
"""
# pylint: disable=I0011,C0111

import unittest2

from app.command_router import route_pollease_command
from app.pollease_commands import create_poll

class TestParsing(unittest2.TestCase):

    def test_command_parser_gets_create(self):

        sample = u'create mypoll \u201coption 1\u201d \u201coption 2"'

        res = route_pollease_command(sample)

        self.assertEqual(res, create_poll)

if __name__ == '__main__':
    unittest2.main()
