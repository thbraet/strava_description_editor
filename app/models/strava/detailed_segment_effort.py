from ...extensions import db

class DetailedSegmentEffort(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)  # Unique identifier of this effort
    activity_id = db.Column(db.BigInteger, db.ForeignKey('meta_activity.id'), nullable=False)  # Unique identifier of the related activity
    elapsed_time = db.Column(db.Integer, nullable=False)  # Effort's elapsed time in seconds
    start_date = db.Column(db.DateTime, nullable=False)  # Time at which the effort was started
    start_date_local = db.Column(db.DateTime, nullable=False)  # Local time at which the effort was started
    distance = db.Column(db.Float, nullable=False)  # Effort's distance in meters
    is_kom = db.Column(db.Boolean, nullable=False)  # Whether this effort is the current best on the leaderboard
    name = db.Column(db.String(256), nullable=False)  # Name of the segment on which this effort was performed

    activity_id = db.Column(db.BigInteger, db.ForeignKey('meta_activity.id'))  # Foreign key to MetaActivity
    athlete_id = db.Column(db.BigInteger, db.ForeignKey('meta_athlete.id'))  # Foreign key to MetaAthlete
    moving_time = db.Column(db.Integer, nullable=False)  # Effort's moving time in seconds
    start_index = db.Column(db.Integer, nullable=False)  # Start index of this effort in its activity's stream
    end_index = db.Column(db.Integer, nullable=False)  # End index of this effort in its activity's stream
    average_cadence = db.Column(db.Float, nullable=True)  # Effort's average cadence
    average_watts = db.Column(db.Float, nullable=True)  # Average wattage of this effort
    device_watts = db.Column(db.Boolean, nullable=False)  # Whether the wattage was reported by a dedicated device
    average_heartrate = db.Column(db.Float, nullable=True)  # Athlete's average heart rate during this effort
    max_heartrate = db.Column(db.Float, nullable=True)  # Athlete's maximum heart rate during this effort
    
    segment_id = db.Column(db.BigInteger, db.ForeignKey('summary_segment.id'))  # Foreign key to SummarySegment
    kom_rank = db.Column(db.Integer, nullable=True)  # Rank of the effort on the global leaderboard
    pr_rank = db.Column(db.Integer, nullable=True)  # Rank of the effort on the athlete's leaderboard
    hidden = db.Column(db.Boolean, nullable=False)  # Whether this effort should be hidden when viewed within an activity

    activity = db.relationship('MetaActivity', backref='detailed_segment_efforts')  # Relationship to MetaActivity
    athlete = db.relationship('MetaAthlete', backref='detailed_segment_efforts')  # Relationship to MetaAthlete
    segment = db.relationship('SummarySegment', backref='detailed_segment_efforts')  # Relationship to SummarySegment
