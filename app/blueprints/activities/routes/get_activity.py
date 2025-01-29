from flask import jsonify
from app.blueprints.auth.functions.login_required import login_required
from app.models.strava.detailed_activity import get_activity_by_id
from app.blueprints.activities import activities_bp


@activities_bp.route('/get_activity/<int:activity_id>')
@login_required(next_url='activities.get_activity')
def get_activity(activity_id):
    data = get_activity_by_id(activity_id)
    return jsonify(data)