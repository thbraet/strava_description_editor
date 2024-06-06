import os

class Config:
    SECRET_KEY = os.urandom(23)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///strava_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
