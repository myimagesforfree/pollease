"""
    I0011 - inline pylint disables
    C0103 - variables should b named in constants convention
"""
# pylint: disable=I0011,C0103

import json
import sqlite3
import traceback

import requests
from flask import Blueprint, g, request
from flask_api import FlaskAPI
from app.resources.command_router import route_pollease_command
from app.config import get_config

from app.resources.logger import logger
from app.resources.pollease_commands import cast_vote
from app.repo.pollease_repository import PolleaseRepository
from app.domain.slack_command import SlackCommand

repo = PolleaseRepository(get_config().get("DATABASE", "DB_PATH"))
pollease_api = Blueprint('pollease_api', __name__)

@pollease_api.route('/authorize', methods=['GET'])
def authorize():
    """Authorizes this app with the central Slack app store. """
    code = request.args.get('code')

    query_string = "?client_id=%s&client_secret=%s&code=%s" % \
     (get_config().get("SLACK", "SLACK_CLIENT_ID"), get_config().get("SLACK", \
      "SLACK_CLIENT_SECRET"), code)

    auth_request_url = get_config().get("SLACK", "SLACK_AUTH_URL") + query_string

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

@pollease_api.errorhandler(Exception)
def handle_error(exception):
    """Outer exception handler."""
    logger.error("An exception occurred: " + repr(exception))
    logger.error(traceback.format_exc())

def get_db():
    """Creates a database connection for use with this request flight."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(get_config().get("DATABASE", "DB_PATH"))
    return db
