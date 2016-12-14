import shlex

def parse_create_command(command_text):
    params = shlex.split(command_text)
    poll_name = params.pop(0)
    return poll_name, params
