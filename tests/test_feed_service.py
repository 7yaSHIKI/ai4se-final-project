"""
订阅管理服务测试
"""
import pytest
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base, Feed
from src.services import feed_service
from src.schemas import FeedCreate


@pytest.fixture
def db():
    """创建内存数据库用于测试"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.mark.asyncio
async def test_create_feed_success(db):
    """测试成功创建订阅"""
    feed_data = FeedCreate(
        name="阮一峰的网络日志",
        url="https://www.ruanyifeng.com/blog/atom.xml",
        tags="技术,博客"
    )

    feed = await feed_service.create_feed(db, feed_data)

    assert feed.id is not None
    assert feed.name == "阮一峰的网络日志"
    assert feed.url == "https://www.ruanyifeng.com/blog/atom.xml"
    assert '"技术"' in feed.tags
    assert '"博客"' in feed.tags


@pytest.mark.asyncio
async def test_create_feed_duplicate(db):
    """测试重复订阅检查"""
    feed_data = FeedCreate(
        name="测试订阅",
        url="https://www.ruanyifeng.com/blog/atom.xml",
        tags="技术"
    )

    # 第一次创建成功
    await feed_service.create_feed(db, feed_data)

    # 第二次应该失败
    with pytest.raises(ValueError, match="已订阅该源"):
        await feed_service.create_feed(db, feed_data)


def test_delete_feed(db):
    """测试删除订阅"""
    # 创建测试数据
    feed = Feed(
        name="测试",
        url="http://test.com/rss",
        tags='["技术"]'
    )
    db.add(feed)
    db.commit()
    feed_id = feed.id

    # 删除
    feed_service.delete_feed(db, feed_id)

    # 验证已删除
    assert db.query(Feed).filter(Feed.id == feed_id).first() is None


def test_delete_feed_not_found(db):
    """测试删除不存在的订阅"""
    with pytest.raises(ValueError, match="订阅源不存在"):
        feed_service.delete_feed(db, 999)


def test_get_all_feeds(db):
    """测试获取所有订阅"""
    # 创建测试数据
    feed1 = Feed(name="Feed 1", url="http://test1.com/rss", tags='["技术"]')
    feed2 = Feed(name="Feed 2", url="http://test2.com/rss", tags='["新闻"]')
    db.add_all([feed1, feed2])
    db.commit()

    # 获取所有订阅
    feeds = feed_service.get_all_feeds(db)

    assert len(feeds) == 2
    assert feeds[0].name == "Feed 1"
    assert feeds[1].name == "Feed 2"


def test_update_feed_tags(db):
    """测试更新订阅标签"""
    # 创建测试数据
    feed = Feed(name="测试", url="http://test.com/rss", tags='["技术"]')
    db.add(feed)
    db.commit()

    # 更新标签
    feed_service.update_feed_tags(db, feed.id, "技术,博客,Python")

    # 验证
    updated_feed = db.query(Feed).filter(Feed.id == feed.id).first()
    assert '"技术"' in updated_feed.tags
    assert '"博客"' in updated_feed.tags
    assert '"Python"' in updated_feed.tags
