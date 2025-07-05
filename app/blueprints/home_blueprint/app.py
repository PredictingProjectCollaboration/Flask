from flask import Flask, render_template
from . import home_bp


@home_bp.route('/')
def index():
    """Renders the home page."""
    return render_template('index.html', message="Welcome to your Flask App!")
