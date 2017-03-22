# external imports
from flask import Flask
from flask_bootstrap import Bootstrap
# local imports
from data.manager import ThreadManager

threadManager = ThreadManager()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.cfg')

    Bootstrap(app)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .thread import thread as thread_blueprint
    app.register_blueprint(thread_blueprint, url_prefix = '/thread')

    return app
