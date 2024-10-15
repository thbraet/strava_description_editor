import requests


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