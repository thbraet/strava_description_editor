import os
import requests
from flask import Blueprint, request, jsonify
from .models import db, User

webhook_bp = Blueprint('webhook', __name__)

client_secret = os.getenv("STRAVA_CLIENT_SECRET")
client_id = os.getenv("STRAVA_CLIENT_ID")

@webhook_bp.route('/subscription', methods=['GET'])
def verify_subscription():
    print("Challenge")
    challenge = request.args.get('hub.challenge')
    return jsonify({'hub.challenge': challenge})

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

@webhook_bp.route('/subscription', methods=['POST'])
def handle_webhook():
    event_data = request.json

    if event_data['object_type'] != 'activity' or event_data['aspect_type'] != 'create':
        return jsonify({'status': 'ignored'}), 200

    owner_id = event_data['owner_id']
    user = User.query.filter_by(strava_id=owner_id).first()
    if not user:
        return jsonify({'status': 'ignored'}), 200

    activity_id = event_data['object_id']
    activity_data = get_activity_data(activity_id, user.access_token)
    if not activity_data:
        return jsonify({'status': 'error', 'message': 'Failed to retrieve activity data'}), 400

    calories = activity_data.get('calories', 0)
    if calories < 500:
        if update_activity_visibility(activity_id, user.access_token, True):
            return jsonify({'status': 'success', 'message': 'Activity hidden due to low calories'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Failed to update activity visibility'}), 400

    return jsonify({'status': 'ignored'}), 200

