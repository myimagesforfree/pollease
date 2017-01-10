"""
    I0011 - inline pylint disables
    C0103 - variables should b named in constants convention
"""
# pylint: disable=I0011,C0103,C0111

import sqlite3

from custom_exceptions import PolleaseException
from db_constants import *
from constants import *
from models.poll import Poll, PollChoice
from papertrail import logger

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
        """Creates all tables in the database"""
        self.conn.execute(SQL_CREATE_POLLS_TABLE)
        self.conn.execute(SQL_CREATE_POLL_CHOICES_TABLE)
        self.conn.execute(SQL_CREATE_VOTES_TABLE)
        self.conn.commit()

    def persist_poll(self, db_conn, poll):
        """Persists a poll object to the polls table"""
        try:
            db_conn.execute(SQL_PERSIST_POLL % (poll.poll_id, poll.team_id, poll.channel_id, \
            poll.name, poll.is_open, poll.owner_user_id))

            self.persist_poll_choices(db_conn, poll)
            db_conn.commit()
        except sqlite3.Error as e:
            logger.info("Error inserting poll into the database. " + str(e))
            raise PolleaseException(ERR_CREATING_POLL)

    def persist_poll_choices(self, db_conn, poll):
        """Persists poll choices to the poll_choices table"""
        #Could be more efficient by doing in batch insert, but this should be a very small list
        for choice in poll.poll_choices:
            db_conn.execute(SQL_PERSIST_POLL_CHOICES % (choice.choice_id, choice.name, \
            poll.poll_id))

    def persist_vote(self, db_conn, poll_id, poll_choice_id, voter_user_id):
        """Persists a vote to the votes table"""
        try:
            db_conn.execute(SQL_PERSIST_VOTE % (poll_id, poll_choice_id, voter_user_id))
            db_conn.commit()
        except sqlite3.Error as e:
            logger.info("Error inserting vote for poll: " + poll_id + " poll_choice_id: " \
             + poll_choice_id + " voter_user_id: " + voter_user_id + " into the database.")
            raise PolleaseException(ERR_CREATING_VOTE)

    def fetch_poll(self, db_conn, poll_id):
        """Fetches a poll from the polls table. Returns a Poll object"""
        try:
            cursor = db_conn.execute(SQL_FETCH_POLL % poll_id)

            poll = None
            #Should only be one row in the cursor due to the limit
            for row in cursor:
                poll = Poll(row[0], row[1], row[2], row[3], row[4], row[5], \
                self.fetch_poll_choices(db_conn, poll_id))

            return poll
        except sqlite3.Error as e:
            logger.info("Error retrieving poll " + poll_id + " from the database. " + str(e))
            raise PolleaseException(ERR_FETCHING_POLL)

    def fetch_poll_choices(self, db_conn, poll_id):
        """Fetches poll_choices from the poll_choices table. Returns a list of PollChoices """
        cursor = db_conn.execute(SQL_FETCH_POLL_CHOICES % poll_id)

        poll_choices = []
        for row in cursor:
            poll_choices.append(PollChoice(row[0], row[1]))

        return poll_choices

    def fetch_first_poll(self, db_conn):
        """Fetches the top most poll from the polls table. Returns a Poll object"""
        try:
            cursor = db_conn.execute(SQL_FETCH_POLL_TOP1)

            if not cursor:
                return None
            else:
                poll = None
                for row in cursor:
                    poll = Poll(row[0], row[1], row[2], row[3], row[4], row[5], \
                    self.fetch_poll_choices(db_conn, row[0]))
                return poll
        except sqlite3.Error as e:
            logger.info("Error retrieving first poll from the database. " + str(e))
            raise PolleaseException(ERR_FETCHING_POLL)

    def fetch_poll_votes(self, db_conn, poll_id):
        """Fetches the poll_votes from the votes table. Returns a list dictionary of \
        poll_choice_id's (key) and a list of the users who voted for them (value)"""
        try:
            cursor = db_conn.execute(SQL_FETCH_POLL_VOTES % poll_id)

            poll_choices = self.fetch_poll_choices(db_conn, poll_id)

            poll_votes = {key: [] for key in poll_choices}

            for row in cursor:
                poll_choice_id = row[1]
                voter_user_id = row[2]
                poll_votes[poll_choice_id].append(voter_user_id)

            return poll_votes
        except sqlite3.Error as e:
            logger.info("Error retrieving poll_votes for poll " + poll_id + \
            " from the database. " + str(e))
            raise PolleaseException(ERR_FETCHING_POLL_VOTES)

    def __run_sql(self, sql):
        try:
            cursor = self.conn.execute(sql)

            return cursor
        except sqlite3.Error as e:
            logger.info("SQL Error " + str(e))
            raise PolleaseException(ERR_UNKNOWN)
