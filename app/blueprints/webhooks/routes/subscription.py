
from flask import jsonify, request

from .. import webhook_bp
from ....models.models import User
from ...activities.functions.get_activity_data import get_activity_data
from ...activities.functions.update_activity_visibility import update_activity_visibility
from ..functions.check_visibility import check_visibility

@webhook_bp.route('/subscription', methods=['GET'])
def verify_subscription():
    print("Challenge")
    challenge = request.args.get('hub.challenge')
    return jsonify({'hub.challenge': challenge})


@webhook_bp.route('/subscription', methods=['POST'])
def handle_webhook():
    print("Webhook triggered")
    event_data = request.json
    owner_id = event_data['owner_id']
    activity_id = event_data['object_id']

    if event_data['object_type'] != 'activity':
        return jsonify({'status': 'ignored'}), 200

    user = User.query.filter_by(strava_id=owner_id).first()
    if not user:
        return jsonify({'status': 'ignored'}), 200

    activity_data = get_activity_data(activity_id, user.access_token)
    if not activity_data:
        return jsonify({'status': 'error', 'message': 'Failed to retrieve activity data'}), 400
    
    
    if check_visibility(activity_data):
        if update_activity_visibility(activity_id, user.access_token, True):
            print("Updated activity visibility")
            return jsonify({'status': 'success', 'message': 'Activity hidden due to low calories'}), 200
        else:
            print("Failed to update activity visibility")
            return jsonify({'status': 'error', 'message': 'Failed to update activity visibility'}), 400

    return jsonify({'status': 'ignored'}), 200
