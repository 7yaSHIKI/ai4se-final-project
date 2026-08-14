"""
RSS 抓取服务测试
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.services import rss_service
import feedparser


@pytest.mark.asyncio
async def test_fetch_rss_content_success():
    """测试成功抓取 RSS"""
    mock_response = """<?xml version="1.0"?>
    <rss version="2.0">
      <channel>
        <title>Test Feed</title>
        <item>
          <title>Test Article</title>
          <link>http://example.com/1</link>
          <pubDate>Mon, 13 Aug 2026 12:00:00 GMT</pubDate>
          <description>Test content</description>
        </item>
      </channel>
    </rss>"""

    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = AsyncMock()
        mock_get.return_value.text = mock_response
        mock_get.return_value.raise_for_status = MagicMock()

        result = await rss_service.fetch_rss_content("http://test.com/rss")

        assert len(result.entries) > 0
        assert result.entries[0].title == "Test Article"


@pytest.mark.asyncio
async def test_fetch_rss_content_timeout():
    """测试抓取超时"""
    import httpx

    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.side_effect = httpx.TimeoutException("Timeout")

        with pytest.raises(Exception, match="抓取超时"):
            await rss_service.fetch_rss_content("http://test.com/rss")


@pytest.mark.asyncio
async def test_extract_articles_from_feed():
    """测试从 RSS 提取文章"""
    mock_rss = """<?xml version="1.0"?>
    <rss version="2.0">
      <channel>
        <item>
          <title>Article 1</title>
          <link>http://example.com/1</link>
          <pubDate>Mon, 13 Aug 2026 12:00:00 GMT</pubDate>
          <description>Content 1</description>
        </item>
        <item>
          <title>Article 2</title>
          <link>http://example.com/2</link>
          <pubDate>Tue, 14 Aug 2026 12:00:00 GMT</pubDate>
          <description>Content 2</description>
        </item>
      </channel>
    </rss>"""

    feed_obj = feedparser.parse(mock_rss)
    articles = await rss_service.extract_articles_from_feed(feed_obj, feed_id=1)

    assert len(articles) == 2
    assert articles[0]['title'] == "Article 1"
    assert articles[0]['link'] == "http://example.com/1"
    assert articles[0]['feed_id'] == 1
    assert articles[1]['title'] == "Article 2"


@pytest.mark.asyncio
async def test_extract_articles_no_pubdate():
    """测试处理没有发布时间的文章"""
    mock_rss = """<?xml version="1.0"?>
    <rss version="2.0">
      <channel>
        <item>
          <title>No Date Article</title>
          <link>http://example.com/nodate</link>
          <description>Content</description>
        </item>
      </channel>
    </rss>"""

    feed_obj = feedparser.parse(mock_rss)
    articles = await rss_service.extract_articles_from_feed(feed_obj, feed_id=1)

    assert len(articles) == 1
    assert articles[0]['published_at'] is not None  # 应该使用当前时间
