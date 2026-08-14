"""
数据清理服务
清理过期文章
"""
from sqlalchemy.orm import Session
from src.models import Article
from src.config import settings, logger
from datetime import datetime, timedelta


def cleanup_old_articles(db: Session) -> int:
    """
    清理超过保留期的文章

    Args:
        db: 数据库会话

    Returns:
        删除的文章数量
    """
    cutoff_date = datetime.utcnow() - timedelta(days=settings.ARTICLE_RETENTION_DAYS)

    try:
        # 查询过期文章
        old_articles = db.query(Article).filter(
            Article.published_at < cutoff_date
        ).all()

        count = len(old_articles)

        if count == 0:
            logger.info("没有需要清理的文章")
            return 0

        # 删除
        for article in old_articles:
            db.delete(article)

        db.commit()
        logger.info(f"✓ 清理完成：删除 {count} 篇超过 {settings.ARTICLE_RETENTION_DAYS} 天的文章")
        return count

    except Exception as e:
        logger.error(f"清理失败: {str(e)}")
        db.rollback()
        return 0
