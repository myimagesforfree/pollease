"""Poll Class"""
# pylint: disable=I0011,    R0903

class Poll(object):
    """The parent record reference to a poll."""
    poll_id = ""
    team_id = ""
    channel_id = ""
    name = ""
    date_open = 0
    date_close = 0
    owner_user_id = ""
    poll_choices = []

    def __init__(self, poll_id, team_id, team_domain, channel_id, channel_name, \
            name, date_open, date_close, owner_user_id, poll_choices):
        self.poll_id = poll_id
        self.team_id = team_id
        self.team_domain = team_domain
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.name = name
        self.date_open = date_open
        self.date_close = date_close
        self.owner_user_id = owner_user_id
        self.poll_choices = poll_choices

class PollChoice(object):
    """The parent record reference to a poll choice."""
    choice_id = ""
    name = ""

    def __init__(self, choice_id, name):
        self.choice_id = choice_id
        self.name = name


