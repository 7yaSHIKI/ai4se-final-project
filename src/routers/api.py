"""
API 路由
提供 RESTful API 接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas import FeedCreate, FeedResponse, ArticleResponse
from src.services import feed_service, rss_service
from src.models import Article, Feed
from datetime import datetime, timedelta
import json

router = APIRouter(prefix="/api", tags=["API"])


@router.post("/feeds", response_model=FeedResponse)
async def add_feed(feed_data: FeedCreate, db: Session = Depends(get_db)):
    """添加订阅源"""
    try:
        feed = await feed_service.create_feed(db, feed_data)
        return feed
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误：{str(e)}")


@router.get("/feeds", response_model=list[FeedResponse])
async def list_feeds(db: Session = Depends(get_db)):
    """获取所有订阅源"""
    feeds = feed_service.get_all_feeds(db)
    return feeds


@router.delete("/feeds/{feed_id}")
async def remove_feed(feed_id: int, db: Session = Depends(get_db)):
    """删除订阅源"""
    try:
        feed_service.delete_feed(db, feed_id)
        return {"success": True, "message": "删除成功"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/refresh")
async def refresh_feeds(db: Session = Depends(get_db)):
    """手动刷新所有订阅源"""
    result = await rss_service.refresh_all_feeds(db)
    return {
        "success": True,
        "new_articles": result["new_articles"],
        "success_count": result["success"],
        "failed_count": result["failed"]
    }


@router.get("/articles", response_model=list[ArticleResponse])
async def list_articles(tag: str = None, db: Session = Depends(get_db)):
    """获取文章列表（支持按标签筛选）"""
    # 基础查询：最近 7 天
    from src.config import settings
    cutoff = datetime.utcnow() - timedelta(days=settings.ARTICLE_RETENTION_DAYS)
    query = db.query(Article).filter(Article.published_at >= cutoff)

    # 按标签筛选
    if tag:
        feeds_with_tag = db.query(Feed).filter(Feed.tags.contains(f'"{tag}"')).all()
        feed_ids = [f.id for f in feeds_with_tag]
        if feed_ids:
            query = query.filter(Article.feed_id.in_(feed_ids))
        else:
            return []

    # 按时间倒序
    articles = query.order_by(Article.published_at.desc()).limit(100).all()

    # 附加 feed_name
    result = []
    for article in articles:
        article_dict = ArticleResponse.from_orm(article).model_dump()
        article_dict['feed_name'] = article.feed.name
        result.append(ArticleResponse(**article_dict))

    return result
