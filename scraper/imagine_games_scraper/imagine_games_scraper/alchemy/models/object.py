import json
import uuid
from config import Base

from sqlalchemy import Column, String, ForeignKey, Enum, Integer, ARRAY, JSON, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator, VARCHAR, UserDefinedType

class NameType(UserDefinedType):
    cache_ok = True

    def get_col_spec(self):
        return "name_entry"
    
class NameEntry(TypeDecorator):
    impl = NameType

    def process_bind_param(self, value, dialect):
        return (value.get('main'),value.get('alt'),value.get('short'))
    
class DescriptionType(UserDefinedType):
    cache_ok = True

    def get_col_spec(self):
        return "description_entry"
    
class DescriptionEntry(TypeDecorator):
    impl = DescriptionType

    def process_bind_param(self, value, dialect):
        return (value.get('long'),value.get('short'))

class Object(Base):
    __tablename__ = 'objects'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    legacy_id = Column(
        UUID(as_uuid=True)
    )
    url = Column(
        String
    )
    slug = Column(
        String
    )
    wiki_slug = Column(
        String
    )
    how_long_to_beat_id = Column(
        UUID(as_uuid=True),
        ForeignKey("how_long_to_beat.id")
    )
    type = Column(
        String
    )
    cover_id = Column(
        UUID(as_uuid=True),
        ForeignKey("images.id")
    )
    gallery_id = Column(
        UUID(as_uuid=True),
        ForeignKey("galleries.id")
    )
    names = Column(NameEntry)
    descriptions = Column(DescriptionEntry)

    how_long_to_beat = relationship("HowLongToBeat")
    cover = relationship("Image")
    gallery = relationship("Gallery")

class ObjectAttributeConnection(Base):
    __tablename__ = 'object_attribute_connections'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    object_id = Column(
        UUID(as_uuid=True),
        ForeignKey("objects.id"),
        nullable=False
    )
    attribute_id = Column(
        UUID(as_uuid=True),
        ForeignKey("typed_attributes.id"),
        nullable=False
    )

    object = relationship("Object")
    attribute = relationship("TypedAttribute")

class HowLongToBeat(Base):
    __tablename__ = 'how_long_to_beat'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    legacy_ign_object_id = Column(UUID(as_uuid=True))
    steam_id = Column(Integer)
    itch_id = Column(String)
    platforms = Column(String)
    list = Column(JSON),
    review = Column(JSON),
    time = Column(JSON)

class AgeRating(Base):
    __tablename__ = 'age_ratings'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    legacy_id = Column(
        UUID(as_uuid=True)
    )
    type = Column(String),
    name = Column(String),
    slug = Column(String)

class Region(Base):
    __tablename__ = 'regions'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    legacy_id = Column(
        UUID(as_uuid=True)
    )
    name = Column(String),
    region = Column(String),
    age_rating_id = Column(
        UUID(as_uuid=True),
        ForeignKey("age_ratings.id"),
        nullable=True
    )

    age_rating = relationship("AgeRating")

class Release(Base):
    __tablename__ = 'releases'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    legacy_id = Column(UUID(as_uuid=True))
    date = Column(TIMESTAMP)
    estimated_date = Column(TIMESTAMP)
    time_frame_year = Column(TIMESTAMP)

class ReleasePlatformAttribute(Base):
    __tablename__ = 'release_platform_attributes'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    release_id = Column(
        UUID(as_uuid=True),
        ForeignKey("releases.id"),
        nullable=False
    )
    attribute_id = Column(
        UUID(as_uuid=True),
        ForeignKey("attributes.id"),
        nullable=False
    )

    release = relationship("Release")
    attribute = relationship("Attribute")