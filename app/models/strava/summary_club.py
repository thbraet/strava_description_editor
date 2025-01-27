from sqlalchemy import Column, Integer, String, Boolean, BigInteger
from ...extensions import db
from sqlalchemy.orm import relationship


class SummaryClub(db.Model):
    __tablename__ = 'summary_club'

    id = Column(BigInteger, primary_key=True)  # The club's unique identifier
    resource_state = Column(Integer, nullable=False)  # Resource state, level of detail (meta, summary, detail)
    name = Column(String(128), nullable=False)  # The club's name
    profile_medium = Column(String(256), nullable=True)  # URL to a 60x60 pixel profile picture
    cover_photo = Column(String(256), nullable=True)  # URL to a ~1185x580 pixel cover photo
    cover_photo_small = Column(String(256), nullable=True)  # URL to a ~360x176 pixel cover photo
    sport_type = Column(String(64), nullable=True)  # Deprecated, prefer activity_types (cycling, running, etc.)
    activity_types = Column(String(128), nullable=True)  # The activity types that count for a club
    city = Column(String(128), nullable=True)  # The club's city
    state = Column(String(128), nullable=True)  # The club's state or geographical region
    country = Column(String(64), nullable=True)  # The club's country
    private = Column(Boolean, default=False)  # Whether the club is private
    member_count = Column(Integer, nullable=True)  # The club's member count
    featured = Column(Boolean, default=False)  # Whether the club is featured or not
    verified = Column(Boolean, default=False)  # Whether the club is verified or not
    url = Column(String(256), nullable=True)  # The club's vanity URL

    # Relationships
    # athletes = relationship('DetailedAthlete', back_populates='clubs')  # Relationship to DetailedAthlete

