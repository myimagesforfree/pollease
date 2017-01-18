"""
    I0011 - inline pylint disables
    C0103 - variables should b named in constants convention
"""
# pylint: disable=I0011,C0103

import traceback

from flask import g, request
from flask_api import FlaskAPI
from pollease.papertrail import logger
from pollease.api.pollease_api import pollease_api

"""
    pollease - A Slack poll integration.
    Written by Adam Rehill and Adam Krieger, 2016
"""
app = FlaskAPI(__name__)
app.register_blueprint(pollease_api)

@app.errorhandler(Exception)
def handle_error(exception):
    """Outer exception handler."""
    logger.error("An exception occurred: " + repr(exception))
    logger.error(traceback.format_exc())


@app.teardown_appcontext
def close_connection(exception):
    """Closes the connection upon loss of context."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
    print "Pollease started successfully"
    