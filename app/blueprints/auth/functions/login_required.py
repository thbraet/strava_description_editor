from functools import wraps
from flask import g, request, redirect, session, url_for

def login_required(next_url=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            strava_id = session.get('athlete_id')
            if strava_id is None:
                next_endpoint = url_for(next_url)
                return redirect(url_for('auth.strava', next=next_endpoint or request.url))
            return f(*args, **kwargs)
        return decorated_function
    return decorator