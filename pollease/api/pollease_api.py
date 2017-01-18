"""
    I0011 - inline pylint disables
    C0103 - variables should b named in constants convention
"""
# pylint: disable=I0011,C0103

import json
import sqlite3

import requests
from flask import Blueprint, g, request
from flask_api import FlaskAPI
from pollease.command_router import route_pollease_command
from pollease.config import (DB_PATH, SLACK_AUTH_URL, SLACK_CLIENT_ID,
                             SLACK_CLIENT_SECRET)
from pollease.papertrail import logger
from pollease.pollease_commands import cast_vote
from pollease.polls_repository import PollsRepository
from pollease.slack_command import SlackCommand

repo = PollsRepository(DB_PATH)
pollease_api = Blueprint('pollease_api', __name__)

@pollease_api.route('/authorize', methods=['GET'])
def authorize():
    """Authorizes this app with the central Slack app store. """
    code = request.args.get('code')

    query_string = "?client_id=%s&client_secret=%s&code=%s" % \
     (SLACK_CLIENT_ID, SLACK_CLIENT_SECRET, code)

    auth_request_url = SLACK_AUTH_URL + query_string

    response_json = requests.post(auth_request_url).json()

    if response_json.get("ok"):
        return "Successfully authorized pollease for slack team."
    else:
        return "Error authorizing pollease for slack team."

@pollease_api.route('/pollease', methods=['POST'])
def pollease():
    """Main command router for pollease actions."""

    logger.info(request.form)

    slack_command = SlackCommand(request.form)

    command = route_pollease_command(slack_command.text)
    db_conn = get_db()

    result = command(repo=repo, db_conn=db_conn, command_details=slack_command)

    return result

@pollease_api.route('/interactive', methods=['POST'])
def interactive():
    """Slack Interaction, for example when a user clicks a vote button."""
    logger.info(request.form.get("payload"))
    params = json.loads(request.form.get("payload"))

    voter_user_id = params.get("user").get("id")
    action_dict = params.get("actions")[0]

    vote_values = action_dict.get("value").split()
    poll_id, poll_choice_id = vote_values[0], vote_values[1]

    db_conn = get_db()
    return cast_vote(repo, db_conn, poll_id, poll_choice_id, voter_user_id)

def get_db():
    """Creates a database connection for use with this request flight."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
    return db
