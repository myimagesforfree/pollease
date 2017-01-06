"""
    I0011 - inline pylint disables
    C0103 - variables should b named in constants convention
    C0111 - no docstring present
"""
# pylint: disable=I0011,C0103,C0111

import traceback
from command_parser import CommandParsingException
import command_parser
import requests

from constants import ERR_POLL_ALREADY_IN_PROGRESS, ERR_NO_POLL_IN_PROGRESS, \
ERR_UNKNOWN, COMMAND_CREATE, COMMAND_CLOSE

from config import SLACK_AUTH_URL, SLACK_CLIENT_ID, SLACK_CLIENT_SECRET

from flask import request, url_for
from flask_api import FlaskAPI, exceptions, status
from papertrail import logger
from polls_repository import PollsRepository, Poll

"""
    pollease - A Slack poll integration.
    Written by Adam Rehill and Adam Krieger, 2016
"""
current_poll = None
app = FlaskAPI(__name__)

repo = PollsRepository()
poll = Poll("123", "456", "789", "test poll name", True, "987")
repo.create_poll(poll)
repo.fetch_poll("123")

@app.route('/authorize', methods=['GET'])
def authorize():
    code = request.args.get('code')

    query_string = "?client_id=%s&client_secret=%s&code=%s" % \
     (SLACK_CLIENT_ID, SLACK_CLIENT_SECRET, code)

    auth_request_url = SLACK_AUTH_URL + query_string

    response_json = requests.post(auth_request_url).json()

    if response_json.get("ok"):
        return "Successfully authorized pollease for slack team."
    else:
        return "Error authorizing pollease for slack team."

@app.route('/pollease', methods=['POST'])
def pollease():
    command_text = request.form["text"]

    try:
        command, command_params = command_parser.parse_pollease_command(command_text)

        if command == COMMAND_CREATE:
            return create_poll(command_params)
        elif command == COMMAND_CLOSE:
            return close_poll()

    except CommandParsingException as e:
        return generate_return_message(str(e))
    except Exception:
        return generate_return_message(ERR_UNKNOWN)

    return generate_return_message(ERR_UNKNOWN)

@app.route('/interactive', methods=['POST'])
def interactive():
    logger.info("WOOHOO!")

@app.errorhandler(Exception)
def handle_error(exception):
    logger.error("An exception occurred: " + repr(exception))
    logger.error(traceback.format_exc())


def create_poll(command_params):
    poll_name, voting_choices = command_parser.parse_create_command(command_params)

    if current_poll is None:
        logger.info("Creating poll: " + poll_name)
        return generate_new_poll_response(poll_name, voting_choices)
    else:
        logger.info("Failed to create poll: " + poll_name + \
        ". Another poll is already in progress.")
        return generate_return_message(ERR_POLL_ALREADY_IN_PROGRESS)

def close_poll():
    global current_poll

    if current_poll is None:
        return generate_return_message(ERR_NO_POLL_IN_PROGRESS)
    else:
        poll_name = current_poll.get("text")
        logger.info("Closing poll: " + poll_name)

        current_poll = None
        return generate_return_message("Poll: '" + poll_name + "' has now been closed.")

def generate_new_poll_response(poll_name, voting_choices):
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

    global current_poll
    current_poll = {
        "text": poll_name,
        "attachments": attachments,
        "response_url": "https://0665a1ee.ngrok.io/test"
    }

    return current_poll

def generate_return_message(message):
    return {
        "text": message
        }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
