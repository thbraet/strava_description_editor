
from flask import  redirect, request, session, url_for
import requests

from ....models.models import User
from ....extensions import db


from .. import auth_bp, client_id, client_secret


@auth_bp.route('/callback')
def callback():
    """
    This route handles the callback from Strava after user authorization.
    It exchanges the authorization code for an access token and stores user information.
    """
    # Get the authorization code from the request arguments
    code = request.args.get('code')

    # If no code is provided, return an authorization failure message
    if not code:
        return "Authorization failed."

    # URL to request an access token from Strava
    token_url = 'https://www.strava.com/oauth/token'
    
    # Prepare the payload for the token request with client credentials and authorization code
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code'
    }
    
    # Send a POST request to Strava to exchange the authorization code for an access token
    response = requests.post(token_url, data=payload)

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        return "Failed to retrieve access token."

    # Parse the JSON response to get access token and user details
    response_data = response.json()
    strava_id = response_data['athlete']['id']
    
    # Check if the user already exists in the database by their Strava ID
    if user := User.query.filter_by(strava_id=strava_id).first():
        # Update the existing user's access token, refresh token, and expiration time
        user.access_token = response_data['access_token']
        user.refresh_token = response_data['refresh_token']
        user.expires_at = response_data['expires_at']

    else:
        # Create a new user record if the user does not exist
        user = User(
            strava_id=strava_id,
            access_token=response_data['access_token'],
            refresh_token=response_data['refresh_token'],
            expires_at=response_data['expires_at']
        )
        # Add the new user to the database session
        db.session.add(user)
        
    # Commit the transaction to save the changes to the database
    db.session.commit()
    
    
    # Log the session ID and data
    print(f'Session ID: {session.sid if hasattr(session, "sid") else "No SID"}')
    
    print(f'Session Data: {dict(session)}')
    
    # logging.debug(f'Session ID: {session.sid if hasattr(session, "sid") else "No SID"}')
    # logging.debug(f'Session Data: {dict(session)}')


    # Store the Strava ID in the session for later use
    session['strava_id'] = strava_id
    
    # Redirect the user to the profile page
    return redirect(url_for('auth.profile'))
