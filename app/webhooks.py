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

@webhook_bp.route('/subscription', methods=['POST'])
def handle_webhook():
    event_data = request.json

    if event_data['object_type'] == 'activity' and event_data['aspect_type'] == 'create':
        owner_id = event_data['owner_id']
        if user := User.query.filter_by(strava_id=owner_id).first():
            activity_id = event_data['object_id']
            headers = {'Authorization': f'Bearer {user.access_token}'}
            activity_url = f'https://www.strava.com/api/v3/activities/{activity_id}'
            response = requests.get(activity_url, headers=headers)

            if response.status_code == 200:
                activity_data = response.json()
                calories = activity_data.get('calories', 0)

                if calories < 500:
                    update_payload = {'private': True}
                    response = requests.put(activity_url, headers=headers, json=update_payload)

                    if response.status_code == 200:
                        return jsonify({'status': 'success', 'message': 'Activity hidden due to low calories'}), 200
                    else:
                        return jsonify({'status': 'error', 'message': 'Failed to update activity visibility'}), 400
    return jsonify({'status': 'ignored'}), 200
