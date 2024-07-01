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


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))

# This decorator defines a cmd line command (init-bd) which calls the following code
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialised the database')


# We need to initialise the above commands when our app is started otherwise it won't know to run them
# teardown_appcontext means "call this when cleaning up after a response"
# cli.add_command means "make this a command that flask can execute"
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
