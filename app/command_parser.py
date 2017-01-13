"""
    Handles parsing logistics for pollease.
"""
import shlex

from constants import COMMAND_CLOSE, COMMAND_CREATE, ERR_PARSING_COMMAND, VALID_COMMANDS
from custom_exceptions import CommandParsingException
from pollease import create_poll, close_poll

def parse_pollease_command(command_text):
    """
        Parses the command text to an object.
        If the command is valid, returns the command to be used.
    """
    params = __deserialize_text(command_text)
    command = params.pop(0).lower()

    if command not in VALID_COMMANDS:
        raise CommandParsingException(ERR_PARSING_COMMAND)
    else:
        if command == COMMAND_CREATE:
            return create_poll
        elif command == COMMAND_CLOSE:
            return close_poll

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
