import requests

# from app.blueprints.auth.functions.get_authenticated_user import get_authenticated_user
from ...auth.functions.make_strava_request import make_strava_request

def get_activity_data(activity_id):
    """
    Fetches data for a specific Strava activity using the activity ID and access token.
    """
    response = make_strava_request(f'https://www.strava.com/api/v3/activities/{activity_id}')
    
    # Return the activity data if the request was successful (status code 200)
    if response.status_code == 200:
        return response.json()
    
    # Return None if the request was not successful
    return response

# get_activity_data(12670507732)