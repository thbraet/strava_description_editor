from flask import render_template, url_for
from .. import auth_bp, client_id, client_secret


@auth_bp.route('/strava')
def strava():
    """
    This route renders a page with a button to authorize the app with Strava.
    Clicking the button redirects the user to Strava's authorization page.
    """
    # Construct the URL for Strava's authorization endpoint
    print( client_id)
    
    authorization_url = (f"https://www.strava.com/oauth/authorize?client_id={client_id}"
                         f"&redirect_uri={url_for('auth.callback', _external=True)}"
                         "&response_type=code&scope=read_all,activity:read_all,activity:write,profile:read_all,profile:write")
    
    # Render the 'strava.html' template with the authorization URL
    return render_template('strava.html', authorization_url=authorization_url)