import json
import uuid
from config import Base

from sqlalchemy import Column, String, ForeignKey, Enum, Integer, ARRAY, JSON, TIMESTAMP, DECIMAL, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator, VARCHAR, UserDefinedType

class ArticleContent(Base):
    __tablename__ = 'article_contents'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    legacy_id = Column(UUID(as_uuid=True))
    hero_video_content_id = Column(UUID(as_uuid=True))
    hero_video_content_slug = Column(String)
    processed_html = Column(String)


class Article(Base):
    __tablename__ = 'articles'

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
    article_content_id = Column(
        UUID(as_uuid=True),
        ForeignKey("article_contents.id"),
        nullable=False
    )
    review_id = Column(
        UUID(as_uuid=True),
        ForeignKey("official_reviews.id")
    )

    content = relationship("Content")
    article = relationship("Article")
    review = relationship("OfficialReview")