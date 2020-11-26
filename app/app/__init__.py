"""Root package."""

import os
from flask_api import FlaskAPI
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()
BCRYPT = Bcrypt()

curr_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(curr_dir, os.pardir))

def create_app(config_type):
    """App factory.

    Args:
        config_type: Name of the config file without extension.
    Returns:
        App object.
    """
    # Create app with specified configuration.
    app = FlaskAPI(__name__)

    configuration = os.path.join(root_dir, 'config', str(config_type) + '.py')
    app.config.from_pyfile(configuration)

    # Initialize extensions for current app.
    DB.init_app(app)
    BCRYPT.init_app(app)

    # Import and register blueprints.
    from app.auth import authentication
    from app.utils import utils
    from app.hello import hello

    app.register_blueprint(authentication)
    app.register_blueprint(utils)
    app.register_blueprint(hello)

    return app
