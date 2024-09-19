import os
from flask import Blueprint
from ...models.models import StravaActivity, db, User


charts_bp = Blueprint('charts', __name__, template_folder='templates')

from . import routes