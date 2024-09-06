from flask import redirect, render_template, request, session, url_for

import requests

from ...models.models import User
from ...extensions import db
from . import auth_bp, client_id, client_secret

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
    return redirect(url_for('auth.profile'))

def get_authenticated_user():
    print(session)
    strava_id = session.get('strava_id')
    print(strava_id)
    if not strava_id:
        print("Redirect")
        return None, redirect(url_for('auth.strava'))
    user = User.query.filter_by(strava_id=strava_id).first()
    if not user:
        return None, redirect(url_for('auth.strava'))
    return user, None

def make_strava_request(url, user, method='GET', data=None):
    headers = {'Authorization': f'Bearer {user.access_token}'}
    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'PUT':
        response = requests.put(url, headers=headers, data=data)
    return response


@auth_bp.route('/profile')
def profile():
    user, redirect_response = get_authenticated_user()
    if redirect_response:
        return redirect_response

    response = make_strava_request('https://www.strava.com/api/v3/athlete', user)
    if response.status_code != 200:
        return "Failed to retrieve profile information."

    profile_data = response.json()
    return f"Hello, {profile_data['firstname']} {profile_data['lastname']}!"