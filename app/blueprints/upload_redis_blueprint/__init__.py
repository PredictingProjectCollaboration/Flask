# This file makes the 'upload_controllers' directory a Python package.

from flask import Blueprint,g, current_app as app
import redis


# It's good practice to prefix API-like routes.
upload_bp = Blueprint('upload_bp', __name__, url_prefix='/api')

@upload_bp.before_request
def before_upload_request():
    if not hasattr(g, 'redis_client'): # Check to avoid re-assigning if other before_request did
        g.redis_client = app.redis_client
        print("--- g.redis_client set as reference to global client ---")
    pass

    
