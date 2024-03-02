import json
import uuid
from imagine_games_scraper.alchemy.config import Base

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

    def __init__(self):
        self.id = uuid.uuid4()

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

    how_long_to_beat = relationship("HowLongToBeat", foreign_keys=[how_long_to_beat_id])
    cover = relationship("Image", foreign_keys=[cover_id])
    gallery = relationship("Gallery", foreign_keys=[gallery_id])

class ObjectAttributeConnection(Base):
    __tablename__ = 'object_attribute_connections'

    def __init__(self):
        self.id = uuid.uuid4()

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

    object = relationship("Object", foreign_keys=[object_id])
    attribute = relationship("TypedAttribute", foreign_keys=[attribute_id])

class HowLongToBeat(Base):
    __tablename__ = 'how_long_to_beat'

    def __init__(self):
        self.id = uuid.uuid4()

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    legacy_id = Column(Integer)
    legacy_ign_object_id = Column(UUID(as_uuid=True))
    steam_id = Column(Integer)
    itch_id = Column(String)
    platforms = Column(String)
    list = Column(JSON),
    review = Column(JSON),
    time = Column(JSON)

class AgeRating(Base):
    __tablename__ = 'age_ratings'

    def __init__(self):
        self.id = uuid.uuid4()

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

    def __init__(self):
        self.id = uuid.uuid4()

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    legacy_id = Column(
        UUID(as_uuid=True)
    )
    object_id = Column(
        UUID(as_uuid=True),
        ForeignKey("objects.id"),
        nullable=False
    )
    name = Column(String),
    region = Column(String),
    age_rating_id = Column(
        UUID(as_uuid=True),
        ForeignKey("age_ratings.id"),
        nullable=True
    )

    object = relationship("Object", foreign_keys=[object_id])
    age_rating = relationship("AgeRating", foreign_keys=[age_rating_id])

class Release(Base):
    __tablename__ = 'releases'

    def __init__(self):
        self.id = uuid.uuid4()

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    legacy_id = Column(UUID(as_uuid=True))
    date = Column(TIMESTAMP)
    estimated_date = Column(TIMESTAMP)
    time_frame_year = Column(TIMESTAMP)

class AgeRatingDescriptor(Base):
    __tablename__ = 'age_rating_descriptors'

    def __init__(self):
        self.id = uuid.uuid4()

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    region_id = Column(
        UUID(as_uuid=True),
        ForeignKey("regions.id"),
        nullable=False
    )
    attribute_id = Column(
        UUID(as_uuid=True),
        ForeignKey("attributes.id"),
        nullable=False
    )

    region = relationship("Region", foreign_keys=[region_id])
    attribute = relationship("Attribute", foreign_keys=[attribute_id])

class AgeRatingInteractiveElement(Base):
    __tablename__ = 'age_rating_interactive_elements'

    def __init__(self):
        self.id = uuid.uuid4()

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    region_id = Column(
        UUID(as_uuid=True),
        ForeignKey("regions.id"),
        nullable=False
    )
    attribute_id = Column(
        UUID(as_uuid=True),
        ForeignKey("attributes.id"),
        nullable=False
    )

    region = relationship("Region", foreign_keys=[region_id])
    attribute = relationship("Attribute", foreign_keys=[attribute_id])

class ReleasePlatformAttribute(Base):
    __tablename__ = 'release_platform_attributes'

    def __init__(self):
        self.id = uuid.uuid4()

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

    release = relationship("Release", foreign_keys=[release_id])
    attribute = relationship("Attribute", foreign_keys=[attribute_id])