"""Database constants"""
SQL_CREATE_POLLS_TABLE = """CREATE TABLE IF NOT EXISTS polls (
                                        id text PRIMARY KEY,
                                        team_id text NOT NULL,
                                        team_domain text NOT NULL,
                                        channel_id text NOT NULL,
                                        channel_name text NOT NULL,
                                        name text NOT NULL,
                                        date_open long NOT NULL,
                                        date_close long NOT NULL,
                                        owner_user_id text NOT NULL
                                    );"""

SQL_CREATE_POLL_CHOICES_TABLE = """CREATE TABLE IF NOT EXISTS poll_choices (
                                id text PRIMARY KEY,
                                name text NOT NULL,
                                poll_id text NOT NULL,
                                FOREIGN KEY (poll_id) REFERENCES polls (id)
                            );"""

SQL_CREATE_VOTES_TABLE = """CREATE TABLE IF NOT EXISTS votes (
                                poll_id text NOT NULL,
                                choice_id text NOT NULL,
                                voter_user_id text NOT NULL,
                                FOREIGN KEY (poll_id) REFERENCES polls (id),
                                FOREIGN KEY (choice_id) REFERENCES poll_choices (id),
                                PRIMARY KEY(poll_id, choice_id, voter_user_id)
                            );"""

SQL_PERSIST_POLL = """INSERT INTO polls VALUES ('{0}', '{1}', '{2}', '{3}', '{4}',
                                                '{5}', '{6}', '{7}', '{8}');"""

SQL_PERSIST_POLL_CHOICES = "INSERT INTO poll_choices VALUES ('%s', '%s', '%s');"

SQL_PERSIST_POLL_VOTE = "INSERT INTO votes VALUES ('%s', '%s', '%s');"

SQL_FETCH_POLL = "SELECT * FROM polls WHERE id='%s' LIMIT 1;"

SQL_FETCH_OPEN_POLL_BY_CHANNEL = """SELECT * FROM polls WHERE
                                    team_id='{0}' AND 
                                    channel_id='{1}' AND 
                                    date_close > {2} 
                                    LIMIT 1;"""

SQL_FETCH_POLL_TOP1 = "SELECT * FROM polls LIMIT 1;"

SQL_FETCH_POLL_CHOICES = "SELECT * FROM poll_choices WHERE poll_id='%s';"

SQL_FETCH_POLL_VOTES = "SELECT * FROM votes WHERE poll_id='%s' LIMIT 1;"

SQL_FETCH_POLL_VOTE_BY_POLL_AND_USER = "SELECT choice_id FROM votes WHERE poll_id='%s' \
 AND voter_user_id='%s' LIMIT 1;"

SQL_UPDATE_POLL_VOTE = "UPDATE votes SET choice_id='%s' WHERE poll_id='%s' \
 AND voter_user_id='%s';"

SQL_UPDATE_POLL = """UPDATE polls
    SET date_close = {1}
    WHERE id = '{0}';"""