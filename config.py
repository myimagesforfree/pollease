PAPERTRAIL_SERVER = ""
PAPERTRAIL_PORT = 8080

SLACK_AUTH_URL = "https://slack.com/api/oauth.access"

SLACK_CLIENT_ID = ""

SLACK_CLIENT_SECRET = ""

try:
    from local_config import *
except ImportError as import_error:
    pass
