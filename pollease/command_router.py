"""Returns the expected function based on the command text."""

from custom_exceptions import CommandParsingException
from constants import VALID_COMMANDS, COMMAND_CLOSE, COMMAND_CREATE, ERR_PARSING_COMMAND

from command_parser import __deserialize_text
from pollease_commands import create_poll, close_poll

def route_pollease_command(command_text):
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
