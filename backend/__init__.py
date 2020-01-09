import os

from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'backend.sqlite'),
    )

    if test_config is None:
        #load the instance config if exists
        app.config.from_pyfile('config.py', silent=True)
    else:
        #load test config
        app.config.from_mapping(test_config)

    #create instance folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        return 'Blub'
    
    from backend.util import db
    db.init_app(app)

    from . import register
    app.register_blueprint(register.bp)

    from . import login
    app.register_blueprint(login.bp)

    from . import information
    app.register_blueprint(information.bp)

    from . import user
    app.register_blueprint(user.bp)

    from . import configuration
    app.register_blueprint(configuration.bp) 

    return app