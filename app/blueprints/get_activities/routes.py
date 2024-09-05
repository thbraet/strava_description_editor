from datetime import datetime
from flask import jsonify, render_template, request
import requests

from app.blueprints.auth.models import StravaActivity
from app.blueprints.auth.routes import get_authenticated_user, make_strava_request
from . import activities_bp
from ...extensions import db

def get_activity_data(activity_id, access_token):    
    headers = {'Authorization': f'Bearer {access_token}'}
    activity_url = f'https://www.strava.com/api/v3/activities/{activity_id}'
    response = requests.get(activity_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def update_activity_visibility(activity_id, access_token, visibility):
    headers = {'Authorization': f'Bearer {access_token}'}
    activity_url = f'https://www.strava.com/api/v3/activities/{activity_id}'
    update_payload = {'private': visibility}
    response = requests.put(activity_url, headers=headers, json=update_payload)
    return response.status_code == 200

@activities_bp.route('/update_activity', methods=['GET', 'POST'])
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

@activities_bp.route('/store_activities', methods=['GET'])
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