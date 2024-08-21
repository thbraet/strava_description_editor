import os
from flask import Blueprint, redirect, render_template, request, session, url_for
import requests
from app.models import StravaActivity, db, User


auth_bp = Blueprint('auth', __name__)

client_secret = os.getenv("STRAVA_CLIENT_SECRET")
client_id = os.getenv("STRAVA_CLIENT_ID")

@auth_bp.route('/strava')
def strava():
    authorization_url = (f"https://www.strava.com/oauth/authorize?client_id={client_id}"
                         f"&redirect_uri={url_for('auth.callback', _external=True)}"
                         "&response_type=code&scope=read_all,activity:read_all,activity:write,profile:read_all,profile:write")
    
    return render_template('strava.html', authorization_url=authorization_url)

@auth_bp.route('/callback')
def callback():

    code = request.args.get('code')

    if not code:
        return "Authorization failed."

    token_url = 'https://www.strava.com/oauth/token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code'
    }
    response = requests.post(token_url, data=payload)

    if response.status_code != 200:
        return "Failed to retrieve access token."

    response_data = response.json()
    strava_id = response_data['athlete']['id']
    if user := User.query.filter_by(strava_id=strava_id).first():
        user.access_token = response_data['access_token']
        user.refresh_token = response_data['refresh_token']
        user.expires_at = response_data['expires_at']

    else:
        user = User(
            strava_id=strava_id,
            access_token=response_data['access_token'],
            refresh_token=response_data['refresh_token'],
            expires_at=response_data['expires_at']
        )
        db.session.add(user)
    db.session.commit()
    session['strava_id'] = strava_id

    return redirect(url_for('main.profile'))