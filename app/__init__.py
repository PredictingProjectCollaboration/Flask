from flask import Flask
import redis
import config
from app.blueprints.upload_redis_blueprint.upload_controller import upload_bp
from app.blueprints.home_blueprint.app import home_bp


def create_app(config_class=config.Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app

    # Register blueprints
    app.register_blueprint(upload_bp)
    app.register_blueprint(home_bp)

    # You might also set up error handlers, context processors, etc. here

    return app
