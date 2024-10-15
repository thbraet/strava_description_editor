import requests


def make_strava_request(url, user, method='GET', data=None, params=None):
    """
    Make a request to the Strava API using the access token of the authenticated user.
    """
    # Set up the headers with the access token for authorization
    headers = {'Authorization': f'Bearer {user.access_token}'}
    
    # Make the request based on the specified HTTP method
    if method == 'GET':
        response = requests.get(url, headers=headers, params=params)
    elif method == 'PUT':
        response = requests.put(url, headers=headers, data=data)
    
    # Return the response object
    return response