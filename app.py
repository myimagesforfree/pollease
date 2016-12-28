"""
    pollease - A Slack poll integration.
    Written by Adam Rehill and Adam Krieger, 2016
"""
from bottle import error, route, run, template, request
import command_parser
import logging
import socket
from logging.handlers import SysLogHandler
from papertrail import Papertrail

ERR_POLL_ALREADY_IN_PROGRESS = "Error. There is already a poll in progress. " + \
    "Please close that poll first."

TEST_DICTIONARY = {'data': []}
CURRENT_POLL = None

LOGGER = Papertrail().get_papertrail_logger()

@route('/')
def home():
    return TEST_DICTIONARY

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/bjork', method='POST')
def do_a_thing():
    TEST_DICTIONARY['data'].append(request.body.read())

@route('/create', method='POST')
def create_poll():
    if CURRENT_POLL is not None:
        raw_json = request.json
        command_text = raw_json.get("text")
        poll_name, voting_choices = command_parser.parse_create_command(command_text)

        LOGGER.info("Creating poll: " + poll_name)
        return generate_new_poll_response(poll_name, voting_choices)
    else:
        LOGGER.info("Failed to create poll: " + poll_name + \
        ". Another poll is already in progress.")
        return generate_error_response(ERR_POLL_ALREADY_IN_PROGRESS)

@route('/close', method='POST')
def close_poll():
    global CURRENT_POLL
    LOGGER.info("Closing poll: " + CURRENT_POLL.get("text"))
    CURRENT_POLL = None

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

    global CURRENT_POLL

    CURRENT_POLL = {
        "text": poll_name,
        "attachments": attachments
    }

    return CURRENT_POLL

def generate_error_response(error_message):
    return {
        "text": error_message
        }

@error(500)
def handle_error(error):
    LOGGER.error("An exception occurred: " + error)

run(host='0.0.0.0', port=8080)
