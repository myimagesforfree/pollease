"""
    I0011 - inline pylint disables
    C0103 - variables should b named in constants convention
    C0111 - no docstring present
"""
# pylint: disable=I0011,C0103,C0111
import sys
import traceback
import command_parser
from constants import ERR_POLL_ALREADY_IN_PROGRESS
from flask import request, url_for
from flask_api import FlaskAPI, exceptions, status
from papertrail import Papertrail

"""
    pollease - A Slack poll integration.
    Written by Adam Rehill and Adam Krieger, 2016
"""
logger = Papertrail().get_papertrail_logger()
current_poll = None

app = FlaskAPI(__name__)

@app.route('/create', methods=['POST'])
def create_poll():
    command_text = request.form["text"]
    poll_name, voting_choices = command_parser.parse_create_command(command_text)

    if current_poll is None:
        logger.info("Creating poll: " + poll_name)
        return generate_new_poll_response(poll_name, voting_choices)
    else:
        logger.info("Failed to create poll: " + poll_name + \
        ". Another poll is already in progress.")
        return generate_error_response(ERR_POLL_ALREADY_IN_PROGRESS)

@app.route('/close', methods=['POST'])
def close_poll():
    logger.info("Closing poll: " + current_poll.get("text"))
    current_poll = None

def generate_new_poll_response(poll_name, voting_choices):
    attachments = []

    for choice in voting_choices:
        attachments.append({
            {
                "text": choice,
                "fallback": "You are unable to vote",
                "callback_id": "vote_callback",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "vote",
                        "text": "Vote",
                        "type": "button",
                        "value": "true"
                    }
                ]
            }
        })

    CURRENT_POLL = {
        "text": poll_name,
        "attachments": attachments
    }

    return CURRENT_POLL

def generate_error_response(error_message):
    return {
        "text": error_message
        }

@app.errorhandler(Exception)
def handle_error(exception):
    logger.error("An exception occurred: " + repr(exception))
    logger.error(traceback.format_exc())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
