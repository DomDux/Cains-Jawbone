import tempfile
from flaskr import create_app


def test_config():
    db_fd, db_path = tempfile.mkstemp()
    test_config ={
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    }
    assert not create_app().testing
    assert create_app(test_config).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello World!'
