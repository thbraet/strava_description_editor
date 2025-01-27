from flask import Blueprint, render_template


activities_bp = Blueprint('activities', __name__, template_folder='templates')

from .routes import store_activities, update_activity, get_activity