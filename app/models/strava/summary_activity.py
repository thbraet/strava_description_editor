from datetime import datetime
from ...extensions import db

class SummaryActivity(db.Model):
    __tablename__ = 'summary_activity'  # Change this to your preferred table name

    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String)
    upload_id = db.Column(db.Integer)
    athlete_id = db.Column(db.Integer)
    # athlete_id = db.Column(db.Integer, db.ForeignKey('meta_athlete.id'))  # Assuming MetaAthlete has id as primary key
    name = db.Column(db.String)
    distance = db.Column(db.Float)
    moving_time = db.Column(db.Integer)
    elapsed_time = db.Column(db.Integer)
    total_elevation_gain = db.Column(db.Float)
    elev_high = db.Column(db.Float)
    elev_low = db.Column(db.Float)
    sport_type = db.Column(db.String)
    # sport_type_id = db.Column(db.Integer, db.ForeignKey('sport_type.id'))  # Assuming SportType has id as primary key
    start_date = db.Column(db.DateTime)
    start_date_local = db.Column(db.DateTime)
    timezone = db.Column(db.String)
    start_latlng_id = db.Column(db.Integer)
    end_latlng_id = db.Column(db.Integer)
    # start_latlng_id = db.Column(db.Integer, db.ForeignKey('lat_lng.id'))  # Assuming LatLng has id as primary key
    # end_latlng_id = db.Column(db.Integer, db.ForeignKey('lat_lng.id'))  # Assuming LatLng has id as primary key
    achievement_count = db.Column(db.Integer)
    kudos_count = db.Column(db.Integer)
    comment_count = db.Column(db.Integer)
    athlete_count = db.Column(db.Integer)
    photo_count = db.Column(db.Integer)
    total_photo_count = db.Column(db.Integer)
    map_id = db.Column(db.Integer)
    # map_id = db.Column(db.Integer, db.ForeignKey('polyline_map.id'))  # Assuming PolylineMap has id as primary key
    trainer = db.Column(db.Boolean)
    commute = db.Column(db.Boolean)
    manual = db.Column(db.Boolean)
    private = db.Column(db.Boolean)
    flagged = db.Column(db.Boolean)
    workout_type = db.Column(db.Integer)
    upload_id_str = db.Column(db.String)
    average_speed = db.Column(db.Float)
    max_speed = db.Column(db.Float)
    has_kudoed = db.Column(db.Boolean)
    hide_from_home = db.Column(db.Boolean)
    gear_id = db.Column(db.String)
    kilojoules = db.Column(db.Float)
    average_watts = db.Column(db.Float)
    device_watts = db.Column(db.Boolean)
    max_watts = db.Column(db.Integer)
    weighted_average_watts = db.Column(db.Integer)
    
    
def store_summary_activity(activity_data):
    # Create a new DetailedActivity instance with the fetched data
    new_activity = SummaryActivity(
        id=activity_data['id'],
        athlete_id=activity_data['athlete']['id'],
        name=activity_data['name'],
        start_date=datetime.strptime(activity_data['start_date'], '%Y-%m-%dT%H:%M:%SZ'),
        start_date_local=datetime.strptime(activity_data['start_date_local'], '%Y-%m-%dT%H:%M:%SZ'),
        distance=activity_data['distance'],
        moving_time=activity_data['moving_time'],
        elapsed_time=activity_data['elapsed_time'],
        total_elevation_gain=activity_data['total_elevation_gain'],
        elev_high=activity_data.get('elev_high'),
        elev_low=activity_data.get('elev_low'),
        type=activity_data['type'],
        sport_type=activity_data['sport_type'],
        workout_type=activity_data.get('workout_type'),
        average_speed=activity_data.get('average_speed'),
        max_speed=activity_data.get('max_speed'),
        average_cadence=activity_data.get('average_cadence'),
        average_temp=activity_data.get('average_temp'),
        has_heartrate=activity_data.get('has_heartrate', False),
        average_heartrate=activity_data.get('average_heartrate'),
        max_heartrate=activity_data.get('max_heartrate'),
        kudos_count=activity_data.get('kudos_count'),
        comment_count=activity_data.get('comment_count'),
        achievement_count=activity_data.get('achievement_count'),
        athlete_count=activity_data.get('athlete_count'),
        photo_count=activity_data.get('photo_count'),
        total_photo_count=activity_data.get('total_photo_count'),
        trainer=activity_data.get('trainer', False),
        commute=activity_data.get('commute', False),
        manual=activity_data.get('manual', False),
        private=activity_data.get('private', False),
        visibility=activity_data.get('visibility'),
        flagged=activity_data.get('flagged', False),
        gear_id=activity_data.get('gear_id'),
        upload_id=activity_data['upload_id'],
        upload_id_str=activity_data['upload_id_str'],
        external_id=activity_data.get('external_id'),
        has_kudoed=activity_data.get('has_kudoed', False),
        hide_from_home=activity_data.get('hide_from_home', False),
        map_id=activity_data['map']['id'],  # Assuming you have a map_id column
        summary_polyline=activity_data['map']['summary_polyline'],  # Assuming you have a summary_polyline column
        start_latlng=activity_data.get('start_latlng'),  # Ensure you have a start_latlng column
        end_latlng=activity_data.get('end_latlng'),  # Ensure you have a end_latlng column
    )

    # Add the new activity to the database session
    db.session.add(new_activity)
    db.session.commit()