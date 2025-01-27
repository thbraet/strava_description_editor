from flask import redirect, render_template, request, session, url_for
from .. import auth_bp, client_id, client_secret


@auth_bp.route('/strava')
def strava():
    """
    This route renders a page with a button to authorize the app with Strava.
    Clicking the button redirects the user to Strava's authorization page.
    """
    next_url = request.args.get('next')
    
    authorization_url = (f"https://www.strava.com/oauth/authorize?client_id={client_id}"
                         f"&redirect_uri={url_for('auth.callback', _external=True)}"
                         f"&response_type=code&scope=read_all,activity:read_all,activity:write,profile:read_all,profile:write"
                         f"&state={next_url}")
    
    return redirect(authorization_url)
