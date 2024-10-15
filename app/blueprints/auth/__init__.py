import os
from flask import Blueprint


auth_bp = Blueprint('auth', __name__, template_folder='templates')

# Retrieve Strava client credentials from environment variables
client_secret = os.getenv("STRAVA_CLIENT_SECRET")
client_id = os.getenv("STRAVA_CLIENT_ID")

from .routes import callback, profile, strava