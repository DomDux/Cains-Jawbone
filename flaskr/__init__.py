import os 

from flask import Flask 


# This creates the Flask app.  This is just an instance of the Flask class for now
def create_app(test_config=None):
    # We create an app with all configuration files stored relative to the route folder here.
    app = Flask(__name__, instance_relative_config=True)

    # App Config:
    #  SECRET_KEY is for security/encryption but is 'dev' as a placeholder for now
    #  DATABASE gives the location of the sqlite database Flask will be running
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )


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
    

    # Database connection config
    from .import db
    db.init_app(app)

    # Blueprints:  Views are functions to respond to requests.  Blueprints are groups of related views.
    from . import auth
    app.register_blueprint(auth.bp)
    
    return app
