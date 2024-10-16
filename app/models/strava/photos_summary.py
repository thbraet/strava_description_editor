from ...extensions import db

class PhotosSummary(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)  # Unique identifier
    count = db.Column(db.Integer, nullable=False)     # Number of photos
    primary_id = db.Column(db.BigInteger, db.ForeignKey('photos_summary_primary.id'))  # Foreign key to PhotosSummary_primary
    primary = db.relationship('PhotosSummary_primary', backref='photos_summary')  # Relationship to PhotosSummary_primary
