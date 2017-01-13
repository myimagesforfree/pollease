"""
    I0011 - inline pylint disables
    C0111 - Module docstrings
"""
# pylint: disable=I0011,C0111

import unittest2

from app.models.slack_command import SlackCommand

class TestParsing(unittest2.TestCase):

    def test_sample_slack_form_data(self):

        sample = """token=TOKENNNNNN&team_id=T3F55CL14&team_domain=swedishchefs&
channel_id=C3F55CNDC&channel_name=general&user_id=U3DQ62P5X&user_name=adam.rehill&
command=%2Fpollease&text=what+up+bjorkerz&
response_url=https%3A%2F%2Fhooks.slack.com%2Fcommands%2FT3GARBAGEFJuO0taWFevCp"""

        res = SlackCommand(sample)

        self.assertEqual(
            res.command, 'pollease'
        )

if __name__ == '__main__':
    unittest2.main()
