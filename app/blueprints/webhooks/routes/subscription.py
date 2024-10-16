from flask import jsonify, request
import logging

from .. import webhook_bp
from ....models.models import User
from ...activities.functions.get_activity_data import get_activity_data
from ...activities.functions.update_activity_visibility import update_activity_visibility
from ..functions.check_visibility import check_visibility

logger = logging.getLogger(__name__)

@webhook_bp.route('/subscription', methods=['GET'])
def verify_subscription() -> jsonify:
    """Verify subscription challenge."""
    challenge = request.args.get('hub.challenge')
    logger.info("Challenge verified: %s", challenge)
    return jsonify({'hub.challenge': challenge})


@webhook_bp.route('/subscription', methods=['POST'])
def handle_webhook() -> jsonify:
    """Handle incoming webhook notifications."""
    logger.info("Webhook triggered")
    
    event_data = request.json
    owner_id = event_data.get('owner_id')
    activity_id = event_data.get('object_id')

    if event_data.get('object_type') != 'activity':
        logger.info("Ignored event: not an activity")
        return jsonify({'status': 'ignored'}), 200

    user = User.query.filter_by(strava_id=owner_id).first()
    if not user:
        logger.info("Ignored event: user not found")
        return jsonify({'status': 'ignored'}), 200

    activity_data = get_activity_data(activity_id, user.access_token)
    if not activity_data:
        logger.error("Failed to retrieve activity data for activity ID: %s", activity_id)
        return jsonify({'status': 'error', 'message': 'Failed to retrieve activity data'}), 400
    
    if check_visibility(activity_data):
        if update_activity_visibility(activity_id, user.access_token, True):
            logger.info("Updated activity visibility for activity ID: %s", activity_id)
            return jsonify({'status': 'success', 'message': 'Activity hidden'}), 200
        else:
            logger.error("Failed to update activity visibility for activity ID: %s", activity_id)
            return jsonify({'status': 'error', 'message': 'Failed to update activity visibility'}), 400

    logger.info("Ignored event: visibility check failed")
    return jsonify({'status': 'ignored'}), 200
