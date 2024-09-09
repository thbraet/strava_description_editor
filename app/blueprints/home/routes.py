

from flask import render_template, session
from . import home_bp


@home_bp.route('/')
def home():
        # Log the session ID and data
    print(f'Session ID: {session.sid if hasattr(session, "sid") else "No SID"}')

    print(f'Session Data: {dict(session)}')
    
    return render_template('index.html', name="<INSERT NAME>")

@home_bp.route('/about')
def about():
    return "This is the about page."


@home_bp.route('/user/<username>')
def show_user_profile(username):
    return f"User {username}"