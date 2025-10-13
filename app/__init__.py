from flask import Flask, current_app
from flask_cors import CORS

from .config import Config

from .db.connection import Database


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app, origins=["*"], supports_credentials=True)

    from .features import blueprints

    # Register each blueprint and add a URL prefix
    for name, bp in blueprints.items():
        app.register_blueprint(bp, url_prefix=f"/api/{name}")

    with app.app_context():
        # Comment the line below when testing
        current_app.extensions["db"] = Database()

        # Uncomment the next three lines when testing
        # db = Database()
        # current_app.extensions['db'] = db
        # db.test_supabase_connection()

    return app
