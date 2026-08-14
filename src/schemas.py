from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional, List

# Feed schemas
class FeedBase(BaseModel):
    name: str
    url: str
    tags: Optional[str] = None

class FeedCreate(FeedBase):
    pass

class FeedResponse(FeedBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Article schemas
class ArticleBase(BaseModel):
    title: str
    link: str
    published_at: datetime

class ArticleResponse(ArticleBase):
    id: int
    feed_id: int
    summary: Optional[str] = None
    summary_status: str
    created_at: datetime
    feed_name: Optional[str] = None  # 关联的订阅源名称

    class Config:
        from_attributes = True
