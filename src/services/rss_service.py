"""
RSS 抓取服务
负责从 RSS 源获取文章
"""
import feedparser
import httpx
from datetime import datetime
from sqlalchemy.orm import Session
from src.models import Feed, Article
from src.config import settings, logger
from typing import List, Dict, Any
from dateutil import parser as date_parser


async def fetch_rss_content(url: str) -> feedparser.FeedParserDict:
    """
    抓取 RSS 内容

    Args:
        url: RSS feed URL

    Returns:
        解析后的 RSS 对象

    Raises:
        Exception: 网络错误或解析失败
    """
    try:
        async with httpx.AsyncClient(timeout=settings.RSS_TIMEOUT) as client:
            response = await client.get(url)
            response.raise_for_status()

        # 解析 RSS
        feed = feedparser.parse(response.text)

        if feed.bozo:  # 解析错误
            logger.warning(f"RSS 解析警告 {url}: {feed.bozo_exception}")

        return feed

    except httpx.TimeoutException:
        logger.error(f"RSS 抓取超时: {url}")
        raise Exception(f"抓取超时（>{settings.RSS_TIMEOUT}秒）")
    except Exception as e:
        logger.error(f"RSS 抓取失败 {url}: {str(e)}")
        raise


async def extract_articles_from_feed(feed_obj: feedparser.FeedParserDict, feed_id: int) -> List[Dict[str, Any]]:
    """
    从 RSS feed 对象中提取文章列表

    Args:
        feed_obj: feedparser 解析的对象
        feed_id: 数据库中的 feed ID

    Returns:
        文章字典列表
    """
    articles = []

    for entry in feed_obj.entries:
        try:
            # 提取发布时间
            published_at = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published_at = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                published_at = datetime(*entry.updated_parsed[:6])
            elif hasattr(entry, 'published'):
                published_at = date_parser.parse(entry.published)
            else:
                published_at = datetime.utcnow()

            # 提取内容
            content = ""
            if hasattr(entry, 'content') and entry.content:
                content = entry.content[0].value
            elif hasattr(entry, 'summary'):
                content = entry.summary
            elif hasattr(entry, 'description'):
                content = entry.description

            article_data = {
                'feed_id': feed_id,
                'title': entry.get('title', '无标题'),
                'link': entry.get('link', ''),
                'content': content,
                'published_at': published_at,
                'summary_status': 'pending'
            }

            articles.append(article_data)

        except Exception as e:
            logger.warning(f"解析文章失败: {str(e)}")
            continue

    return articles


async def fetch_and_save_articles(db: Session, feed: Feed) -> int:
    """
    抓取单个 feed 的文章并保存到数据库

    Args:
        db: 数据库会话
        feed: Feed 对象

    Returns:
        新增文章数量
    """
    try:
        # 抓取 RSS
        feed_obj = await fetch_rss_content(feed.url)

        # 提取文章
        articles_data = await extract_articles_from_feed(feed_obj, feed.id)

        # 保存到数据库（去重）
        new_count = 0
        for article_data in articles_data:
            # 检查是否已存在
            exists = db.query(Article).filter(
                Article.link == article_data['link']
            ).first()

            if not exists:
                article = Article(**article_data)
                db.add(article)
                new_count += 1

        db.commit()
        logger.info(f"✓ {feed.name}: 抓取到 {len(articles_data)} 篇，新增 {new_count} 篇")
        return new_count

    except Exception as e:
        logger.error(f"✗ {feed.name} 抓取失败: {str(e)}")
        db.rollback()
        return 0


async def refresh_all_feeds(db: Session) -> Dict[str, int]:
    """
    刷新所有订阅源

    Args:
        db: 数据库会话

    Returns:
        统计信息：{'new_articles': 10, 'success': 5, 'failed': 1}
    """
    feeds = db.query(Feed).all()

    total_new = 0
    success_count = 0
    failed_count = 0

    logger.info(f"开始刷新 {len(feeds)} 个订阅源...")

    for feed in feeds:
        try:
            new_count = await fetch_and_save_articles(db, feed)
            total_new += new_count
            success_count += 1
        except Exception as e:
            failed_count += 1
            logger.error(f"刷新失败 {feed.name}: {str(e)}")

    logger.info(f"✓ 刷新完成：新增 {total_new} 篇文章，成功 {success_count}/{len(feeds)}")

    return {
        'new_articles': total_new,
        'success': success_count,
        'failed': failed_count
    }
