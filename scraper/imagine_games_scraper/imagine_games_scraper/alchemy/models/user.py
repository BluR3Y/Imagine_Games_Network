import json
import uuid
from imagine_games_scraper.alchemy.config import Base

from sqlalchemy import Column, String, ForeignKey, Enum, Integer, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.types import UserDefinedType, TypeDecorator

class User(Base):
    __tablename__ = 'users'

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    legacy_id = Column(
        UUID(as_uuid=True)
    )
    avatar_id = Column(
        UUID(as_uuid=True), 
        ForeignKey('images.id') # Foreign key referencing the images table
    )
    name = Column(String)
    nickname = Column(String)

    avatar = relationship("Image", foreign_keys=[avatar_id]) # Define the relationship
    
class SocialMediaType(UserDefinedType):
    cache_ok = True

    def get_col_spec(self):
        return "social_media_entry"
    
class SocialMediaEntry(TypeDecorator):
    impl = SocialMediaType

    def process_bind_param(self, value, dialect):
        return (value.get('platform'),value.get('username'))
    
class Author(Base):
    __tablename__ = 'authors'

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    legacy_id = Column(Integer)
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey('users.id')
    )
    url = Column(String)
    cover_id = Column(
        UUID(as_uuid=True), 
        ForeignKey('images.id')
    )
    position = Column(String)
    bio = Column(String)
    location = Column(String)
    socials = Column(ARRAY(SocialMediaEntry), default=[])

    user = relationship("User", foreign_keys=[user_id])
    cover = relationship("Image", foreign_keys=[cover_id])

class UserConfiguration(Base):
    __tablename__ = 'user_configurations'

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id')
    )
    privacy = Column(
        Enum('private', 'public', name="privacy_types", create_type=False), # must be one of two possible values
        nullable=False # Field can't be null
    )

    user = relationship("User", foreign_keys=[user_id])