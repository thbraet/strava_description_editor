from flask import Blueprint, render_template


streak_bp = Blueprint('streak', __name__, template_folder='templates')

from .routes import longest_streak