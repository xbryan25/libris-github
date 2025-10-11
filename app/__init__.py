from flask import Flask
from flask_cors import CORS

from .config import Config

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app, origins=["*"], supports_credentials=True)
    
    from .features import blueprints

    # Register each blueprint and add a URL prefix
    for name, bp in blueprints.items():
        app.register_blueprint(bp, url_prefix=f'/api/{name}')

    return app
