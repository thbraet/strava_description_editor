from ...extensions import db

class SummaryGear(db.Model):
    id = db.Column(db.String, primary_key=True)      # Unique identifier for the gear
    resource_state = db.Column(db.Integer, nullable=True)  # Resource state (summary or detail)
    primary = db.Column(db.Boolean, nullable=False)    # Whether this gear is the owner's default one
    name = db.Column(db.String, nullable=False)         # Name of the gear
    distance = db.Column(db.Float, nullable=True)       # Distance logged with this gear
