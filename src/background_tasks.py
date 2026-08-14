"""
后台任务
定期抓取 RSS 和清理旧文章
"""
import asyncio
from datetime import datetime, timedelta
from src.database import SessionLocal
from src.services import rss_service, cleanup_service
from src.config import settings, logger


async def background_fetch_task():
    """后台定时抓取任务 - 每小时执行一次"""
    logger.info("✓ 后台抓取任务已启动")

    while True:
        try:
            logger.info("开始抓取 RSS...")
            db = SessionLocal()
            result = await rss_service.refresh_all_feeds(db)
            db.close()
            logger.info(f"✓ 抓取完成：新增 {result['new_articles']} 篇文章")
        except Exception as e:
            logger.error(f"✗ 后台抓取失败：{str(e)}")

        # 等待下一次执行
        await asyncio.sleep(settings.RSS_FETCH_INTERVAL)


async def background_cleanup_task():
    """后台定时清理任务 - 每天凌晨 3 点执行"""
    logger.info("✓ 后台清理任务已启动")

    while True:
        try:
            # 计算等到凌晨 3 点的时间
            now = datetime.now()
            target = now.replace(hour=3, minute=0, second=0, microsecond=0)
            if target <= now:
                target = target + timedelta(days=1)

            wait_seconds = (target - now).total_seconds()
            logger.info(f"下次清理时间：{target.strftime('%Y-%m-%d %H:%M:%S')} ({wait_seconds/3600:.1f} 小时后)")
            await asyncio.sleep(wait_seconds)

            # 执行清理
            logger.info("开始清理旧文章...")
            db = SessionLocal()
            count = cleanup_service.cleanup_old_articles(db)
            db.close()
            logger.info(f"✓ 清理完成：删除 {count} 篇文章")

        except Exception as e:
            logger.error(f"✗ 后台清理失败：{str(e)}")
            await asyncio.sleep(3600)  # 失败后 1 小时重试
