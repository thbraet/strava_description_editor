import os
from flask import Blueprint, redirect, render_template, request, session, url_for
import requests
from app.models import StravaActivity, db, User


auth_bp = Blueprint('auth', __name__)

# Retrieve Strava client credentials from environment variables
client_secret = os.getenv("STRAVA_CLIENT_SECRET")
client_id = os.getenv("STRAVA_CLIENT_ID")

@auth_bp.route('/strava')
def strava():
    """Redirects you to a page with just one button "Authorize with Strava"
    When you click this button, you will got to the authorization_url which will bring you to the callback function in this file.
    """
    authorization_url = (f"https://www.strava.com/oauth/authorize?client_id={client_id}"
                         f"&redirect_uri={url_for('auth.callback', _external=True)}"
                         "&response_type=code&scope=read_all,activity:read_all,activity:write,profile:read_all,profile:write")
    
    return render_template('strava.html', authorization_url=authorization_url)

@auth_bp.route('/callback')
def callback():

    # Get the authorization code from the request arguments
    code = request.args.get('code')

    # Check if the authorization code is missing
    if not code:
        return "Authorization failed."

    # URL to request an access token from Strava
    token_url = 'https://www.strava.com/oauth/token'
    
    # Payload for the token request, including client credentials and the authorization code
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code'
    }
    
    # Send a POST request to Strava to exchange the authorization code for an access token
    response = requests.post(token_url, data=payload)

    # Check if the request was successful
    if response.status_code != 200:
        return "Failed to retrieve access token."

    # Parse the JSON response to get the access token and other details
    response_data = response.json()
    strava_id = response_data['athlete']['id']
    
    # Check if the user already exists in the database based on their Strava ID
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
    
    # Store the Strava ID in the session
    session['strava_id'] = strava_id

    # Redirect the user to the profile page
    return redirect(url_for('main.profile'))