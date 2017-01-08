"""
    I0011 - inline pylint disables
    C0103 - variables should b named in constants convention
    C0111 - no docstring present
"""
# pylint: disable=I0011,C0103,C0111

import sqlite3
from papertrail import logger
from db_constants import *
from models.poll import Poll

def get_connection(db_path):
    return sqlite3.connect(db_path)

class PollsRepository(object):

    def __init__(self, db_path):
        try:
            self.conn = get_connection(db_path)
            self.build_db()
            logger.info("Successfully initialized sqlite3 in-memory database.")
        except sqlite3.Error as e:
            logger.info("Error initializing sqlite3 in-memory database. " + str(e))

    def build_db(self):
        self.conn.execute(SQL_CREATE_POLLS_TABLE)
        self.conn.execute(SQL_CREATE_POLL_OPTIONS_TABLE)
        self.conn.execute(SQL_CREATE_VOTES_TABLE)
        self.conn.commit()

    def create_poll(self, db_conn, poll):
        try:
            db_conn.execute(SQL_CREATE_POLL % (poll.poll_id, poll.team_id, poll.channel_id, \
            poll.name, poll.is_open, poll.owner_user_id))
            db_conn.commit()
            logger.info("Successfully inserted poll " + poll.poll_id + " into the database.")
        except sqlite3.Error as e:
            logger.info("Error inserting poll into the database. " + str(e))

    def fetch_poll(self, poll_id):
        try:
            cursor = self.conn.execute(SQL_FETCH_POLL % poll_id)

            poll = None
            for row in cursor:
                poll = Poll(row[0], row[1], row[2], row[3], row[4], row[5])


            logger.info("Successfully retrieved poll " + poll.poll_id + " from the database.")

            return poll
        except sqlite3.Error as e:
            logger.info("Error retrieving poll " + poll.id + " from the database. " + str(e))
            return None

    def select_first_poll(self, db_conn):
        cursor = db_conn.execute(SQL_FETCH_POLL_TOP1)

        if not cursor:
            return None
        else:
            poll = None
            for row in cursor:
                poll = Poll(row[0], row[1], row[2], row[3], row[4], row[5])
            return poll

    def __run_sql(self, sql):
        try:
            cursor = self.conn.execute(sql)

            return cursor
        except sqlite3.Error as e:
            logger.info("SQL Error " + str(e))
            return None
