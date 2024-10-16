from ...extensions import db

class DetailedActivity(db.Model):
    __tablename__ = 'detailed_activity'
    
    id = db.Column(db.BigInteger, primary_key=True)  # Unique identifier of the activity
    external_id = db.Column(db.String(256), nullable=True)  # Identifier provided at upload time
    upload_id = db.Column(db.BigInteger, nullable=False)  # Identifier of the upload that resulted in this activity
    athlete_id = db.Column(db.BigInteger, db.ForeignKey('meta_athlete.id'), nullable=False)  # Foreign key to MetaAthlete
    name = db.Column(db.String(256), nullable=True)  # Name of the activity
    distance = db.Column(db.Float, nullable=False)  # Activity's distance in meters
    moving_time = db.Column(db.Integer, nullable=False)  # Activity's moving time in seconds
    elapsed_time = db.Column(db.Integer, nullable=False)  # Activity's elapsed time in seconds
    total_elevation_gain = db.Column(db.Float, nullable=True)  # Activity's total elevation gain
    elev_high = db.Column(db.Float, nullable=True)  # Activity's highest elevation in meters
    elev_low = db.Column(db.Float, nullable=True)  # Activity's lowest elevation in meters
    type = db.Column(db.String(256), nullable=True)  # Deprecated: Prefer to use sport_type
    sport_type_id = db.Column(db.String(256), db.ForeignKey('sport_type.id'), nullable=False)  # Foreign key to SportType
    start_date = db.Column(db.DateTime, nullable=False)  # Time at which the activity was started
    start_date_local = db.Column(db.DateTime, nullable=False)  # Local time at which the activity was started
    timezone = db.Column(db.String(64), nullable=True)  # Timezone of the activity
    start_latlng = db.Column(db.ARRAY(db.Float), nullable=True)  # Latitude/Longitude coordinates as array
    end_latlng = db.Column(db.ARRAY(db.Float), nullable=True)  # Latitude/Longitude coordinates as array
    achievement_count = db.Column(db.Integer, nullable=True)  # Number of achievements gained during this activity
    kudos_count = db.Column(db.Integer, nullable=True)  # Number of kudos given for this activity
    comment_count = db.Column(db.Integer, nullable=True)  # Number of comments for this activity
    athlete_count = db.Column(db.Integer, nullable=True)  # Number of athletes participating in a group activity
    photo_count = db.Column(db.Integer, nullable=True)  # Number of Instagram photos for this activity
    total_photo_count = db.Column(db.Integer, nullable=True)  # Total Instagram and Strava photos for this activity
    map_id = db.Column(db.String(256), db.ForeignKey('polyline_map.id'), nullable=True)  # Foreign key to PolylineMap
    trainer = db.Column(db.Boolean, default=False)  # Whether recorded on a training machine
    commute = db.Column(db.Boolean, default=False)  # Whether this activity is a commute
    manual = db.Column(db.Boolean, default=False)  # Whether this activity was created manually
    private = db.Column(db.Boolean, default=False)  # Whether this activity is private
    flagged = db.Column(db.Boolean, default=False)  # Whether this activity is flagged
    workout_type = db.Column(db.Integer, nullable=True)  # Activity's workout type
    upload_id_str = db.Column(db.String(256), nullable=True)  # Unique identifier of the upload in string format
    average_speed = db.Column(db.Float, nullable=True)  # Activity's average speed in meters per second
    max_speed = db.Column(db.Float, nullable=True)  # Activity's max speed in meters per second
    has_kudoed = db.Column(db.Boolean, default=False)  # Whether the logged-in athlete has kudoed this activity
    hide_from_home = db.Column(db.Boolean, default=False)  # Whether the activity is muted
    gear_id = db.Column(db.String(256), nullable=True)  # Gear ID for the activity
    kilojoules = db.Column(db.Float, nullable=True)  # Total work done in kilojoules during this activity (for rides only)
    average_watts = db.Column(db.Float, nullable=True)  # Average power output in watts (for rides only)
    device_watts = db.Column(db.Boolean, default=False)  # Whether watts are from a power meter
    max_watts = db.Column(db.Integer, nullable=True)  # Max watts for rides with power meter data only
    weighted_average_watts = db.Column(db.Integer, nullable=True)  # Normalized Power for rides with power meter data only
    description = db.Column(db.Text, nullable=True)  # Description of the activity
    photos_id = db.Column(db.BigInteger, db.ForeignKey('photos_summary.id'), nullable=True)  # Foreign key to PhotosSummary
    gear_id = db.Column(db.BigInteger, db.ForeignKey('summary_gear.id'), nullable=True)  # Foreign key to SummaryGear
    calories = db.Column(db.Float, nullable=True)  # Kilocalories consumed during this activity
    # Relationships
    athlete = db.relationship('MetaAthlete', backref='activities')  # Relationship to MetaAthlete
    sport_type = db.relationship('SportType', backref='activities')  # Relationship to SportType
    map = db.relationship('PolylineMap', backref='activities')  # Relationship to PolylineMap
    photos = db.relationship('PhotosSummary', backref='activities')  # Relationship to PhotosSummary
    gear = db.relationship('SummaryGear', backref='activities')  # Relationship to SummaryGear
    segment_efforts = db.relationship('DetailedSegmentEffort', backref='activity', lazy='dynamic')  # Relationship to DetailedSegmentEffort
    splits_metric = db.relationship('Split', backref='metric_activity', foreign_keys='Split.metric_activity_id', lazy='dynamic')  # Relationship to splits in metric units
    splits_standard = db.relationship('Split', backref='standard_activity', foreign_keys='Split.standard_activity_id', lazy='dynamic')  # Relationship to splits in imperial units
    laps = db.relationship('Lap', backref='activity')  # Relationship to Lap objects
    best_efforts = db.relationship('DetailedSegmentEffort', backref='best_activity', lazy='dynamic')  # Collection of best efforts
