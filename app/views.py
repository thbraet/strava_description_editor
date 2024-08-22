from datetime import datetime
import os
import requests
from flask import Blueprint, jsonify, render_template, request, session, url_for, redirect
from .models import StravaActivity, db, User
from .auth import auth_bp

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


@main_bp.route('/profile')
def profile():
    user, redirect_response = get_authenticated_user()
    if redirect_response:
        return redirect_response

    response = make_strava_request('https://www.strava.com/api/v3/athlete', user)
    if response.status_code != 200:
        return "Failed to retrieve profile information."

    profile_data = response.json()
    return f"Hello, {profile_data['firstname']} {profile_data['lastname']}!"

@main_bp.route('/update_activity', methods=['GET', 'POST'])
def update_activity():
    if request.method != 'POST':
        return render_template('update_activity.html')
    activity_url = request.form['activity_url']
    activity_id = activity_url.split('/')[-1]

    user, redirect_response = get_authenticated_user()
    if redirect_response:
        return redirect_response

    response = make_strava_request(f'https://www.strava.com/api/v3/activities/{activity_id}', user)
    if response.status_code != 200:
        return "Failed to retrieve activity details."

    activity_data = response.json()
    elevation_gain = activity_data['total_elevation_gain']

    update_payload = {
        'description': f"Congrats, you covered {elevation_gain} meters of elevation!"
    }
    response = make_strava_request(f'https://www.strava.com/api/v3/activities/{activity_id}', user, method='PUT', data=update_payload)
    if response.status_code != 200:
        return "Failed to update activity description."

    return "Activity description updated successfully!"

@main_bp.route('/store_activities', methods=['GET'])
def store_activities():
    user, redirect_response = get_authenticated_user()
    if redirect_response:
        return jsonify({'message': 'Strava ID not found in session'}), 401

    params = {'per_page': 100, 'page': 2}
    response = make_strava_request('https://www.strava.com/api/v3/athlete/activities', user, params=params)
    if response.status_code != 200:
        return jsonify({'message': 'Failed to retrieve activities'}), 500

    activities_data = response.json()
    for activity_data in activities_data:
        if StravaActivity.query.filter_by(activity_id=activity_data['id']).first():
            continue

        new_activity = StravaActivity(
            activity_id=activity_data['id'],
            athlete_id=activity_data['athlete']['id'],
            name=activity_data['name'],
            start_date=datetime.strptime(activity_data['start_date'], '%Y-%m-%dT%H:%M:%SZ'),
            distance=activity_data['distance'],
            moving_time=activity_data['moving_time'],
            total_elevation_gain=activity_data['total_elevation_gain'],
            type=activity_data['type'],
            sport_type=activity_data['sport_type'],
            average_speed=activity_data.get('average_speed'),
            max_speed=activity_data.get('max_speed'),
        )
        db.session.add(new_activity)

    db.session.commit()
    return jsonify({'message': 'Activities stored successfully'}), 200
