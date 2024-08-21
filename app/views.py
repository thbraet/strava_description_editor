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



@main_bp.route('/profile')
def profile():
    print(session)
    strava_id = session.get('strava_id')
    if not strava_id:
        return redirect(url_for('auth.strava'))

    user = User.query.filter_by(strava_id=strava_id).first()
    if not user:
        return redirect(url_for('auth.strava'))

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
            return redirect(url_for('auth.strava'))

        user = User.query.filter_by(strava_id=strava_id).first()
        if not user:
            return redirect(url_for('auth.strava'))

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

@main_bp.route('/store_activities', methods=['GET'])
def store_activities():
    strava_id = session.get('strava_id')
    if not strava_id:
        return jsonify({'message': 'Strava ID not found in session'}), 401

    user = User.query.filter_by(strava_id=strava_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    headers = {'Authorization': f'Bearer {user.access_token}'}
    activities_url = 'https://www.strava.com/api/v3/athlete/activities'
    params = {'per_page': 100, 'page':2}  # Retrieve last 50 activities
    response = requests.get(activities_url, headers=headers, params=params)

    if response.status_code != 200:
        return jsonify({'message': 'Failed to retrieve activities'}), 500

    activities_data = response.json()

    for activity_data in activities_data:
        # Extract relevant information from activity data
        activity_id = activity_data['id']
        existing_activity = StravaActivity.query.filter_by(activity_id=activity_id).first()
        if existing_activity:
            continue  # Skip storing the activity if it already exists
       
        athlete_id = activity_data['athlete']['id']
        name = activity_data['name']
        start_date = datetime.strptime(activity_data['start_date'], '%Y-%m-%dT%H:%M:%SZ')
        distance = activity_data['distance']
        moving_time = activity_data['moving_time']
        total_elevation_gain = activity_data['total_elevation_gain']
        activity_type = activity_data['type']
        sport_type = activity_data['sport_type']
        average_speed = activity_data.get('average_speed', None)
        max_speed = activity_data.get('max_speed', None)

        # Create StravaActivity instance
        new_activity = StravaActivity(
            activity_id=activity_id,
            athlete_id=athlete_id,
            name=name,
            start_date=start_date,
            distance=distance,
            moving_time=moving_time,
            total_elevation_gain=total_elevation_gain,
            type=activity_type,
            sport_type=sport_type,
            average_speed=average_speed,
            max_speed=max_speed,
        )

        # Add instance to session and commit to save to database
        db.session.add(new_activity)

    db.session.commit()

    return jsonify({'message': 'Activities stored successfully'}), 200
