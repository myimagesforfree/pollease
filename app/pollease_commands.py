"""
    Pollease Action Central
"""
import uuid
import arrow

from constants import ERR_NO_POLL_IN_PROGRESS, ERR_POLL_ALREADY_IN_PROGRESS
from papertrail import logger
from custom_exceptions import PolleaseException
from slack_formatting import generate_return_message

from command_parser import parse_create_command
from poll import Poll, PollChoice

# pylint: disable=I0011,W1202

def create_poll(repo, db_conn, command_details):
    """Creates a new poll, assuming that one isn't already in progress."""

    poll_name, raw_poll_choices = parse_create_command(command_details.text)

    now = arrow.utcnow().timestamp

    current_poll = repo.fetch_poll_by_channel(db_conn, \
        command_details.team_id, command_details.channel_id, now)

    try:
        if current_poll is None:
            logger.info("Creating poll for %s.%s.%s: %s", command_details.team_domain, \
                command_details.channel_name, command_details.user_name, poll_name)

            poll_choices = []
            for choice in raw_poll_choices:
                poll_choices.append(PollChoice(str(uuid.uuid4()), choice))

            now = arrow.utcnow().timestamp
            two_hours = 60 * 120

            new_poll = Poll(str(uuid.uuid4()), command_details.team_id, \
                command_details.team_domain, command_details.channel_id, \
                command_details.channel_name, poll_name, \
                now, \
                now + two_hours, \
                command_details.user_id, poll_choices)

            repo.persist_poll(db_conn, new_poll)

            return generate_new_poll_response(new_poll)
        else:
            logger.info("Failed to create poll: " + poll_name + \
            ". Another poll is already in progress.")
            return generate_return_message(ERR_POLL_ALREADY_IN_PROGRESS)
    except PolleaseException as pex:
        return generate_return_message(str(pex))


def close_poll(repo, db_conn, command_details):
    """Closes the current poll."""
    try:
        now = arrow.utcnow().timestamp

        current_poll = repo.fetch_poll_by_channel(db_conn, \
            command_details.team_id, command_details.channel_id, now)

        if current_poll is None:
            return generate_return_message(ERR_NO_POLL_IN_PROGRESS)
        elif current_poll.owner_user_id != command_details.user_id:
            return generate_return_message("You do not own this poll.")
        else:
            now_after_query = arrow.utcnow().timestamp

            poll_name = current_poll.name
            logger.info("Closing poll: {0}, old close: {1} new close: {2}".format( \
                current_poll.poll_id, current_poll.date_close, now_after_query))

            if now_after_query < current_poll.date_close:
                current_poll.date_close = now_after_query
                repo.update_poll(db_conn, current_poll)

            return generate_return_message("Poll: '" + poll_name + "' has now been closed.")
    except PolleaseException as pex:
        return generate_return_message(str(pex))

def cast_vote(repo, db_conn, poll_id, poll_choice_id, voter_user_id):
    """Casts vote for poll"""
    try:
        repo.persist_vote(db_conn, poll_id, poll_choice_id, voter_user_id)

        msg_options = {
            "replace_original": False
        }

        return generate_return_message("Your vote has been received", msg_options)
    except PolleaseException as pex:
        return generate_return_message(str(pex))

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
                        "value": poll.poll_id + " " + choice.choice_id
                    }
                ]
            }
        )

    current_poll = {
        "text": poll.name,
        "attachments": attachments
    }

    return current_poll
