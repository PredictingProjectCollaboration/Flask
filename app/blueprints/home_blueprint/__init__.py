# This file makes the 'upload_controllers' directory a Python package.

from flask import Blueprint


# It's good practice to prefix API-like routes.
home_bp = Blueprint('home_bp', __name__, url_prefix='/')