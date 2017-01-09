"""
    Pollease Action Central
"""
import command_parser
from models.poll import Poll, PollChoice

from constants import ERR_POLL_ALREADY_IN_PROGRESS, ERR_NO_POLL_IN_PROGRESS

from papertrail import logger
import uuid

def create_poll(command_params, repo, db_conn, command_details):
    """Creates a new poll, assuming that one isn't already in progress."""

    poll_name, raw_poll_choices = command_parser.parse_create_command(command_params)
    current_poll = repo.select_first_poll(db_conn)

    if current_poll is None:
        logger.info("Creating poll for %s.%s.%s: %s", command_details.team_domain, \
            command_details.channel_name, command_details.user_name, poll_name)

        poll_choices = []
        for choice in raw_poll_choices:
            poll_choices.append(PollChoice(str(uuid.uuid4()), choice))

        new_poll = Poll(str(uuid.uuid4()), command_details.team_domain, \
        command_details.channel_id, poll_name, True, command_details.user_id, poll_choices)

        persisted_poll = repo.persist_poll(db_conn, new_poll)

        return generate_new_poll_response(persisted_poll)
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

def generate_new_poll_response(poll):
    """Generates the message object for a pretty Slack message."""
    attachments = []

    for choice in poll.poll_choices:
        attachments.append(
            {
                "text": choice.name,
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
        "text": poll.name,
        "attachments": attachments,
        "response_url": "--update-to-interactive-message-url--"
    }

    return current_poll

def generate_return_message(message):
    """Creates object for helpful Slack message."""
    return {
        "text": message
        }
