from flask import request, session, url_for

from ....blueprints.auth.functions.login_required import login_required
from ...auth.functions.make_strava_request import make_strava_request
from ...home import home_bp


@home_bp.route('/profile')
@login_required(next_url='home.profile')
def profile():
    """
    Fetch and display the user's Strava profile information.
    """

    response = make_strava_request('https://www.strava.com/api/v3/athlete')
    
    if response.status_code != 200:
        return response 
    
    # Parse the JSON response to get the user's profile data
    profile_data = response.json()
    
    # Return a greeting message with the user's first and last name
    return f"Hello, {profile_data['firstname']} {profile_data['lastname']}!"