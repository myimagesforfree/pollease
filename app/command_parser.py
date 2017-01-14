"""
    Handles parsing logistics for pollease.
"""
import shlex

def parse_create_command(command_text):
    """ Parses the vote options out of a create command."""
    params = __deserialize_text(command_text)
    params.pop(0) #Command
    poll_name = params.pop(0) #Pollname
    return poll_name, params

def __deserialize_text(command_text):
    """
        Deserializes the slack command text, which includes the name of the function.
        i.e. >>create myPoll "opt 1" "opt 2"
    """
    #Slack likes to use smart quotes, but shlex doesn't deal with them
    command_text = command_text.replace(u"\u201d", "\"").replace(u"\u201c", "\"")
    command_text = command_text.replace(u"\u2018", "'").replace(u"\u2019", "'")

    params = shlex.split(command_text.encode('utf8'))

    return params
