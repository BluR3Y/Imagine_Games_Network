import json
import uuid
from imagine_games_scraper.alchemy.config import Base

from sqlalchemy import Column, String, ForeignKey, Enum, Integer, ARRAY, JSON, TIMESTAMP, DECIMAL, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class Content(Base):
    __tablename__ = 'contents'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    legacy_id = Column(UUID(as_uuid=True))
    url = Column(String)
    slug = Column(String)
    type = Column(String)
    vertical = Column(String)
    cover_id = Column(
        UUID(as_uuid=True),
        ForeignKey("images.id")
    )
    title = Column(String)
    subtitle = Column(String)
    feed_title = Column(String)
    feed_cover_id = Column(
        UUID(as_uuid=True),
        ForeignKey("images.id")
    )
    primary_object_id = Column(
        UUID(as_uuid=True),
        ForeignKey("objects.id"),
        nullable=False
    )
    excerpt = Column(String)
    description = Column(String)
    state = Column(String)
    publish_date = Column(TIMESTAMP)
    modify_date = Column(TIMESTAMP)
    events = Column(ARRAY(String))
    brand_id = Column(
        UUID(as_uuid=True),
        ForeignKey("brands.id")
    )
    category_id = Column(
        UUID(as_uuid=True),
        ForeignKey("content_categories.id")
    )

    cover = relationship("Image", foreign_keys=[cover_id])
    feed_cover = relationship("Image", foreign_keys=[feed_cover_id])
    primary_object = relationship("Object", foreign_keys=[primary_object_id])
    brand = relationship("Brand", foreign_keys=[brand_id])
    category = relationship("ContentCategory", foreign_keys=[category_id])

class Brand(Base):
    __tablename__ = 'brands'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    legacy_id = Column(UUID(as_uuid=True))
    slug = Column(String)
    name = Column(String)
    logo_light = Column(String)
    logo_dark = Column(String)


class ContentCategory(Base):
    __tablename__ = 'content_categories'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    legacy_id = Column(UUID(as_uuid=True))
    name = Column(String)

class ObjectConnection(Base):
    __tablename__ = 'object_connections'

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
    object_id = Column(
        UUID(as_uuid=True),
        ForeignKey("objects.id"),
        nullable=False
    )

    content = relationship("Content", foreign_keys=[content_id])
    object = relationship("Object", foreign_keys=[object_id])

class Contributor(Base):
    __tablename__ = 'contributors'

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
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    content = relationship("Content", foreign_keys=[content_id])
    user = relationship("User", foreign_keys=[user_id])

class ContentAttributeConnection(Base):
    __tablename__ = 'content_attribute_connections'

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
    attribute_id = Column(
        UUID(as_uuid=True),
        ForeignKey("typed_attributes.id"),
        nullable=False
    )

    content = relationship("Content", foreign_keys=[content_id])
    attribute = relationship("TypedAttribute", foreign_keys=[attribute_id])

class Slideshow(Base):
    __tablename__ = 'slideshows'

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
    gallery_id = Column(
        UUID(as_uuid=True),
        ForeignKey("galleries.id"),
        nullable=False
    )

    content = relationship("Content", foreign_keys=[content_id])
    gallery = relationship("Gallery", foreign_keys=[gallery_id])

class OfficialReview(Base):
    __tablename__ = 'official_reviews'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    legacy_id = Column(UUID(as_uuid=True))
    score = Column(Integer)
    score_text = Column(String)
    editors_choice = Column(Boolean)
    score_summary = Column(String)
    article_url = Column(String)
    video_url = Column(String)
    review_data = Column(TIMESTAMP)

class UserReview(Base):
    __tablename__ = 'user_reviews'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    legacy_id = Column(UUID(as_uuid=True))
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )
    legacy_user_id = Column(UUID(as_uuid=True))
    object_id = Column(
        UUID(as_uuid=True),
        ForeignKey("objects.id"),
        nullable=False
    )
    legacy_object_id = Column(UUID(as_uuid=True))
    is_liked = Column(Boolean)
    score = Column(Integer)
    text = Column(String)
    is_spoiler = Column(Boolean)
    is_private = Column(Boolean)
    publish_date = Column(TIMESTAMP)
    modify_date = Column(TIMESTAMP)
    platform_id = Column(
        UUID(as_uuid=True),
        ForeignKey("attributes.id")
    )

    user = relationship("User", foreign_keys=[user_id])
    object = relationship("Object", foreign_keys=[object_id])
    platform = relationship("Attribute", foreign_keys=[platform_id])

class UserReviewTag(Base):
    __tablename__ = 'user_review_tags'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    legacy_id = Column(UUID(as_uuid=True))
    review_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user_reviews.id"),
        nullable=False
    )
    name = Column(String)
    is_positive = Column(Boolean)

    review = relationship("UserReview", foreign_keys=[review_id])