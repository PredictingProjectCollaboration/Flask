# This file makes the 'upload_controllers' directory a Python package.

from flask import Blueprint,g, current_app as app
import redis


# It's good practice to prefix API-like routes.
upload_bp = Blueprint('upload_bp', __name__, url_prefix='/api')

@upload_bp.before_request
def before_upload_request():
    try:
        redis_client = redis.Redis(
                host=app.config['REDIS_HOST'],
                port=app.config['REDIS_PORT'],
                db=app.config['REDIS_DB'],
                decode_responses=True
            )
        g.redis_client = redis_client
    except redis.exceptions.ConnectionError as e:
        app.logger.error(f"Failed to connect to Redis: {e}")

    pass

    
