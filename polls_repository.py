"""
    I0011 - inline pylint disables
    C0103 - variables should b named in constants convention
    C0111 - no docstring present
"""
# pylint: disable=I0011,C0103,C0111

import sqlite3
from papertrail import logger
from db_constants import *
from models.poll import Poll, PollChoice

def get_connection(db_path):
    return sqlite3.connect(db_path)

class PollsRepository(object):

    def __init__(self, db_path):
        try:
            self.conn = get_connection(db_path)
            self.build_db()
            logger.info("Successfully initialized sqlite3 pollease database.")
        except sqlite3.Error as e:
            logger.info("Error initializing sqlite3 pollease database. " + str(e))

    def build_db(self):
        self.conn.execute(SQL_CREATE_POLLS_TABLE)
        self.conn.execute(SQL_CREATE_POLL_CHOICES_TABLE)
        self.conn.execute(SQL_CREATE_VOTES_TABLE)
        self.conn.commit()

    def persist_poll(self, db_conn, poll):
        try:
            db_conn.execute(SQL_PERSIST_POLL % (poll.poll_id, poll.team_id, poll.channel_id, \
            poll.name, poll.is_open, poll.owner_user_id))

            self.persist_poll_choices(db_conn, poll)
            db_conn.commit()

            logger.info("Successfully inserted poll " + poll.poll_id + " into the database.")
            return poll
        except sqlite3.Error as e:
            logger.info("Error inserting poll into the database. " + str(e))
            return None

    def persist_poll_choices(self, db_conn, poll):
        #Could be more efficient by doing in batch insert, but this should be a very small list
        for choice in poll.poll_choices:
            db_conn.execute(SQL_PERSIST_POLL_CHOICES % (choice.choice_id, choice.name, \
            poll.poll_id))

    def fetch_poll(self, db_conn, poll_id):
        try:
            cursor = db_conn.execute(SQL_FETCH_POLL % poll_id)

            poll = None
            #Should only be one row in the cursor due to the limit
            for row in cursor:
                poll = Poll(row[0], row[1], row[2], row[3], row[4], row[5], \
                self.fetch_poll_choices(db_conn, poll_id))

            logger.info("Successfully retrieved poll " + poll.poll_id + " from the database.")

            return poll
        except sqlite3.Error as e:
            logger.info("Error retrieving poll " + poll_id + " from the database. " + str(e))
            return None

    def fetch_poll_choices(self, db_conn, poll_id):
        cursor = db_conn.execute(SQL_FETCH_POLL_CHOICES % poll_id)

        poll_choices = []
        for row in cursor:
            poll_choices.append(PollChoice(row[0], row[1]))

        return poll_choices

    def select_first_poll(self, db_conn):
        cursor = db_conn.execute(SQL_FETCH_POLL_TOP1)

        if not cursor:
            return None
        else:
            poll = None
            for row in cursor:
                poll = Poll(row[0], row[1], row[2], row[3], row[4], row[5], \
                self.fetch_poll_choices(db_conn, row[0]))
            return poll

    def __run_sql(self, sql):
        try:
            cursor = self.conn.execute(sql)

            return cursor
        except sqlite3.Error as e:
            logger.info("SQL Error " + str(e))
            return None
