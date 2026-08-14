"""
Web 页面路由
提供 HTML 页面
"""
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.template_config import templates
from src.models import Article, Feed
from src.services import summary_service
from datetime import datetime, timedelta
import json

router = APIRouter(tags=["Web"])


@router.get("/")
async def index(request: Request, tag: str = None, db: Session = Depends(get_db)):
    """首页 - 文章列表"""
    from src.config import settings

    # 获取所有标签
    feeds = db.query(Feed).all()
    all_tags = set()
    for feed in feeds:
        if feed.tags:
            try:
                tags_list = json.loads(feed.tags)
                all_tags.update(tags_list)
            except:
                pass

    # 获取文章
    cutoff = datetime.utcnow() - timedelta(days=settings.ARTICLE_RETENTION_DAYS)
    query = db.query(Article).filter(Article.published_at >= cutoff)

    if tag:
        feeds_with_tag = db.query(Feed).filter(Feed.tags.contains(f'"{tag}"')).all()
        feed_ids = [f.id for f in feeds_with_tag]
        if feed_ids:
            query = query.filter(Article.feed_id.in_(feed_ids))

    articles = query.order_by(Article.published_at.desc()).limit(50).all()

    # 为每篇文章附加 feed_name
    for article in articles:
        article.feed_name = article.feed.name

    # 为未生成摘要的文章生成摘要（异步，最多5篇）
    pending_articles = [a for a in articles if a.summary_status == 'pending'][:5]
    for article in pending_articles:
        await summary_service.generate_article_summary(db, article)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "articles": articles,
        "tags": sorted(all_tags),
        "current_tag": tag
    })


@router.get("/feeds")
async def feeds_page(request: Request, db: Session = Depends(get_db)):
    """订阅管理页面"""
    from src.services import feed_service
    feeds = feed_service.get_all_feeds(db)
    return templates.TemplateResponse("feeds.html", {
        "request": request,
        "feeds": feeds
    })


# 自定义 Jinja2 过滤器
def from_json_filter(value):
    """将 JSON 字符串转换为 Python 对象"""
    if not value:
        return []
    try:
        return json.loads(value)
    except:
        return []


# 注册过滤器
templates.env.filters['from_json'] = from_json_filter
