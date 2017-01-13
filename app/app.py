"""
    I0011 - inline pylint disables
    C0103 - variables should b named in constants convention
"""
# pylint: disable=I0011,C0103

import sqlite3
import traceback

import json
import command_parser
import requests
from config import (DB_PATH, SLACK_AUTH_URL, SLACK_CLIENT_ID,
                    SLACK_CLIENT_SECRET)
from custom_exceptions import CommandParsingException
from flask import g, request
from flask_api import FlaskAPI
from models.slack_command import SlackCommand
from papertrail import logger
from polls_repository import PollsRepository
from pollease import cast_vote, generate_return_message

"""
    pollease - A Slack poll integration.
    Written by Adam Rehill and Adam Krieger, 2016
"""
app = FlaskAPI(__name__)
repo = PollsRepository(DB_PATH)

@app.route('/authorize', methods=['GET'])
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

@app.route('/pollease', methods=['POST'])
def pollease():
    """Main command router for pollease actions."""

    command_details = SlackCommand(request.form)

    try:
        command = command_parser.parse_pollease_command(command_details.text)

        db_conn = get_db()
        result = command(repo=repo, db_conn=db_conn, command_details=command_details)

        return result

    except CommandParsingException as e:
        return generate_return_message(str(e))

@app.route('/interactive', methods=['POST'])
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

@app.errorhandler(Exception)
def handle_error(exception):
    """Outer exception handler."""
    logger.error("An exception occurred: " + repr(exception))
    logger.error(traceback.format_exc())

def get_db():
    """Creates a database connection for use with this request flight."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Closes the connection upon loss of context."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
