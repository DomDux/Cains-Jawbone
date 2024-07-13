import os 

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .config import Config
from .models import db


# This creates the Flask app.  This is just an instance of the Flask class for now
def create_app(test_config=None):
    # We create an app with all configuration files stored relative to the route folder here.
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    # App Config:
    #  SECRET_KEY is for security/encryption but is 'dev' as a placeholder for now
    #  DATABASE gives the location of the sqlite database Flask will be running
    """ app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    ) """


    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # Basic Route:
    @app.route('/hello')
    def hello():
        return 'Hello World!'
    

    # Blueprints:  
    # Views are functions to respond to requests.  
    # Blueprints are groups of related views.
    from . import graph
    # app.register_blueprint(auth.bp)
    app.register_blueprint(graph.bp)
    app.add_url_rule('/', endpoint='hello')
    
    return app
