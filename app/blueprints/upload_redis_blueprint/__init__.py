# This file makes the 'upload_controllers' directory a Python package.

from flask import Blueprint


# It's good practice to prefix API-like routes.
upload_bp = Blueprint('upload_bp', __name__, url_prefix='/api')