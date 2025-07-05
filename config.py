import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Set Flask configuration variables."""

    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_very_secret_key')
    
    # Project Paths
    BASE_DIR = basedir
    ROOT_DIR = os.path.dirname(basedir)

    # File Upload Settings
    UPLOAD_FOLDER = os.path.join(basedir, 'instance', 'uploads')
    ALLOWED_EXTENSIONS = {'csv','json'}

    # Redis configed variables
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0