from ....models.strava.detailed_athlete import DetailedAthlete
from ....models.strava.user_tokens import UserTokens
from flask import current_app as app


def get_access_token(athlete: DetailedAthlete) -> str:
    
    token_entry = UserTokens.query.filter_by(athlete_id=athlete.id).first()
    
    return token_entry.access_token
    
    