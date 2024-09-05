

from flask import render_template
from . import home_bp


@home_bp.route('/')
def home():
    return render_template('index.html', name="<INSERT NAME>")

@home_bp.route('/about')
def about():
    return "This is the about page."


@home_bp.route('/user/<username>')
def show_user_profile(username):
    return f"User {username}"