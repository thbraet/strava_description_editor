import requests


def update_activity_visibility(activity_id, access_token, visibility):
    """
    Updates the visibility of a Strava activity (public/private) based on the provided visibility setting.
    """
    # Set up headers with the access token for authorization
    headers = {
        'Authorization': f'Bearer {access_token}',
        "Content-Type": "application/json"
    }
    
    # Construct the URL for the specific activity
    activity_url = f'https://www.strava.com/api/v3/activities/{activity_id}'
    
    # Prepare the payload with the visibility setting
    update_payload = {"hide_from_home": visibility}
    
    # Send a PUT request to Strava API to update the activity's visibility
    response = requests.put(activity_url, headers=headers, json=update_payload)
    
    # Return True if the request was successful (status code 200), otherwise False
    return response.status_code == 200
