from ..functions.make_strava_request import make_strava_request
from .. import auth_bp
from ..functions.get_authenticated_user import get_authenticated_user

@auth_bp.route('/profile')
def profile():
    """
    Fetch and display the user's Strava profile information.
    """
    # Retrieve the authenticated user, or redirect to the Strava authorization page if not authenticated
    user, redirect_response = get_authenticated_user()
    if redirect_response:
        return redirect_response

    # Make a request to Strava API to get the user's profile information
    response = make_strava_request('https://www.strava.com/api/v3/athlete', user)
    
    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        return "Failed to retrieve profile information."

    # Parse the JSON response to get the user's profile data
    profile_data = response.json()
    
    # Return a greeting message with the user's first and last name
    return f"Hello, {profile_data['firstname']} {profile_data['lastname']}!"