"""Functions for formatting Slack-specific data."""

def generate_return_message(message, options=None):
    """Generates an object that will render text back to the Slack channel.
     Optional Options dictionary will include any options for the message
     such as color, replace original, etc."""

    msg = {
        "text": message
    }

    if options is not None:
        msg.update(options)

    return msg
