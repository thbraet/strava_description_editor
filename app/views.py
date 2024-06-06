import os
import requests
from flask import Blueprint, render_template, request, session, url_for, redirect
from .models import db, User

main_bp = Blueprint('main', __name__)

client_secret = os.getenv("STRAVA_CLIENT_SECRET")
client_id = os.getenv("STRAVA_CLIENT_ID")

@main_bp.route('/')
def home():
    return render_template('index.html', name="Thibauld")

@main_bp.route('/about')
def about():
    return "This is the about page."

@main_bp.route('/user/<username>')
def show_user_profile(username):
    return f"User {username}"

@main_bp.route('/strava')
def strava():
    print(url_for('main.callback', _external=True))
    authorization_url = (f"https://www.strava.com/oauth/authorize?client_id={client_id}"
                         f"&redirect_uri={url_for('main.callback', _external=True)}"
                         "&response_type=code&scope=read_all,activity:read_all,activity:write,profile:read_all,profile:write")
    
    print(authorization_url)
    return render_template('strava.html', authorization_url=authorization_url)

@main_bp.route('/callback')
def callback():
    print(request.args)
    
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
    user = User.query.filter_by(strava_id=strava_id).first()
    
    if not user:
        user = User(
            strava_id=strava_id,
            access_token=response_data['access_token'],
            refresh_token=response_data['refresh_token'],
            expires_at=response_data['expires_at']
        )
        db.session.add(user)
    else:
        user.access_token = response_data['access_token']
        user.refresh_token = response_data['refresh_token']
        user.expires_at = response_data['expires_at']
    
    db.session.commit()
    session['strava_id'] = strava_id

    return redirect(url_for('main.profile'))

@main_bp.route('/profile')
def profile():
    strava_id = session.get('strava_id')
    if not strava_id:
        return redirect(url_for('main.strava'))

    user = User.query.filter_by(strava_id=strava_id).first()
    if not user:
        return redirect(url_for('main.strava'))

    headers = {'Authorization': f'Bearer {user.access_token}'}
    profile_url = 'https://www.strava.com/api/v3/athlete'
    response = requests.get(profile_url, headers=headers)
    
    if response.status_code != 200:
        return "Failed to retrieve profile information."

    profile_data = response.json()
    return f"Hello, {profile_data['firstname']} {profile_data['lastname']}!"

@main_bp.route('/update_activity', methods=['GET', 'POST'])
def update_activity():
    if request.method == 'POST':
        activity_url = request.form['activity_url']
        activity_id = activity_url.split('/')[-1]

        strava_id = session.get('strava_id')
        if not strava_id:
            return redirect(url_for('main.strava'))

        user = User.query.filter_by(strava_id=strava_id).first()
        if not user:
            return redirect(url_for('main.strava'))

        headers = {'Authorization': f'Bearer {user.access_token}'}
        activity_url = f'https://www.strava.com/api/v3/activities/{activity_id}'
        response = requests.get(activity_url, headers=headers)

        if response.status_code != 200:
            return "Failed to retrieve activity details."

        activity_data = response.json()
        elevation_gain = activity_data['total_elevation_gain']

        update_url = f'https://www.strava.com/api/v3/activities/{activity_id}'
        update_payload = {
            'description': f"Congrats, you covered {elevation_gain} meters of elevation!"
        }
        response = requests.put(update_url, headers=headers, data=update_payload)

        if response.status_code != 200:
            return "Failed to update activity description."

        return "Activity description updated successfully!"
    return render_template('update_activity.html')
