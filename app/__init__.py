import os
from flask import Flask
import redis
import config
from app.blueprints.upload_redis_blueprint.upload_controller import upload_bp
from app.blueprints.home_blueprint.app import home_bp
from flask_session import Session



def create_app(config_class=config.Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Redis client with the app
    try:
        redis_client = redis.Redis(
            host=app.config['REDIS_HOST'],
            port=app.config['REDIS_PORT'],
            db=app.config['REDIS_DB'],
            decode_responses=True
        )
        app.redis_client = redis_client
        app.redis_client.ping()
        app.logger.info("Successfully connected to Redis")
    except redis.exceptions.ConnectionError as e:
        app.logger.error(f"Failed to connect to Redis: {e}")

    # Ensure the session directory exists and Initialize Flask-Session
    if not os.path.exists(app.config["SESSION_FILE_DIR"]):
        os.makedirs(app.config["SESSION_FILE_DIR"])
    sess = Session(app)

        
    # Register blueprints
    app.register_blueprint(upload_bp)
    app.register_blueprint(home_bp)

    # You might also set up error handlers, context processors, etc. here

    return app
