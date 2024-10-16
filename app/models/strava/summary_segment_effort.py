from ...extensions import db

class SummarySegmentEffort(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)  # Unique identifier for this segment effort
    activity_id = db.Column(db.BigInteger, nullable=False)  # Unique identifier of the activity related to this effort
    elapsed_time = db.Column(db.Integer, nullable=False)  # Effort's elapsed time in seconds
    start_date = db.Column(db.DateTime, nullable=False)  # Time at which the effort was started
    start_date_local = db.Column(db.DateTime, nullable=False)  # Start time in local timezone
    distance = db.Column(db.Float, nullable=False)  # Effort's distance in meters
    is_kom = db.Column(db.Boolean, nullable=False)  # Whether this effort is the current best on the leaderboard
