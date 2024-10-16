from ...extensions import db

class PolylineMap(db.Model):
    id = db.Column(db.String, primary_key=True)  # Identifier of the map
    polyline = db.Column(db.String, nullable=True)  # Detailed polyline (only returned in detailed representations)
    summary_polyline = db.Column(db.String, nullable=True)  # Summary polyline of the map
