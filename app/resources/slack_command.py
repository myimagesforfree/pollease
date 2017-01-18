"""Slack Command Class"""
# pylint: disable=I0011,    R0903

class SlackCommand(object):
    """The parent record reference to a poll."""
    command = ""
    text = ""
    team_id = ""
    team_domain = ""
    channel_id = ""
    channel_name = ""
    user_id = ""
    user_name = ""
    response_url = ""

    def __init__(self, request_data):

        self.command = request_data['command']
        self.text = request_data['text']
        self.team_id = request_data['team_id']
        self.team_domain = request_data['team_domain']
        self.channel_id = request_data['channel_id']
        self.channel_name = request_data['channel_name']
        self.user_id = request_data['user_id']
        self.user_name = request_data['user_name']
        self.response_url = request_data['response_url']
