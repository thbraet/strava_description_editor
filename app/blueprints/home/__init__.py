from flask import Blueprint, render_template


home_bp = Blueprint('home', __name__, template_folder='templates')

from .routes import about, home, user