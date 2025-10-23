from flask import Flask, current_app
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .config import Config

from .db.connection import Database

import os

jwt = JWTManager()


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
        with app.app_context():
            current_app.extensions["db"] = Database()

    return app
