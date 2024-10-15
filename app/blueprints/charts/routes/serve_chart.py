from flask import send_from_directory
from .. import charts_bp

@charts_bp.route('/charts/<path:filename>')
def serve_chart(filename):
    # Serve files from the specified directory
    return send_from_directory('/home/thbraet/strava_description_editor/app/blueprints/charts/charts/', filename)

  