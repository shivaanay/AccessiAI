import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'local-development-key-change-before-deployment')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///accessiai.db').replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_SCAN_SECONDS = int(os.environ.get('MAX_SCAN_SECONDS', '35'))
    JSON_SORT_KEYS = False
