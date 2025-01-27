from typing import Optional, Tuple
from flask import redirect, session, url_for, Response, current_app as app

from ....models.strava.detailed_athlete import DetailedAthlete
from ....models.strava.user_tokens import UserTokens

def get_session_user():
    
    strava_id = session.get('athlete_id')
    user = DetailedAthlete.query.filter_by(id=strava_id).first()
    
    return user
    


