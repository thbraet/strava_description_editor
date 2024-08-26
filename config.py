import os
from datetime import timedelta
import redis

class Config:
    SECRET_KEY = os.urandom(23)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///strava_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = os.path.join(os.getcwd(), 'flask_sessions')
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
