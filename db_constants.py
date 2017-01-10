SQL_CREATE_POLLS_TABLE = """CREATE TABLE IF NOT EXISTS polls (
                                        id text PRIMARY KEY,
                                        team_id text NOT NULL,
                                        channel_id text NOT NULL,
                                        name text NOT NULL,
                                        is_open integer NOT NULL,
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

SQL_PERSIST_POLL = "INSERT INTO polls VALUES ('%s', '%s', '%s', '%s', %d, '%s');"

SQL_PERSIST_POLL_CHOICES = "INSERT INTO poll_choices VALUES ('%s', '%s', '%s');"

SQL_PERSIST_VOTE = "INSERT INTO votes VALUES ('%s', '%s', '%s');"

SQL_FETCH_POLL = "SELECT * FROM polls WHERE id='%s' LIMIT 1;"

SQL_FETCH_POLL_TOP1 = "SELECT * FROM polls LIMIT 1;"

SQL_FETCH_POLL_CHOICES = "SELECT * FROM poll_choices WHERE poll_id='%s';"

SQL_FETCH_POLL_VOTES = "SELECT * FROM votes WHERE poll_id='%s' LIMIT 1;"
