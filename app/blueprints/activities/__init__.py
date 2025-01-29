from flask import Blueprint, jsonify, render_template, request

from app.blueprints.auth.functions import get_session_user
from app.blueprints.auth.functions.login_required import login_required
from app.blueprints.auth.functions.make_strava_request import make_strava_request
from app.models.strava.detailed_activity import get_activity_by_id
from app.models.strava.summary_activity import SummaryActivity, store_summary_activity


activities_bp = Blueprint('activities', __name__, template_folder='templates')

@activities_bp.route('/get_activity/<int:activity_id>')
@login_required(next_url='activities.get_activity')
def get_activity(activity_id):
    data = get_activity_by_id(activity_id)
    return jsonify(data)


@activities_bp.route('/store_activities', methods=['GET'])
@login_required(next_url='activities.store_activities')
def store_activities():
    """
    Fetches and stores activities from Strava into the local database.
    """
    # Retrieve the authenticated user; redirect to Strava authorization if not authenticated
    user = get_session_user()
    

    # Initialize pagination variables
    page = 1
    per_page = 100
    total_activities_fetched = 0
    
    while True:
        # Define parameters to fetch activities for the current page
        params = {'per_page': per_page, 'page': page}
        
        # Fetch activities from the Strava API
        response = make_strava_request('http://www.strava.com/api/v3/athlete/activities', method='GET', params=params)
        
        # Return an error message if the request to fetch activities fails
        if response.status_code != 200:
            return jsonify({'message': f'Failed to retrieve activities (page {page})'}), 500

        # Parse the activities data from the response
        activities_data = response.json()
        
        if not activities_data:
            break  # Break the loop if there are no more activities
        
        for activity_data in activities_data:
            # Check if the activity already exists in the database
            if SummaryActivity.query.filter_by(id=activity_data['id']).first():
                continue    
            
            store_summary_activity(activity_data)
            
            total_activities_fetched += 1

        # Move to the next page
        page += 1

    # Return a success message indicating activities were stored successfully
    return jsonify({'message': f'{total_activities_fetched} activities stored successfully'}), 200


@activities_bp.route('/update_activity', methods=['GET', 'POST'])
@login_required(next_url='activities.update_activity')
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
    user, redirect_response = get_session_user()
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