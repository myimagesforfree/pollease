import shlex

from constants import COMMAND_CLOSE, COMMAND_CREATE, ERR_PARSING_COMMAND, VALID_COMMANDS

def parse_pollease_command(command_text):
    params = shlex.split(command_text)
    command = params.pop(0).lower()

    if command not in VALID_COMMANDS:
        raise CommandParsingException(ERR_PARSING_COMMAND)
    else:
        return command, params

def parse_create_command(command_params):
    poll_name = command_params.pop(0)
    return poll_name, command_params

class CommandParsingException(Exception):
    pass
