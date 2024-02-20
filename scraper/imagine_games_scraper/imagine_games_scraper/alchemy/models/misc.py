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

class Attribute(Base):
    __tablename__ = 'attributes'

    def __init__(self):
        self.id = uuid.uuid4()

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    name = Column(
        String
    )
    short_name = Column(
        String
    )
    slug = Column(
        String
    )

class TypedAttribute(Base):
    __tablename__ = 'typed_attributes'

    def __init__(self):
        self.id = uuid.uuid4()

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    type = Column(
        String,
        nullable=False
    )
    attribute_id = Column(
        UUID(as_uuid=True),
        ForeignKey('attributes.id'),
        nullable=False
    )

    attribute = relationship("Attribute", foreign_keys=[attribute_id])

class PollConfiguration(Base):
    __tablename__ = 'poll_configurations'

    def __init__(self):
        self.id = uuid.uuid4()

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    require_authentication = Column(BOOLEAN)
    require_authentication_for_results = Column(BOOLEAN)
    multi_choice = Column(BOOLEAN)
    auto_display_results = Column(BOOLEAN)

class Poll(Base):
    __tablename__ = 'polls'

    def __init__(self):
        self.id = uuid.uuid4()

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
    configuration_id = Column(
        UUID(as_uuid=True),
        ForeignKey("poll_configurations.id")
    )
    image_id = Column(
        UUID(as_uuid=True),
        ForeignKey("images.id")
    )
    voters = Column(Integer)

    content = relationship("Content", foreign_keys=[content_id])
    configuration = relationship("PollConfiguration", foreign_keys=[configuration_id])
    image = relationship("Image", foreign_keys=[image_id])

class PollAnswer(Base):
    __tablename__ = 'poll_answer'

    def __init__(self):
        self.id = uuid.uuid4()

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    legacy_id = Column(Integer)
    poll_id = Column(
        UUID(as_uuid=True),
        ForeignKey("polls.id"),
        nullable=False
    )
    answer = Column(String)
    votes = Column(Integer)

    poll = relationship("Poll", foreign_keys=[poll_id])

class Catalog(Base):
    __tablename__ = 'catalogs'

    def __init__(self):
        self.id = uuid.uuid4()

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    content_id = Column(
        UUID(as_uuid=True),
        ForeignKey("contents.id"),
        nullable=False
    )

    content = relationship("Content", foreign_keys=[content_id])

class CommerceDeal(Base):
    __tablename__ = 'commerce_deals'

    def __init__(self):
        self.id = uuid.uuid4()

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    legacy_id = Column(UUID(as_uuid=True))
    url = Column(String)
    title = Column(String)
    description = Column(String)
    brand = Column(String)
    model = Column(String)
    vendor = Column(String)
    price = Column(NUMERIC)
    msrp = Column(NUMERIC)
    discount = Column(NUMERIC)
    coupon_code = Column(String)
    sponsor_disclosure = Column(String)
    is_large = Column(BOOLEAN)
    region_code = Column(String)
    up_votes = Column(Integer)
    cover_id = Column(
        UUID(as_uuid=True),
        ForeignKey("images.id")
    )

    cover = relationship("Image", foreign_keys=[cover_id])

class DealConnection(Base):
    __tablename__ = 'deal_connections'

    def __init__(self):
        self.id = uuid.uuid4()

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    deal_id = Column(
        UUID(as_uuid=True),
        ForeignKey("commerce_deals.id"),
        nullable=False
    )
    catalog_id = Column(
        UUID(as_uuid=True),
        ForeignKey("catalogs.id"),
        nullable=False
    )

    deal = relationship("CommerceDeal", foreign_keys=[deal_id])
    catalog = relationship("Catalog", foreign_keys=[catalog_id])