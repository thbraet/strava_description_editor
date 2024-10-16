from ...extensions import db

class Lap(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)  # Unique identifier of this lap
    activity_id = db.Column(db.BigInteger, db.ForeignKey('meta_activity.id'), nullable=False)  # Foreign key to MetaActivity
    athlete_id = db.Column(db.BigInteger, db.ForeignKey('meta_athlete.id'), nullable=False)  # Foreign key to MetaAthlete
    average_cadence = db.Column(db.Float, nullable=True)  # Lap's average cadence
    average_speed = db.Column(db.Float, nullable=True)  # Lap's average speed in meters per second
    distance = db.Column(db.Float, nullable=False)  # Lap's distance in meters
    elapsed_time = db.Column(db.Integer, nullable=False)  # Lap's elapsed time in seconds
    start_index = db.Column(db.Integer, nullable=False)  # Start index of this lap in the activity's stream
    end_index = db.Column(db.Integer, nullable=False)  # End index of this lap in the activity's stream
    lap_index = db.Column(db.Integer, nullable=False)  # Index of this lap in the activity
    max_speed = db.Column(db.Float, nullable=True)  # Maximum speed of this lap in meters per second
    moving_time = db.Column(db.Integer, nullable=False)  # Lap's moving time in seconds
    name = db.Column(db.String(256), nullable=True)  # Name of the lap
    pace_zone = db.Column(db.Integer, nullable=True)  # Athlete's pace zone during this lap
    split = db.Column(db.Integer, nullable=True)  # An integer instance for split
    start_date = db.Column(db.DateTime, nullable=False)  # Time at which the lap was started
    start_date_local = db.Column(db.DateTime, nullable=False)  # Local time at which the lap was started
    total_elevation_gain = db.Column(db.Float, nullable=True)  # Elevation gain of this lap in meters

    activity = db.relationship('MetaActivity', backref='laps')  # Relationship to MetaActivity
    athlete = db.relationship('MetaAthlete', backref='laps')  # Relationship to MetaAthlete
