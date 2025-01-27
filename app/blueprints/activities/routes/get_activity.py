from flask import jsonify

from ....models.strava.detailed_activity import get_activity_by_id

from ....blueprints.auth.functions.login_required import login_required
from ....blueprints.activities.functions.get_activity_data import get_activity_data
from .. import activities_bp


@activities_bp.route('/get_activity/<int:activity_id>')
@login_required(next_url='activities.get_activity')
def get_activity(activity_id):
    data = get_activity_by_id(activity_id)
    return jsonify(data)
