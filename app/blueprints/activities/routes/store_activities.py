from flask import jsonify
from app.blueprints.auth.functions.get_session_user import get_session_user
from app.blueprints.auth.functions.login_required import login_required
from app.blueprints.auth.functions.make_strava_request import make_strava_request
from app.models.strava.summary_activity import SummaryActivity, store_summary_activity
from app.blueprints.activities import activities_bp


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

