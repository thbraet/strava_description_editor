
from flask import jsonify, request

from .. import webhook_bp
from ....models.models import User
from ...activities.functions import get_activity_data, update_activity_visibility

@webhook_bp.route('/subscription', methods=['GET'])
def verify_subscription():
    print("Challenge")
    challenge = request.args.get('hub.challenge')
    return jsonify({'hub.challenge': challenge})


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
