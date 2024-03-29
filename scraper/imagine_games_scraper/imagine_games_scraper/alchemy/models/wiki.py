import json
import uuid
from imagine_games_scraper.alchemy.config import Base

from sqlalchemy import Column, String, ForeignKey, Enum, Integer, ARRAY, JSON, TIMESTAMP, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator, VARCHAR, UserDefinedType

class WikiObject(Base):
    __tablename__ = 'wiki_objects'

    def __init__(self):
        self.id = uuid.uuid4()

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    legacy_id = Column(UUID(as_uuid=True))
    name = Column(String)

class WikiNavigation(Base):
    __tablename__ = 'wiki_navigations'

    def __init__(self):
        self.id = uuid.uuid4()

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    wiki_object_id = Column(
        UUID(as_uuid=True),
        ForeignKey("wiki_objects.id"),
        nullable=False
    )
    label = Column(String)
    url = Column(String)

    wiki_object = relationship("WikiObject", foreign_keys=[wiki_object_id])

class MapObject(Base):
    __tablename__ = 'map_objects'

    def __init__(self):
        self.id = uuid.uuid4()

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    legacy_id = Column(UUID(as_uuid=True))
    wiki_object_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("wiki_objects.id"),
        nullable=True
    )

    wiki_object = relationship("WikiObject", foreign_keys=[wiki_object_id])

class Map(Base):
    __tablename__ = 'maps'

    def __init__(self):
        self.id = uuid.uuid4()

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    legacy_id = Column(UUID(as_uuid=True))
    map_object_id = Column(
        UUID(as_uuid=True),
        ForeignKey("map_objects.id"),
        nullable=False
    )
    name = Column(String)
    slug = Column(String)
    cover_id = Column(
        UUID(as_uuid=True),
        ForeignKey("images.id")
    )
    width = Column(Integer)
    height = Column(Integer)
    map_type = Column(String)
    initial_zoom = Column(Integer)
    min_zoom = Column(Integer)
    max_zoom = Column(Integer)
    initial_latitude = Column(DECIMAL)
    initial_longitude = Column(DECIMAL)
    marker_count = Column(Integer)
    map_genie_game_id = Column(Integer)
    tile_sets = Column(ARRAY(String))
    background_color = Column(String)

    map_object = relationship("MapObject", foreign_keys=[map_object_id])
    cover = relationship("Image", foreign_keys=[cover_id])