"""
    Pollease Action Central
"""
import command_parser
from models.poll import Poll

from constants import ERR_POLL_ALREADY_IN_PROGRESS, ERR_NO_POLL_IN_PROGRESS

from papertrail import logger

def create_poll(command_params, repo, db_conn, command_details):
    """Creates a new poll, assuming that one isn't already in progress."""

    poll_name, voting_choices = command_parser.parse_create_command(command_params)

    current_poll = repo.select_first_poll(db_conn)

    if current_poll is None:
        logger.info("Creating poll for {0}.{1}.{2}: {3}".format(command_details.team_domain, \
            command_details.channel_name, command_details.user_name, poll_name))
        new_poll = Poll("newpoll", command_details.team_domain, "chan", "poll_name", True, "owner")
        repo.create_poll(db_conn, new_poll)
        return generate_new_poll_response(poll_name, voting_choices)
    else:
        logger.info("Failed to create poll: " + poll_name + \
        ". Another poll is already in progress.")
        return generate_return_message(ERR_POLL_ALREADY_IN_PROGRESS)

def close_poll(command_params, repo, db_conn, command_details):
    """Closes the current poll."""
    current_poll = repo.select_first_poll(db_conn)

    if current_poll is None:
        return generate_return_message(ERR_NO_POLL_IN_PROGRESS)
    else:
        poll_name = current_poll.get("text")
        logger.info("Closing poll: " + poll_name)

        return generate_return_message("Poll: '" + poll_name + "' has now been closed.")

def generate_new_poll_response(poll_name, voting_choices):
    """Generates the message object for a pretty Slack message."""
    attachments = []

    for choice in voting_choices:
        attachments.append(
            {
                "text": choice,
                "response_type": "in_channel",
                "fallback": "You are unable to vote",
                "callback_id": "vote_callback",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "vote",
                        "text": "Vote",
                        "type": "button",
                        "value": "false"
                    }
                ]
            }
        )

    current_poll = {
        "text": poll_name,
        "attachments": attachments,
        "response_url": "https://0665a1ee.ngrok.io/test"
    }

    return current_poll

def generate_return_message(message):
    """Creates object for helpful Slack message."""
    return {
        "text": message
        }
