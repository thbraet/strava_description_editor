from flask import request, session, url_for

from ....blueprints.auth.functions.login_required import login_required
from ...auth.functions.make_strava_request import make_strava_request
from ...home import home_bp


@home_bp.route('/profile')
@login_required(next_url='home.profile')
def profile():
    """
    Fetch and display the user's Strava profile information.

    This route is protected by the login_required decorator, which ensures that
    only authenticated users can access it. It makes a request to the Strava API
    to fetch the authenticated user's profile information and displays a greeting
    message with the user's first and last name.

    Returns:
        str: A greeting message with the user's first and last name if the request
             is successful. Otherwise, returns the response object with the error status.
    """
    # Make a request to the Strava API to fetch the authenticated user's profile information
    response = make_strava_request('https://www.strava.com/api/v3/athlete')
    
    # Check if the request was successful
    if response.status_code != 200:
        # Return the response object with the error status
        return response 
    
    # Parse the JSON response to get the user's profile data
    profile_data = response.json()
    
    # Return a greeting message with the user's first and last name
    return f"Hello, {profile_data['firstname']} {profile_data['lastname']}!"