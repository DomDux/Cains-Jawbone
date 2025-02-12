import os
import tempfile
import pytest
from flaskr import create_app
from flaskr.models import db

# This mimics the app instanciation in the __init__.py file
@pytest.fixture(scope='session')
def app():
    # Create TEMPORARY database file for testing
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

    with app.app_context():
        # db.init_app(app)
        db.create_all()

    yield app


    with app.app_context():
        db.drop_all()  # Cleanup after all tests

    os.close(db_fd)
    os.unlink(db_path)



# Run the tests on a dedicated test client so not interfere with the server
@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

@pytest.fixture(scope='session')
def runner(app):
    return app.test_cli_runner()

# Provide a database session for each test
@pytest.fixture(scope='function')
def session(app):
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        
        db.session.configure(bind=connection)

        yield db.session

        transaction.rollback()
        connection.close()
        db.session.remove()