"""
    I0011 - inline pylint disables
    C0103 - variables should b named in constants convention
    C0111 - no docstring present
"""
# pylint: disable=I0011,C0103,C0111

import sqlite3
from papertrail import logger
from db_constants import SQL_CREATE_POLL_OPTIONS_TABLE, SQL_CREATE_POLLS_TABLE, \
SQL_CREATE_VOTES_TABLE, SQL_CREATE_POLL, SQL_FETCH_POLL

def get_connection():
    return sqlite3.connect(':memory:')

class PollsRepository():

    def __init__(self):
        try:
            self.conn = get_connection()
            self.build_db()
            logger.info("Successfully initialized sqlite3 in-memory database.")
        except sqlite3.Error as e:
            logger.info("Error initializing sqlite3 in-memory database. " + str(e))

    def build_db(self):
        self.conn.execute(SQL_CREATE_POLLS_TABLE)
        self.conn.execute(SQL_CREATE_POLL_OPTIONS_TABLE)
        self.conn.execute(SQL_CREATE_VOTES_TABLE)
        self.conn.commit()

    def create_poll(self, poll):
        try:
            self.conn.execute(SQL_CREATE_POLL % (poll.id, poll.team_id, poll.channel_id, \
            poll.name, poll.is_open, poll.owner_user_id))
            self.conn.commit()
            logger.info("Successfully inserted poll " + poll.id + " into the database.")
        except sqlite3.Error as e:
            logger.info("Error inserting poll into the database. " + str(e))

    def fetch_poll(self, poll_id):
        try:
            cursor = self.conn.execute(SQL_FETCH_POLL % poll_id)

            poll = None
            for row in cursor:
                poll = Poll(row[0], row[1], row[2], row[3], row[4], row[5])


            logger.info("Successfully retrieved poll " + poll.id + " from the database.")

            return poll
        except sqlite3.Error as e:
            logger.info("Error retrieving poll " + poll.id + " from the database. " + str(e))
            return None

class Poll():
    def __init__(self, poll_id, team_id, channel_id, name, is_open, owner_user_id):
        self.id = poll_id
        self.team_id = team_id
        self.channel_id = channel_id
        self.name = name
        self.is_open = is_open
        self.owner_user_id = owner_user_id

