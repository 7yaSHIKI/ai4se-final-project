from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Feed(Base):
    __tablename__ = "feeds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False, unique=True)
    tags = Column(Text)  # JSON 数组字符串
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    articles = relationship("Article", back_populates="feed", cascade="all, delete-orphan")

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    feed_id = Column(Integer, ForeignKey("feeds.id"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    link = Column(String(1000), nullable=False, unique=True)
    content = Column(Text)
    summary = Column(Text)
    summary_status = Column(String(20), default="pending", index=True)  # pending/success/failed
    published_at = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    feed = relationship("Feed", back_populates="articles")

    # 复合索引
    __table_args__ = (
        Index('idx_feed_published', 'feed_id', 'published_at'),
        Index('idx_status_published', 'summary_status', 'published_at'),
    )
