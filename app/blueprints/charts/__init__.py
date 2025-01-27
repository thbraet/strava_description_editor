import os
from flask import Blueprint


charts_bp = Blueprint('charts', __name__, template_folder='templates')

from .routes import serve_chart, calendar