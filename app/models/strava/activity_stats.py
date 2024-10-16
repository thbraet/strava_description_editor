from ...extensions import db

class ActivityStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    athlete_id = db.Column(db.Integer, nullable=False)  # Reference to the athlete

    biggest_ride_distance = db.Column(db.Float, nullable=True)  # Longest distance ridden (meters)
    biggest_climb_elevation_gain = db.Column(db.Float, nullable=True)  # Highest climb ridden (meters)

    # Recent totals (last 4 weeks)
    recent_ride_totals_id = db.Column(db.Integer, db.ForeignKey('activity_total.id'))
    recent_ride_totals = db.relationship('ActivityTotal', foreign_keys=[recent_ride_totals_id])

    recent_run_totals_id = db.Column(db.Integer, db.ForeignKey('activity_total.id'))
    recent_run_totals = db.relationship('ActivityTotal', foreign_keys=[recent_run_totals_id])

    recent_swim_totals_id = db.Column(db.Integer, db.ForeignKey('activity_total.id'))
    recent_swim_totals = db.relationship('ActivityTotal', foreign_keys=[recent_swim_totals_id])

    # Year to date (YTD) totals
    ytd_ride_totals_id = db.Column(db.Integer, db.ForeignKey('activity_total.id'))
    ytd_ride_totals = db.relationship('ActivityTotal', foreign_keys=[ytd_ride_totals_id])

    ytd_run_totals_id = db.Column(db.Integer, db.ForeignKey('activity_total.id'))
    ytd_run_totals = db.relationship('ActivityTotal', foreign_keys=[ytd_run_totals_id])

    ytd_swim_totals_id = db.Column(db.Integer, db.ForeignKey('activity_total.id'))
    ytd_swim_totals = db.relationship('ActivityTotal', foreign_keys=[ytd_swim_totals_id])

    # All time totals
    all_ride_totals_id = db.Column(db.Integer, db.ForeignKey('activity_total.id'))
    all_ride_totals = db.relationship('ActivityTotal', foreign_keys=[all_ride_totals_id])

    all_run_totals_id = db.Column(db.Integer, db.ForeignKey('activity_total.id'))
    all_run_totals = db.relationship('ActivityTotal', foreign_keys=[all_run_totals_id])

    all_swim_totals_id = db.Column(db.Integer, db.ForeignKey('activity_total.id'))
    all_swim_totals = db.relationship('ActivityTotal', foreign_keys=[all_swim_totals_id])