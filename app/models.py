from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strava_id = db.Column(db.Integer, unique=True, nullable=False)
    access_token = db.Column(db.String(128), nullable=False)
    refresh_token = db.Column(db.String(128), nullable=False)
    expires_at = db.Column(db.Integer, nullable=False)
