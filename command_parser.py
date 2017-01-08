"""
    Handles parsing logistics for pollease.
"""
import shlex

from constants import COMMAND_CLOSE, COMMAND_CREATE, ERR_PARSING_COMMAND, VALID_COMMANDS
from pollease import create_poll, close_poll

def parse_pollease_command(command_text):
    """
        Parses the command text to an object.
        If the command is valid, returns the command to be used.
    """
    command_text = command_text.replace(u"\u201d", "\"").replace(u"\u201c", "\"")
    command_text = command_text.replace(u"\u2018", "'").replace(u"\u2019", "'")
    params = shlex.split(command_text.encode('utf8'))
    command = params.pop(0).lower()

    if command not in VALID_COMMANDS:
        raise CommandParsingException(ERR_PARSING_COMMAND)
    else:
        if command == COMMAND_CREATE:
            return create_poll, params
        elif command == COMMAND_CLOSE:
            return close_poll, params

def parse_create_command(command_params):
    """ Parses the vote options out of a create command."""
    poll_name = command_params.pop(0)
    return poll_name, command_params

class CommandParsingException(Exception):
    """Custom exception for command parse failures."""
    pass
