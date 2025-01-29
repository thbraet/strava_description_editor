import os
from flask import Blueprint, redirect, request, session, url_for
import requests

from app.models.strava.detailed_athlete import DetailedAthlete, create_detailed_athlete, update_detailed_athlete
from app.models.strava.user_tokens import UserTokens, create_user_tokens, update_user_tokens


auth_bp = Blueprint('auth', __name__, template_folder='templates')

# Retrieve Strava client credentials from environment variables
client_secret = os.getenv("STRAVA_CLIENT_SECRET")
client_id = os.getenv("STRAVA_CLIENT_ID")


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
    
    next_url = request.args.get('state')
    
    def exchange_code_for_access_token(code):
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

        # Parse the JSON response to get access token and user details
        response_data = response.json()
        
        return response_data
    
    response_data = exchange_code_for_access_token(code)  

    # Store the Strava ID in the session for later use
    athlete_id = response_data.get('athlete').get('id')
    session['athlete_id'] = athlete_id

    # Check if the athlete already exists in the database by their Strava ID
    detailed_athlete = DetailedAthlete.query.filter_by(id=athlete_id).first()
    
    if detailed_athlete:
        detailed_athlete = update_detailed_athlete(detailed_athlete, response_data.get('athlete'))
    
    else:
        detailed_athlete  = create_detailed_athlete(response_data.get('athlete'))
        
    
    # Check if the user's tokens already exist
    user_tokens = UserTokens.query.filter_by(athlete_id=athlete_id).first()
    
    if user_tokens:
        user_tokens = update_user_tokens(user_tokens, response_data)
    else:
        user_tokens = create_user_tokens(response_data)
    
    # return redirect(url_for('home.profile'))
    return redirect(next_url)
    
 
@auth_bp.route('/strava')
def strava():
    """
    This route renders a page with a button to authorize the app with Strava.
    Clicking the button redirects the user to Strava's authorization page.
    """
    next_url = request.args.get('next')
    
    authorization_url = (f"https://www.strava.com/oauth/authorize?client_id={client_id}"
                         f"&redirect_uri={url_for('auth.callback', _external=True)}"
                         f"&response_type=code&scope=read_all,activity:read_all,activity:write,profile:read_all,profile:write"
                         f"&state={next_url}")
    
    return redirect(authorization_url)
