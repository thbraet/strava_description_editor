from ...extensions import db

class SummaryPRSegmentEffort(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)  # Unique identifier for the PR segment effort
    pr_activity_id = db.Column(db.BigInteger, nullable=False)  # Unique identifier of the activity related to the PR effort
    pr_elapsed_time = db.Column(db.Integer, nullable=False)  # Elapsed time of the PR effort
    pr_date = db.Column(db.DateTime, nullable=False)  # Time at which the PR effort was started
    effort_count = db.Column(db.Integer, nullable=False)  # Number of efforts by the authenticated athlete on this segment
