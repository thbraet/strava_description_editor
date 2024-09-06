from flask import redirect, render_template, request, session, url_for

import requests

from ...models.models import User
from ...extensions import db
from . import auth_bp, client_id, client_secret

@auth_bp.route('/strava')
def strava():
    """
    This route renders a page with a button to authorize the app with Strava.
    Clicking the button redirects the user to Strava's authorization page.
    """
    # Construct the URL for Strava's authorization endpoint
    authorization_url = (f"https://www.strava.com/oauth/authorize?client_id={client_id}"
                         f"&redirect_uri={url_for('auth.callback', _external=True)}"
                         "&response_type=code&scope=read_all,activity:read_all,activity:write,profile:read_all,profile:write")
    
    # Render the 'strava.html' template with the authorization URL
    return render_template('strava.html', authorization_url=authorization_url)

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
    
    # Store the Strava ID in the session for later use
    session['strava_id'] = strava_id

    # Redirect the user to the profile page
    return redirect(url_for('auth.profile'))

def get_authenticated_user():
    """
    Retrieve the authenticated user from the session. Redirect to Strava authorization if not authenticated.
    """
    # Print the session for debugging purposes
    print(session)
    # Get the Strava ID from the session
    strava_id = session.get('strava_id')
    print(strava_id)
    
    # If Strava ID is not found in the session, redirect to the Strava authorization page
    if not strava_id:
        print("Redirect")
        return None, redirect(url_for('auth.strava'))
    
    # Query the database to find the user by Strava ID
    user = User.query.filter_by(strava_id=strava_id).first()
    
    # If user is not found in the database, redirect to the Strava authorization page
    if not user:
        return None, redirect(url_for('auth.strava'))
    
    # Return the user and None (indicating no redirect is needed)
    return user, None

def make_strava_request(url, user, method='GET', data=None):
    """
    Make a request to the Strava API using the access token of the authenticated user.
    """
    # Set up the headers with the access token for authorization
    headers = {'Authorization': f'Bearer {user.access_token}'}
    
    # Make the request based on the specified HTTP method
    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'PUT':
        response = requests.put(url, headers=headers, data=data)
    
    # Return the response object
    return response



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