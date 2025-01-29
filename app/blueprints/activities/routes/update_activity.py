

from flask import render_template, request
from app.blueprints.auth.functions.get_session_user import get_session_user
from app.blueprints.auth.functions.login_required import login_required
from app.blueprints.auth.functions.make_strava_request import make_strava_request
from app.blueprints.activities import activities_bp

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