from ...extensions import db

class DetailedAthlete(db.Model):
    __tablename__ = 'detailed_athlete'
    
    id = db.Column(db.BigInteger, primary_key=True)  # Unique identifier of the athlete
    resource_state = db.Column(db.Integer, nullable=False)  # Resource state, indicates level of detail
    firstname = db.Column(db.String(64), nullable=False)  # Athlete's first name
    lastname = db.Column(db.String(64), nullable=False)  # Athlete's last name
    profile_medium = db.Column(db.String(256), nullable=True)  # URL to a 62x62 pixel profile picture
    profile = db.Column(db.String(256), nullable=True)  # URL to a 124x124 pixel profile picture
    city = db.Column(db.String(128), nullable=True)  # Athlete's city
    state = db.Column(db.String(128), nullable=True)  # Athlete's state or geographical region
    country = db.Column(db.String(64), nullable=True)  # Athlete's country
    sex = db.Column(db.String(1), nullable=True)  # Athlete's sex (M, F)
    premium = db.Column(db.Boolean, default=False)  # Deprecated. Use summit field instead
    summit = db.Column(db.Boolean, default=False)  # Whether the athlete has any Summit subscription
    created_at = db.Column(db.DateTime, nullable=False)  # Time at which the athlete was created
    updated_at = db.Column(db.DateTime, nullable=False)  # Time at which the athlete was last updated
    follower_count = db.Column(db.Integer, nullable=True)  # Athlete's follower count
    friend_count = db.Column(db.Integer, nullable=True)  # Athlete's friend count
    measurement_preference = db.Column(db.String(16), nullable=True)  # Athlete's preferred unit system (feet, meters)
    ftp = db.Column(db.Integer, nullable=True)  # Athlete's FTP (Functional Threshold Power)
    weight = db.Column(db.Float, nullable=True)  # Athlete's weight
    clubs_id = db.Column(db.BigInteger, db.ForeignKey('summary_club.id'), nullable=True)  # Foreign key to SummaryClub
    bikes_id = db.Column(db.BigInteger, db.ForeignKey('summary_gear.id'), nullable=True)  # Foreign key to SummaryGear for bikes
    shoes_id = db.Column(db.BigInteger, db.ForeignKey('summary_gear.id'), nullable=True)  # Foreign key to SummaryGear for shoes
    
    # Relationships
    clubs = db.relationship('SummaryClub', backref='athletes')  # Relationship to SummaryClub
    bikes = db.relationship('SummaryGear', backref='biker_athletes', foreign_keys=[bikes_id])  # Relationship to SummaryGear for bikes
    shoes = db.relationship('SummaryGear', backref='shoes_athletes', foreign_keys=[shoes_id])  # Relationship to SummaryGear for shoes
