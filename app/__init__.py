from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .config import Config

from .db.connection import Database

import os

import atexit

jwt = JWTManager()

db = None  # global reference


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    jwt.init_app(app)
    CORS(app, origins=["http://127.0.0.1:3000"], supports_credentials=True)

    from .features import blueprints

    # Register each blueprint and add a URL prefix
    for name, bp in blueprints.items():
        app.register_blueprint(bp, url_prefix=f"/api/{name}")

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug:
        db = Database()
        db.init_app(app)
        app.extensions["db"] = db

    # @app.teardown_appcontext
    # def close_db(exception=None):
    #     db = app.extensions.get("db")
    #     if db:
    #         db.close()

    # Extra safety: ensure clean shutdown even on Ctrl+C or reloader exit
    atexit.register(lambda: app.extensions.get("db") and app.extensions["db"].close())

    return app
