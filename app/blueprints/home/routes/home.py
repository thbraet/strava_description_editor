from flask import render_template, session

from .. import home_bp


@home_bp.route('/')
def home():
    # Log the session ID and data
    print(f'Session ID: {session.sid if hasattr(session, "sid") else "No SID"}')

    print(f'Session Data: {dict(session)}')
    
    return render_template('index.html', name="<INSERT NAME>")
