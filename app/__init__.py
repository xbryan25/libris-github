from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .config import Config

from .db.connection import Database

import os

import atexit

jwt = JWTManager()

db = None  # global reference


def create_app():

    app = Flask(__name__, static_folder="static", template_folder="templates")

    NUXT_DIST_DIR = os.path.join(os.path.dirname(__file__), "static")
    NUXT_ASSETS_DIR = os.path.join(os.path.dirname(__file__), "static", "_nuxt")

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
    #     if db and db.pool and not db.pool.closed:
    #         db.close()

    # Close pool gracefully only when the app exits
    atexit.register(lambda: app.extensions.get("db") and app.extensions["db"].close())

    @app.route("/_nuxt/<path:filename>")
    def nuxt_static(filename):
        return send_from_directory(NUXT_ASSETS_DIR, filename)

    @app.route("/images/<path:filename>")
    def nuxt_images(filename):
        return send_from_directory(os.path.join(NUXT_DIST_DIR, "images"), filename)

    @app.route("/_ipx/_/images/<path:filename>")
    def ipx_fallback(filename):
        # Serve images that Nuxt Image tries to optimize via IPX
        return send_from_directory(os.path.join(NUXT_DIST_DIR, "images"), filename)

    @app.route("/favicon.svg")
    def favicon_svg():
        return send_from_directory(NUXT_DIST_DIR, "favicon.svg")

    # Serve index.html for any non-API route
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):
        # Prevent catching API routes
        if path.startswith("api/"):
            return jsonify({"error": "Not Found"}), 404
        return render_template("index.html")

    return app
