from sqlalchemy.orm import Session
from src.models import Feed
from src.schemas import FeedCreate
from src.config import logger
import feedparser
import httpx
import json


async def validate_rss_url(url: str) -> tuple[bool, str]:
    """验证 RSS URL 是否有效"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()

        # 尝试解析 RSS
        feed = feedparser.parse(response.text)
        if feed.bozo:
            return False, "无法解析 RSS，请检查 URL"

        return True, feed.feed.get('title', 'Untitled Feed')
    except httpx.TimeoutException:
        return False, "连接超时"
    except Exception as e:
        return False, f"错误：{str(e)}"


async def create_feed(db: Session, feed_data: FeedCreate) -> Feed:
    """添加订阅源"""
    # 检查是否已存在
    existing = db.query(Feed).filter(Feed.url == feed_data.url).first()
    if existing:
        raise ValueError("该订阅源已存在")

    # 验证 URL
    is_valid, result = await validate_rss_url(feed_data.url)
    if not is_valid:
        raise ValueError(result)

    # 如果没有提供名称，使用从 RSS 提取的标题
    if not feed_data.name:
        feed_data.name = result

    # 创建订阅源
    feed = Feed(
        name=feed_data.name,
        url=feed_data.url,
        tags=json.dumps(feed_data.tags.split(',') if feed_data.tags else [])
    )
    db.add(feed)
    db.commit()
    db.refresh(feed)

    logger.info(f"✓ 添加订阅源：{feed.name}")
    return feed
