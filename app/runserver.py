"""
    I0011 - inline pylint disables
    C0103 - variables should b named in constants convention
    W0403 - relative imports
"""
# pylint: disable=I0011,C0103,W0403
import os
import sys

# Used to solve issue with relative imports
sys.path.insert(0, os.path.abspath(".."))

from api.pollease_api import pollease_api
from flask import g, request
from flask_api import FlaskAPI

"""
    pollease - A Slack poll integration.
    Written by Adam Rehill and Adam Krieger, 2016
"""

app = FlaskAPI(__name__)
app.register_blueprint(pollease_api)

# This must be present in this file as blueprint doesn't have teardown context
@app.teardown_appcontext
def close_connection(exception):
    """Closes the connection upon loss of context."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    print "\nStarting pollease flask server...logging will now appear in papertrail"
    app.run(debug=True, host='0.0.0.0', port=8080, use_reloader=False)
