from flask import session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strava_id = db.Column(db.Integer, unique=True, nullable=False)
    access_token = db.Column(db.String(128), nullable=False)
    refresh_token = db.Column(db.String(128), nullable=False)
    expires_at = db.Column(db.Integer, nullable=False)


class StravaActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.BigInteger, unique=True, nullable=True)
    athlete_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(256), nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    distance = db.Column(db.Float, nullable=True)
    moving_time = db.Column(db.Integer, nullable=True)
    total_elevation_gain = db.Column(db.Float, nullable=True)
    type = db.Column(db.String(50), nullable=True)
    sport_type = db.Column(db.String(50), nullable=True)
    average_speed = db.Column(db.Float, nullable=True)
    max_speed = db.Column(db.Float, nullable=True)
    
class FoodCalories(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.String)
    calories_per_serving_unit = db.Column(db.Integer)
    emoji = db.Column(db.String)
