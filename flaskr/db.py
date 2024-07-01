import sqlite3

import click
from flask import current_app, g
# g is a special object unique for each request used to store data that might be accessed by multiple functions during the request.


# At the begining of the request, we make a connection to the DB
def get_db():
    if 'db' not in g:
        # Our app is built in __init__.py so we call current_app for config info
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


# Closes the connection (if one was created)
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()