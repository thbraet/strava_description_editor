from ...extensions import db

class PhotosSummary(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)  # Unique identifier
    source = db.Column(db.Integer, nullable=True)     # Source of the photo
    unique_id = db.Column(db.String, nullable=True)    # Unique identifier for the photo
    urls = db.Column(db.String, nullable=True)          # URLs of the photos
