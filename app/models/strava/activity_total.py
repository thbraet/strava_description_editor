from ...extensions import db

class ActivityTotal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=True)  # Number of activities
    distance = db.Column(db.Float, nullable=True)  # Total distance in meters
    moving_time = db.Column(db.Integer, nullable=True)  # Total moving time in seconds
    elapsed_time = db.Column(db.Integer, nullable=True)  # Total elapsed time in seconds
    elevation_gain = db.Column(db.Float, nullable=True)  # Total elevation gain in meters
    achievement_count = db.Column(db.Integer, nullable=True)  # Total number of achievements
