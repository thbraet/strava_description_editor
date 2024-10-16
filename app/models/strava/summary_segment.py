from ...extensions import db

class SummarySegment(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)  # Unique identifier of this segment
    name = db.Column(db.String(256), nullable=False)  # Name of this segment
    activity_type = db.Column(db.String(50), nullable=False)  # Type of activity (Ride or Run)
    distance = db.Column(db.Float, nullable=False)  # Segment's distance in meters
    average_grade = db.Column(db.Float, nullable=False)  # Segment's average grade in percentages
    maximum_grade = db.Column(db.Float, nullable=False)  # Segment's maximum grade in percentages
    elevation_high = db.Column(db.Float, nullable=False)  # Segment's highest elevation in meters
    elevation_low = db.Column(db.Float, nullable=False)  # Segment's lowest elevation in meters
    start_latlng = db.Column(db.ARRAY(db.Float), nullable=False)  # LatLng for start coordinates
    end_latlng = db.Column(db.ARRAY(db.Float), nullable=False)  # LatLng for end coordinates
    climb_category = db.Column(db.Integer, nullable=False)  # Category of the climb [0, 5]
    city = db.Column(db.String(100), nullable=True)  # Segment's city
    state = db.Column(db.String(100), nullable=True)  # Segment's state or geographical region
    country = db.Column(db.String(100), nullable=True)  # Segment's country
    private = db.Column(db.Boolean, nullable=False)  # Whether this segment is private

    athlete_pr_effort_id = db.Column(db.BigInteger, db.ForeignKey('summary_pr_segment_effort.id'))  # Foreign key to SummaryPRSegmentEffort
    athlete_segment_stats_id = db.Column(db.BigInteger, db.ForeignKey('summary_segment_effort.id'))  # Foreign key to SummarySegmentEffort

    athlete_pr_effort = db.relationship('SummaryPRSegmentEffort', backref='summary_segments')  # Relationship to SummaryPRSegmentEffort
    athlete_segment_stats = db.relationship('SummarySegmentEffort', backref='summary_segments_stats')  # Relationship to SummarySegmentEffort
