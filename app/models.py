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



    # trainer = db.Column(db.Boolean, nullable=True)
    # commute = db.Column(db.Boolean, nullable=True)
    # manual = db.Column(db.Boolean, nullable=True)
    # private = db.Column(db.Boolean, nullable=True)
    # flagged = db.Column(db.Boolean, nullable=True)
    # gear_id = db.Column(db.String(50), nullable=True)
    # average_cadence = db.Column(db.Float, nullable=True)
    # average_temp = db.Column(db.Float, nullable=True)
    # average_watts = db.Column(db.Float, nullable=True)
    # weighted_average_watts = db.Column(db.Float, nullable=True)
    # kilojoules = db.Column(db.Float, nullable=True)
    # device_watts = db.Column(db.Boolean, nullable=True)
    # has_heartrate = db.Column(db.Boolean, nullable=True)
    # max_watts = db.Column(db.Float, nullable=True)
    # elev_high = db.Column(db.Float, nullable=True)
    # elev_low = db.Column(db.Float, nullable=True)
    # pr_count = db.Column(db.Integer, nullable=True)
    # total_photo_count = db.Column(db.Integer, nullable=True)
    # has_kudoed = db.Column(db.Boolean, nullable=True)
    # workout_type = db.Column(db.Integer, nullable=True)
    # suffer_score = db.Column(db.Integer, nullable=True)
    # description = db.Column(db.Text, nullable=True)
    # calories = db.Column(db.Float, nullable=True)
    # hide_from_home = db.Column(db.Boolean, nullable=True)
    # device_name = db.Column(db.String(100), nullable=True)
    # segment_leaderboard_opt_out = db.Column(db.Boolean, nullable=True)
    # leaderboard_opt_out = db.Column(db.Boolean, nullable=True)
