from datetime import datetime
from flask import jsonify

from ...auth.functions.get_authenticated_user import get_authenticated_user
from ...auth.functions.make_strava_request import make_strava_request
from ....models.models import StravaActivity, db

from .. import activities_bp

@activities_bp.route('/store_activities', methods=['GET'])
def store_activities():
    """
    Fetches and stores activities from Strava into the local database.
    """
    # Retrieve the authenticated user; redirect to Strava authorization if not authenticated
    user, redirect_response = get_authenticated_user()
    if redirect_response:
        return jsonify({'message': 'Strava ID not found in session'}), 401

    # Initialize pagination variables
    page = 1
    per_page = 100
    total_activities_fetched = 0
    
    while True:
        # Define parameters to fetch activities for the current page
        params = {'per_page': per_page, 'page': page}
        
        # Fetch activities from the Strava API
        response = make_strava_request('https://www.strava.com/api/v3/athlete/activities', user, params=params)
        
        # Return an error message if the request to fetch activities fails
        if response.status_code != 200:
            return jsonify({'message': f'Failed to retrieve activities (page {page})'}), 500

        # Parse the activities data from the response
        activities_data = response.json()
        
        if not activities_data:
            break  # Break the loop if there are no more activities
        
        for activity_data in activities_data:
            # Check if the activity already exists in the database
            if StravaActivity.query.filter_by(activity_id=activity_data['id']).first():
                continue

            # Create a new StravaActivity instance with the fetched data
            new_activity = StravaActivity(
                activity_id=activity_data['id'],
                athlete_id=activity_data['athlete']['id'],
                name=activity_data['name'],
                start_date=datetime.strptime(activity_data['start_date'], '%Y-%m-%dT%H:%M:%SZ'),
                distance=activity_data['distance'],
                moving_time=activity_data['moving_time'],
                total_elevation_gain=activity_data['total_elevation_gain'],
                type=activity_data['type'],
                sport_type=activity_data['sport_type'],
                average_speed=activity_data.get('average_speed'),
                max_speed=activity_data.get('max_speed'),
            )

            # Add the new activity to the database session
            db.session.add(new_activity)
            total_activities_fetched += 1
        
        # Commit the transaction to save the new activities in the database
        db.session.commit()

        # Move to the next page
        page += 1

    # Return a success message indicating activities were stored successfully
    return jsonify({'message': f'{total_activities_fetched} activities stored successfully'}), 200