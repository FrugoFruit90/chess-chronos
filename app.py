import logging
import os

from flask import Flask
from flask_cors import CORS

from config import config

root = logging.getLogger()
logging.basicConfig(level=logging.INFO)
root.setLevel(logging.INFO)
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)


def create_app(app_environment=None):
    app = Flask(__name__)
    if app_environment is None:
        app.config.from_object(config[os.getenv('FLASK_ENV', 'dev')])
    else:
        app.config.from_object(config[app_environment])
    CORS(app)

    @app.route('/')
    def index():
        return

    return app


if __name__ == "__main__":
    app = create_app(os.getenv('FLASK_ENV', 'dev'))
    app.run()
