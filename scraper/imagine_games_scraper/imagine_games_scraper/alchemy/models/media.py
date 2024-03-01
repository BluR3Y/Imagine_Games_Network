import json
import uuid
from imagine_games_scraper.alchemy.config import Base

from sqlalchemy import Column, String, ForeignKey, Enum, Integer, ARRAY, TIMESTAMP, BOOLEAN, NUMERIC
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator, VARCHAR

class Gallery(Base):
    __tablename__ = 'galleries'

    def __init__(self):
        self.id = uuid.uuid4()

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

class Image(Base):
    __tablename__ = 'images'

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
    legacy_url = Column(
        String,
        nullable=False
    )
    url = Column(
        String,
        nullable=False
    )
    link = Column(
        String
    )
    caption = Column(
        String
    )
    embargo_date = Column(
        TIMESTAMP
    )

class ImageConnection(Base):
    __tablename__ = 'image_connections'

    def __init__(self):
        self.id = uuid.uuid4()

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    image_id = Column(
        UUID(as_uuid=True),
        ForeignKey('images.id'),
        nullable=False
    )
    gallery_id = Column(
        UUID(as_uuid=True),
        ForeignKey('galleries.id'),
        nullable=False
    )

    image = relationship("Image", foreign_keys=[image_id])
    gallery = relationship("Gallery", foreign_keys=[gallery_id])