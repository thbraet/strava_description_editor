from datetime import datetime
from ...extensions import db

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class UserTokens(db.Model):
    __tablename__ = 'user_tokens'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    athlete_id = Column(Integer, ForeignKey('detailed_athlete.id'))  # Foreign key to DetailedAthlete
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    # Relationship to DetailedAthlete
    athlete = relationship('DetailedAthlete', back_populates='tokens', uselist=False)
    
def create_user_tokens(data):  
    # Create UserTokens instance
    user_tokens = UserTokens(
        athlete_id=data['athlete']['id'],
        access_token=data.get('access_token'),
        refresh_token = data.get('refresh_token'),
        expires_at = datetime.fromtimestamp(data.get('expires_at'))
        
    )
    
    # Add the new user to the database session
    db.session.add(user_tokens)
    
    # Commit the transaction to save the changes to the database
    db.session.commit()
    
    return user_tokens

def update_user_tokens(user_tokens, data):
    # Update the tokens if they already exist
    user_tokens.access_token = data.get('access_token')
    user_tokens.refresh_token = data.get('refresh_token')
    user_tokens.expires_at = datetime.fromtimestamp(data.get('expires_at'))
    
    # Commit the changes to the database
    db.session.commit()
    
    return user_tokens
