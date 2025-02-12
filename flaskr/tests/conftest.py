import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.models import db

# This mimics the app instanciation in __init__.py
@pytest.fixture
def app():
    # Create TEMPORARY database file for testing
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })
    
    """
    'yield' is like 'return' except it returns generators.
    What is a generator?  It's a type of iterable that can only be used ONCE
    This means, when the function is called, the code doesn't run but a generator is returned.
    The code is only run when the values in this generator are accessed.
    It's better for memory as once the value is read/the things in the generator are accessed,
    they are not stored so memory is freed up.
    """
    yield app

    os.close(db_fd)
    os.unlink(db_path)


# Run the tests on a dedicated test client so not interfere with the server
@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


# Provide a database session for each test
@pytest.fixture
def session(app):
    with app.app_context():
        db.session.begin_nested()  # Start a savepoint
        yield db.session
        db.session.rollback()  # Rollback after test
