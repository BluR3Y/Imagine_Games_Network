import json
import uuid
from config import Base

from sqlalchemy import Column, String, ForeignKey, Enum, Integer, ARRAY, JSON, TIMESTAMP, NUMERIC, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator, VARCHAR, UserDefinedType

class Video(Base):
    __tablename__ = 'videos'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    legacy_id = Column(UUID(as_uuid=True))
    content_id = Column(
        UUID(as_uuid=True),
        ForeignKey("contents.id"),
        nullable=False
    )
    metadata_id = Column(
        UUID(as_uuid=True),
        ForeignKey("video_metadatas.id"),
        nullable=False
    )

    content = relationship("Content")
    metadata = relationship("VideoMetadata")

class VideoMetadata(Base):
    __tablename__ = 'video_metadatas'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    ad_breaks = Column(BOOLEAN)
    chat_enabled = Column(BOOLEAN)
    description_html = Column(String)
    downloadable = Column(BOOLEAN)
    duration = Column(NUMERIC)
    m3u_url = Column(String)

class VideoAsset(Base):
    __tablename__ = 'video_assets'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    metadata_id = Column(
        UUID(as_uuid=True),
        ForeignKey("video_metadatas.id"),
        nullable=False
    )
    url = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    fps = Column(Integer)

    metadata = relationship("VideoMetadata")

class VideoCaption(Base):
    __tablename__ = 'video_captions'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    metadata_id = Column(
        UUID(as_uuid=True),
        ForeignKey("video_metadatas.id"),
        nullable=False
    )
    language = Column(String)
    text = Column(String)

    metadata = relationship("VideoMetadata")