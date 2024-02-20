import json
import uuid
from imagine_games_scraper.alchemy.config import Base

from sqlalchemy import Column, String, ForeignKey, Enum, Integer, ARRAY, JSON, TIMESTAMP, DECIMAL, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator, VARCHAR, UserDefinedType

class ArticleContent(Base):
    __tablename__ = 'article_contents'

    def __init__(self):
        self.id = uuid.uuid4()

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
    article_content_id = Column(
        UUID(as_uuid=True),
        ForeignKey("article_contents.id"),
        nullable=False
    )
    review_id = Column(
        UUID(as_uuid=True),
        ForeignKey("official_reviews.id")
    )

    content = relationship("Content", foreign_keys=[content_id])
    article_content = relationship("ArticleContent", foreign_keys=[article_content_id])
    review = relationship("OfficialReview", foreign_keys=[review_id])