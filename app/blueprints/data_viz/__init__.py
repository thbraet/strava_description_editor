import os
from flask import Blueprint
from ...models.models import StravaActivity, db, User


data_viz_bp = Blueprint('data_viz', __name__, template_folder='templates')

from . import routes