from datetime import datetime
from typing import Optional, Dict, Any, Union

from flask import redirect, url_for, Response
from ...extensions import db

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger, Boolean, Float
from sqlalchemy.orm import relationship
from .summary_club import SummaryClub
# from .summary_gear import SummaryGear
# from .meta_athlete import MetaAthlete

class DetailedAthlete(db.Model):
    __tablename__ = 'detailed_athlete'
    
    id: int = Column(BigInteger, primary_key=True)  # Unique identifier of the athlete
    username: str = Column(String(128), nullable=False)  # Athlete's username
    resource_state: int = Column(Integer, nullable=False)  # Resource state, indicates level of detail
    firstname: str = Column(String(64), nullable=False)  # Athlete's first name
    lastname: str = Column(String(64), nullable=False)  # Athlete's last name
    bio: Optional[str] = Column(String(256), nullable=True)  # Athlete's biography
    profile_medium: Optional[str] = Column(String(256), nullable=True)  # URL to a 62x62 pixel profile picture
    profile: Optional[str] = Column(String(256), nullable=True)  # URL to a 124x124 pixel profile picture
    badge_type_id: int = Column(Integer, nullable=False)  # Badge type identifier
    city: Optional[str] = Column(String(128), nullable=True)  # Athlete's city
    state: Optional[str] = Column(String(128), nullable=True)  # Athlete's state or geographical region
    country: Optional[str] = Column(String(64), nullable=True)  # Athlete's country
    sex: Optional[str] = Column(String(1), nullable=True)  # Athlete's sex (M, F)
    premium: bool = Column(Boolean, default=False)  # Deprecated. Use summit field instead
    summit: bool = Column(Boolean, default=False)  # Whether the athlete has any Summit subscription
    created_at: datetime = Column(DateTime, nullable=False)  # Time at which the athlete was created
    updated_at: datetime = Column(DateTime, nullable=False)  # Time at which the athlete was last updated
    follower_count: Optional[int] = Column(Integer, nullable=True)  # Athlete's follower count
    friend_count: Optional[int] = Column(Integer, nullable=True)  # Athlete's friend count
    measurement_preference: Optional[str] = Column(String(16), nullable=True)  # Athlete's preferred unit system (feet, meters)
    ftp: Optional[int] = Column(Integer, nullable=True)  # Athlete's FTP (Functional Threshold Power)
    weight: Optional[float] = Column(Float, nullable=True)  # Athlete's weight
    
    # Add this to create a bidirectional relationship with UserTokens
    tokens = relationship('UserTokens', back_populates='athlete', uselist=False)
    activities = relationship('DetailedActivity', back_populates='athlete')
    

def get_detailed_athlete(athlete_id: int) -> Union[Optional[DetailedAthlete], Response]:
    # Query the database for the DetailedAthlete by their ID
    detailed_athlete = DetailedAthlete.query.filter_by(id=athlete_id).first()

    # If the athlete is found, return the instance
    if detailed_athlete:
        return detailed_athlete
    
    # If the athlete is not found, redirect to the Strava auth page
    return redirect(url_for('auth.strava'))


def create_detailed_athlete(data: Dict[str, Any]) -> DetailedAthlete:
    # Create DetailedAthlete instance
    detailed_athlete = DetailedAthlete(
        id=data['id'],
        username=data.get('username'),  # Use .get() to handle missing keys gracefully
        resource_state=data.get('resource_state', 0),
        firstname=data.get('firstname', ''),
        lastname=data.get('lastname', ''),
        bio=data.get('bio', ''),
        city=data.get('city', ''),
        state=data.get('state', ''),
        country=data.get('country', ''),
        sex=data.get('sex', ''),
        premium=data.get('premium', False),
        summit=data.get('summit', False),
        created_at=datetime.fromisoformat(data.get('created_at')[:-1]),  # Ensure this matches the correct data type in your model
        updated_at=datetime.fromisoformat(data.get('updated_at')[:-1]),  # Ensure this matches the correct data type in your model
        badge_type_id=data.get('badge_type_id', 0),
        weight=data.get('weight', 0.0),  # Assuming weight is a float
        profile_medium=data.get('profile_medium', ''),
        profile=data.get('profile', ''),
        # friend=data.get('friend'),
        # follower=data.get('follower')
    )
    # Add the new user to the database session
    db.session.add(detailed_athlete)
        
    # Commit the transaction to save the changes to the database
    db.session.commit()
    
    return detailed_athlete


def update_detailed_athlete(detailed_athlete: DetailedAthlete, athlete_data: Dict[str, Any]) -> DetailedAthlete:
    # Update fields if they exist in the provided data
    detailed_athlete.username = athlete_data.get('username', detailed_athlete.username)
    detailed_athlete.resource_state = athlete_data.get('resource_state', detailed_athlete.resource_state)
    detailed_athlete.firstname = athlete_data.get('firstname', detailed_athlete.firstname)
    detailed_athlete.lastname = athlete_data.get('lastname', detailed_athlete.lastname)
    detailed_athlete.bio = athlete_data.get('bio', detailed_athlete.bio)
    detailed_athlete.city = athlete_data.get('city', detailed_athlete.city)
    detailed_athlete.state = athlete_data.get('state', detailed_athlete.state)
    detailed_athlete.country = athlete_data.get('country', detailed_athlete.country)
    detailed_athlete.sex = athlete_data.get('sex', detailed_athlete.sex)
    detailed_athlete.premium = athlete_data.get('premium', detailed_athlete.premium)
    detailed_athlete.summit = athlete_data.get('summit', detailed_athlete.summit)
    detailed_athlete.created_at = datetime.fromisoformat(athlete_data['created_at'][:-1])
    detailed_athlete.updated_at = datetime.fromisoformat(athlete_data['updated_at'][:-1])  
    detailed_athlete.badge_type_id = athlete_data.get('badge_type_id', detailed_athlete.badge_type_id)
    detailed_athlete.weight = athlete_data.get('weight', detailed_athlete.weight)
    detailed_athlete.profile_medium = athlete_data.get('profile_medium', detailed_athlete.profile_medium)
    detailed_athlete.profile = athlete_data.get('profile', detailed_athlete.profile)
    
    # Commit the changes to the database
    db.session.commit()
    
    return detailed_athlete
