from datetime import datetime
from flask import Response
from sqlalchemy.types import Enum as SQLAEnum


from ...blueprints.auth.functions import make_strava_request
from ...extensions import db
from typing import Union, Optional
# from .meta_athlete import MetaAthlete
# from .sport_type import SportType
# from .polyline_map import PolylineMap
# from .photos_summary import PhotosSummary   
# from .summary_gear import SummaryGear
# from .detailed_segment_effort import DetailedSegmentEffort
# # from .split import Split
# from .lap import Lap
# from .detailed_segment_effort import DetailedSegmentEffort


class DetailedActivity(db.Model):
    __tablename__ = 'detailed_activity'
    
    id = db.Column(db.BigInteger, primary_key=True)  # Unique identifier of the activity
    external_id = db.Column(db.String(256), nullable=True)  # Identifier provided at upload time
    upload_id = db.Column(db.BigInteger, nullable=False)  # Identifier of the upload that resulted in this activity
    name = db.Column(db.String(256), nullable=True)  # Name of the activity
    distance = db.Column(db.Float, nullable=False)  # Activity's distance in meters
    moving_time = db.Column(db.Integer, nullable=False)  # Activity's moving time in seconds
    elapsed_time = db.Column(db.Integer, nullable=False)  # Activity's elapsed time in seconds
    total_elevation_gain = db.Column(db.Float, nullable=True)  # Activity's total elevation gain
    elev_high = db.Column(db.Float, nullable=True)  # Activity's highest elevation in meters
    elev_low = db.Column(db.Float, nullable=True)  # Activity's lowest elevation in meters
    type = db.Column(db.String(256), nullable=True)  # Deprecated: Prefer to use sport_type
    start_date = db.Column(db.DateTime, nullable=False)  # Time at which the activity was started
    start_date_local = db.Column(db.DateTime, nullable=False)  # Local time at which the activity was started
    sport_type = db.Column(db.String(256), nullable=True)  # Type of sport (e.g. ride, run, swim)
    timezone = db.Column(db.String(64), nullable=True)  # Timezone of the activity
    # start_latlng = db.Column(db.ARRAY(db.Float), nullable=True)  # Latitude/Longitude coordinates as array
    # end_latlng = db.Column(db.ARRAY(db.Float), nullable=True)  # Latitude/Longitude coordinates as array
    achievement_count = db.Column(db.Integer, nullable=True)  # Number of achievements gained during this activity
    kudos_count = db.Column(db.Integer, nullable=True)  # Number of kudos given for this activity
    comment_count = db.Column(db.Integer, nullable=True)  # Number of comments for this activity
    athlete_count = db.Column(db.Integer, nullable=True)  # Number of athletes participating in a group activity
    photo_count = db.Column(db.Integer, nullable=True)  # Number of Instagram photos for this activity
    total_photo_count = db.Column(db.Integer, nullable=True)  # Total Instagram and Strava photos for this activity
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
    
    athlete_id = db.Column(db.BigInteger, db.ForeignKey('detailed_athlete.id'), nullable=False)  # Foreign key to DetailedAthlete
    athlete = db.relationship('DetailedAthlete', back_populates='activities')  # Relationship to MetaAthlete



def get_activity_by_id(activity_id: int) -> Optional[Union[dict, Response]]:
    
    #Check if activity already in db
    db_activity = DetailedActivity.query.filter_by(id=activity_id).first()
    
    # If not, fetch the activity from Strava
    if not db_activity:
        response = make_strava_request(f'https://www.strava.com/api/v3/activities/{activity_id}')
    
        # Return the activity data if the request was successful (status code 200)
        if response.status_code == 200:
            return response.json()
        
        # Return None if the request was not successful
        return response
    
    return db_activity


# def store_activity(activity_data):
#     # Create a new StravaActivity instance with the fetched data

#             # Add the new activity to the database session
#     db.session.add(new_activity)
#     db.session.commit()

