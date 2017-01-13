"""
    I0011 - inline pylint disables
    C0103 - variables should b named in constants convention
    W1202 - The % format is officially obsolete.
"""
# pylint: disable=I0011,C0103,C0111,W1202

import sqlite3
import arrow
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
            logger.info("Persisting poll {0}. Team: {1} Channel: {2} Expires: {3}".format( \
                poll.poll_id, poll.team_id, poll.channel_id, arrow.get(poll.date_close)))

            sql = SQL_PERSIST_POLL.format(poll.poll_id, \
                poll.team_id, poll.team_domain, poll.channel_id, poll.channel_name, \
                poll.name, poll.date_open, poll.date_close, poll.owner_user_id)
            db_conn.execute(sql)

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
            previous_vote = self.fetch_vote_for_poll_and_user(db_conn, poll_id, voter_user_id)

            if previous_vote is None:
                db_conn.execute(SQL_PERSIST_POLL_VOTE % (poll_id, poll_choice_id, voter_user_id))
                db_conn.commit()
            else:
                db_conn.execute(SQL_UPDATE_POLL_VOTE % (poll_choice_id, poll_id, voter_user_id))
                db_conn.commit()

        except sqlite3.Error as e:
            logger.info("Error inserting vote for poll: " + poll_id + " poll_choice_id: " \
             + poll_choice_id + " voter_user_id: " + voter_user_id + " into the database. " \
             + str(e))
            raise PolleaseException(ERR_CREATING_VOTE)

    def fetch_poll(self, db_conn, poll_id):
        """Fetches a poll from the polls table. Returns a Poll object"""
        try:
            cursor = db_conn.execute(SQL_FETCH_POLL % poll_id)

            poll = None
            #Should only be one row in the cursor due to the limit
            for row in cursor:
                poll = self.__poll_from_row(db_conn, row)

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
                    poll = self.__poll_from_row(db_conn, row)
                return poll
        except sqlite3.Error as e:
            logger.info("Error retrieving first poll from the database. " + str(e))
            raise PolleaseException(ERR_FETCHING_POLL)

    def fetch_poll_by_channel(self, db_conn, team_id, channel_id, now):
        """Fetches the poll by team_id and channel_id.
            Assumes one poll per channel."""
        poll = None

        logger.info("Trying to fetch for {0}.{1} at {2}".format( \
            team_id, channel_id, now))

        try:
            sql = SQL_FETCH_OPEN_POLL_BY_CHANNEL.format(team_id, channel_id, now)
            cursor = db_conn.execute(sql)
            for row in cursor:
                poll = self.__poll_from_row(db_conn, row)
        except sqlite3.Error as e:
            logger.info("Error retrieving poll from the database. " + str(e))
            raise PolleaseException(ERR_FETCHING_POLL)

        return poll

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

    def fetch_vote_for_poll_and_user(self, db_conn, poll_id, voter_user_id):
        """Returns the poll_choice_id (vote) for a poll_id and voter_user_id"""
        try:
            cursor = db_conn.execute(SQL_FETCH_POLL_VOTE_BY_POLL_AND_USER % \
             (poll_id, voter_user_id))

            poll_choice_id = None
            for row in cursor:
                poll_choice_id = row[0]

            return poll_choice_id
        except sqlite3.Error as e:
            logger.info("Error retrieving vote for poll " + poll_id + \
            " user_id: " + voter_user_id + " from the database. " + str(e))
            raise PolleaseException(ERR_FETCHING_POLL_VOTES)

    def update_poll(self, db_conn, poll):
        """Updates the poll in the database with the given values."""
        sql = SQL_UPDATE_POLL.format(poll.poll_id, poll.date_close)

        db_conn.execute(sql)
        db_conn.commit()

    def __run_sql(self, sql, custom_error):
        try:
            cursor = self.conn.execute(sql)

            return cursor
        except sqlite3.Error as e:
            logger.info("SQL Error " + str(e))
            raise PolleaseException(custom_error)

    def __poll_from_row(self, db_conn, row):
        return Poll(row[0], row[1], row[2], row[3], row[4], row[5], \
                row[6], row[7], row[8], \
                self.fetch_poll_choices(db_conn, row[0]))
