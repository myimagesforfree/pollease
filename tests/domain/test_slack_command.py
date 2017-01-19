"""
    I0011 - inline pylint disables
    C0111 - Module docstrings
"""
# pylint: disable=I0011,C0111

import unittest2
from werkzeug.datastructures import MultiDict

from app.domain.slack_command import SlackCommand

class TestParsing(unittest2.TestCase):

    def test_sample_slack_form_data(self):

        sample = MultiDict([('user_id', u'U3EEPPWEN'), ('response_url', \
            u'https://hooks.slack.com/commands/T3F55CL14/127584780323/6D8ueUmxGdA2mUUk16vykCpf'), \
            ('text', u'create mypoll \u201coption 1\u201d \u201coption 2"'), \
            ('token', u'qy8cU27iplKPHIQQhK1hrFcK'), \
            ('channel_id', u'C3F55CNDC'), ('team_id', u'T3F55CL14'), ('command', u'/pollease'), \
            ('team_domain', u'swedishchefs'), ('user_name', u'adamkrieger'), \
            ('channel_name', u'general')])

        res = SlackCommand(sample)

        self.assertEqual(res.command, '/pollease')
        self.assertEqual(res.team_domain, 'swedishchefs')

if __name__ == '__main__':
    unittest2.main()
