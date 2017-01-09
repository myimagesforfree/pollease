"""Poll Class"""
# pylint: disable=I0011,    R0903

class Poll(object):
    """The parent record reference to a poll."""
    poll_id = ""
    team_id = ""
    channel_id = ""
    name = ""
    is_open = False
    owner_user_id = ""
    poll_choices = []

    def __init__(self, poll_id, team_id, channel_id, name, is_open, owner_user_id, poll_choices):
        self.poll_id = poll_id
        self.team_id = team_id
        self.channel_id = channel_id
        self.name = name
        self.is_open = is_open
        self.owner_user_id = owner_user_id
        self.poll_choices = poll_choices

class PollChoice(object):
    """The parent record reference to a poll choice."""
    choice_id = ""
    name = ""

    def __init__(self, choice_id, name):
        self.choice_id = choice_id
        self.name = name

