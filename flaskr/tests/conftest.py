import os
import tempfile
import pytest
import logging as log
from flaskr import create_app
from flaskr.models import db as _db

# This mimics the app instanciation in the __init__.py file
@pytest.fixture(scope='function')
def app():
    # Create TEMPORARY database file for testing
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

    with app.app_context():
        _db.create_all()

    yield app

    with app.app_context():
        _db.drop_all()  # Cleanup after all tests

    os.close(db_fd)
    os.unlink(db_path)

# Run the tests on a dedicated test client so not interfere with the server
@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    return app.test_cli_runner()

# Provide a database session for each test
@pytest.fixture(scope='function')
def session(app):
    with app.app_context():
        connection = _db.engine.connect()
        transaction = connection.begin()
        options = dict(bind=connection, binds={})
        session = _db._make_scoped_session(options=options)
        _db.session = session

        yield session
        # For some reason, the transaction is not rolled back automatically

        transaction.rollback()
        connection.close()
        session.remove()