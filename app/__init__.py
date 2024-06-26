import os

from flask import Flask

import manage
from app.blueprint import register_routing
from app.db import db
from app.extention import cors, migrate
from app.utils.logging import configure_logging


def create_app(settings_module):
    app = Flask(__name__)
    app.config.from_object(settings_module)

    # Initialize the extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, supports_credentials="true", resources={r"*": {"origins": "*"}})
    manage.init_app(app)

    # Logging configuration
    configure_logging(app)

    # Register Blueprint
    register_routing(app)

    return app


app = create_app(
    os.getenv("APP_SETTINGS_MODULE")
)
