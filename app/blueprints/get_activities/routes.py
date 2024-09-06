from datetime import datetime, timedelta
from flask import jsonify, render_template, request
import requests

from app.models.models import StravaActivity
from app.blueprints.auth.routes import get_authenticated_user, make_strava_request
from . import activities_bp
from ...extensions import db

def get_activity_data(activity_id, access_token):
    """
    Fetches data for a specific Strava activity using the activity ID and access token.
    """
    # Set up headers with the access token for authorization
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Construct the URL for the specific activity
    activity_url = f'https://www.strava.com/api/v3/activities/{activity_id}'
    
    # Send a GET request to Strava API to fetch the activity details
    response = requests.get(activity_url, headers=headers)
    
    # Return the activity data if the request was successful (status code 200)
    if response.status_code == 200:
        return response.json()
    
    # Return None if the request was not successful
    return None

def update_activity_visibility(activity_id, access_token, visibility):
    """
    Updates the visibility of a Strava activity (public/private) based on the provided visibility setting.
    """
    # Set up headers with the access token for authorization
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Construct the URL for the specific activity
    activity_url = f'https://www.strava.com/api/v3/activities/{activity_id}'
    
    # Prepare the payload with the visibility setting
    update_payload = {'private': visibility}
    
    # Send a PUT request to Strava API to update the activity's visibility
    response = requests.put(activity_url, headers=headers, json=update_payload)
    
    # Return True if the request was successful (status code 200), otherwise False
    return response.status_code == 200

@activities_bp.route('/update_activity', methods=['GET', 'POST'])
def update_activity():
    """
    Renders a form for updating an activity's description or handles form submission
    to update the description based on activity elevation gain.
    """
    # If the request method is not POST, render the form template
    if request.method != 'POST':
        return render_template('update_activity.html')
    
    # Extract the activity URL from the form data
    activity_url = request.form['activity_url']
    
    # Extract the activity ID from the URL
    activity_id = activity_url.split('/')[-1]

    # Retrieve the authenticated user; redirect to Strava authorization if not authenticated
    user, redirect_response = get_authenticated_user()
    if redirect_response:
        return redirect_response

    # Fetch the activity details using the Strava API
    response = make_strava_request(f'https://www.strava.com/api/v3/activities/{activity_id}', user)
    
    # Return an error message if the request to fetch activity details fails
    if response.status_code != 200:
        return "Failed to retrieve activity details."

    # Parse the activity data from the response
    activity_data = response.json()
    elevation_gain = activity_data['total_elevation_gain']

    # Prepare the payload with a new description based on the elevation gain
    update_payload = {
        'description': f"Congrats, you covered {elevation_gain} meters of elevation!"
    }
    
    # Send a PUT request to update the activity's description
    response = make_strava_request(f'https://www.strava.com/api/v3/activities/{activity_id}', user, method='PUT', data=update_payload)
    
    # Return an error message if the update request fails
    if response.status_code != 200:
        return "Failed to update activity description."

    # Return a success message if the description was updated successfully
    return "Activity description updated successfully!"


@activities_bp.route('/store_activities', methods=['GET'])
def store_activities():
    """
    Fetches and stores activities from Strava into the local database.
    """
    # Retrieve the authenticated user; redirect to Strava authorization if not authenticated
    user, redirect_response = get_authenticated_user()
    if redirect_response:
        return jsonify({'message': 'Strava ID not found in session'}), 401

    # Define parameters to fetch activities; can be adjusted for pagination
    params = {'per_page': 100, 'page': 2}
    
    # Fetch activities from the Strava API
    response = make_strava_request('https://www.strava.com/api/v3/athlete/activities', user, params=params)
    
    # Return an error message if the request to fetch activities fails
    if response.status_code != 200:
        return jsonify({'message': 'Failed to retrieve activities'}), 500

    # Parse the activities data from the response
    activities_data = response.json()
    
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

    # Commit the transaction to save the new activities in the database
    db.session.commit()
    
    # Return a success message indicating activities were stored successfully
    return jsonify({'message': 'Activities stored successfully'}), 200


