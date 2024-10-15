from flask import redirect, session, url_for
from ....models.models import User


def get_authenticated_user():
    """
    Retrieve the authenticated user from the session. Redirect to Strava authorization if not authenticated.
    """
    # Print the session for debugging purposes
    print(session)
    # Get the Strava ID from the session
    strava_id = session.get('strava_id')
    print(strava_id)
    
    # If Strava ID is not found in the session, redirect to the Strava authorization page
    if not strava_id:
        print("Redirect")
        return None, redirect(url_for('auth.strava'))
    
    # Query the database to find the user by Strava ID
    user = User.query.filter_by(strava_id=strava_id).first()
    
    # If user is not found in the database, redirect to the Strava authorization page
    if not user:
        return None, redirect(url_for('auth.strava'))
    
    # Return the user and None (indicating no redirect is needed)
    return user, None