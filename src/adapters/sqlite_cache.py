# this should use redis or some other production level DB,
# but that is outside the scope of this practice project
# so we are going to just get by with sqlite.

import time
import sqlite3


class SQLiteDBException(Exception):
    """Exception in passing sqlite db connection"""


# we are just going to open and close the DB connection over and over again.
# it is sqlite, so there won't be any network delay.
# a production DB would need to handle concurency safety and multiple connections,
# but doing that is outside the scope of this practice project.
def sqlite_db_wrapper(db_action):

    def wrapper(*args):
        connection = sqlite3.connect("my_database.db")
        cursor = connection.cursor()
        result = db_action(*args, connection=connection, cursor=cursor)
        connection.commit()
        connection.close()
        return result

    return wrapper


@sqlite_db_wrapper
def create_table(connection=None, cursor=None):
    if cursor is None or connection is None:
        raise SQLiteDBException("failed to get connection or cursor for transaction")
    cursor.execute(
        """\
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY NOT NULL,
    unix_time INTEGER NOT NULL,
    credentials TEXT,
    email BOOLEAN,
    profile BOOLEAN
    );
    """
    )


@sqlite_db_wrapper
def read(session_id: str, connection=None, cursor=None) -> dict:
    return non_decorated_read(session_id, connection=connection, cursor=cursor)


def non_decorated_read(session_id: str, connection=None, cursor=None) -> dict:
    if cursor is None or connection is None:
        raise SQLiteDBException("failed to get connection or cursor for transaction")

    cursor.execute(
        """\
SELECT session_id,
    unix_time,
    credentials,
    email,
    profile
FROM sessions
WHERE 
    session_id=?;
    """,
        (session_id,),
    )
    rows = cursor.fetchall()
    for row in rows:
        session_id, unix_time, credentials, email, profile = row
        result = {
            "session_id": session_id,
            "unix_time": unix_time,
            "credentials": credentials,
            "email": email,
            "profile": profile
        }
        return result
    return {}


@sqlite_db_wrapper
def write(
    session_id: str,
    unix_time: int,
    credentials: dict,
    email: bool,
    profile: bool,
    connection=None,
    cursor=None,
):
    if cursor is None or connection is None:
        raise SQLiteDBException("failed to get connection or cursor for transaction")
    session = non_decorated_read(session_id, connection=connection, cursor=cursor)

    now = int(time.time())
    older_than_one_day = now - unix_time > 86400
    if (session is None or not session) and not older_than_one_day:
        cursor.execute(
            """INSERT INTO sessions (
                session_id, 
                unix_time, 
                credentials, 
                email, 
                profile
            ) VALUES (?, ?, ?, ?, ?)""",
            (session_id, unix_time, str(credentials), email, profile),
        )
        return

    if older_than_one_day:
        delete(session_id, connection=connection, cursor=cursor)


@sqlite_db_wrapper
def delete(session_id: str, connection=None, cursor=None):
    if cursor is None or connection is None:
        raise SQLiteDBException("failed to get connection or cursor for transaction")

    cursor.execute("DELETE FROM sessions WHERE session_id=?", (session_id,))
