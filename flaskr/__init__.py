import os 

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from .config import Config
from .models import db
from .blueprints.pages import populate_pages


# This creates the Flask app.  This is just an instance of the Flask class for now
def create_app(test_config=None):
    # We create an app with all configuration files stored relative to the route folder here.
    app = Flask(__name__)
    CORS(app, resources={r"/page/*": {"origins": "http://localhost:3000"}})

    app.config.from_object(Config)
    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()
        populate_pages()

    # App Config:
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)


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
    from .blueprints import graph, notes, pages, entities
    # app.register_blueprint(auth.bp)
    app.register_blueprint(graph.bp)
    app.register_error_handler(graph.NodeNotFoundError, graph.handle_node_not_found_error)
    app.register_error_handler(graph.InvalidNodeIDError, graph.handle_invalid_node_id_error)
    app.register_error_handler(entities.RequestJSONBodyError, entities.handle_bad_json_body_error)
    app.register_error_handler(entities.RecordAlreadyExists, entities.handle_record_already_exists_error)

    app.register_blueprint(notes.bp)
    app.register_blueprint(pages.bp)
    app.register_blueprint(entities.people_bp)
    app.register_blueprint(entities.loc_bp)
    app.register_blueprint(entities.event_bp)
    app.register_blueprint(entities.tag_bp)
    app.add_url_rule('/', endpoint='hello')
    
    return app
