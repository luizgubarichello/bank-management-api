from flask import Flask
from flask_pymongo import PyMongo

from config import Config

mongo = PyMongo()


def create_app(config: type[Config] = Config) -> Flask:
    """Create a Flask application instance.

    Returns:
        Flask: A Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config)
    mongo.init_app(app)

    from app.views.account_routes import account_bp
    from app.views.transaction_routes import transaction_bp

    app.register_blueprint(account_bp, url_prefix="/api/v1/conta")
    app.register_blueprint(transaction_bp, url_prefix="/api/v1/transacao")

    return app
