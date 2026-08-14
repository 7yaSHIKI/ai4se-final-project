"""
AI 摘要服务测试
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.services import summary_service


@pytest.mark.asyncio
async def test_generate_summary_success():
    """测试成功生成摘要"""
    with patch('src.services.summary_service.client.chat.completions.create') as mock_create:
        # 模拟 OpenAI API 响应
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "这是一篇关于 Python 编程的文章摘要。"
        mock_create.return_value = mock_response

        success, summary = await summary_service.generate_summary(
            content="Python 是一种高级编程语言...",
            title="Python 编程入门"
        )

        assert success is True
        assert "Python" in summary
        assert len(summary) > 0


@pytest.mark.asyncio
async def test_generate_summary_api_error():
    """测试 API 调用失败"""
    with patch('src.services.summary_service.client.chat.completions.create') as mock_create:
        # 模拟 API 错误
        mock_create.side_effect = Exception("API rate limit exceeded")

        success, result = await summary_service.generate_summary(
            content="测试内容",
            title="测试标题"
        )

        assert success is False
        assert "LLM 调用失败" in result


def test_strip_html_tags():
    """测试 HTML 标签清理"""
    html_text = "<p>这是<strong>测试</strong>内容</p><br/>"
    clean_text = summary_service.strip_html_tags(html_text)

    assert "<p>" not in clean_text
    assert "<strong>" not in clean_text
    assert "这是测试内容" in clean_text


@pytest.mark.asyncio
async def test_generate_summary_truncate_content():
    """测试长内容截取"""
    with patch('src.services.summary_service.client.chat.completions.create') as mock_create:
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "摘要"
        mock_create.return_value = mock_response

        long_content = "测试" * 2000  # 超过 2000 字符
        success, summary = await summary_service.generate_summary(long_content)

        assert success is True
        # 验证传递给 API 的内容被截取
        call_args = mock_create.call_args
        prompt = call_args[1]['messages'][1]['content']
        assert len(prompt) < len(long_content)
