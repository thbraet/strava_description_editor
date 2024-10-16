from ...extensions import db

class LatLng(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)  # Latitude coordinate
    longitude = db.Column(db.Float, nullable=False)  # Longitude coordinate
