from flask import Blueprint


activities_bp = Blueprint('activities', __name__, template_folder='templates')


from app.blueprints.activities.routes.get_activity import get_activity
