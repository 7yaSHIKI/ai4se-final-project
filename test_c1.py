#!/usr/bin/env python3
"""
Task C1 验证脚本
测试订阅管理服务 - 添加订阅功能
"""

import asyncio
import sys
sys.path.insert(0, '/home/seiha/Courses/AI4SE/ai4se-final-project')

from src.services.feed_service import validate_rss_url


async def test_validate_rss_url():
    """测试 RSS URL 验证功能"""
    print("=" * 60)
    print("Task C1 功能验证：RSS URL 验证")
    print("=" * 60)

    # 测试用例
    test_cases = [
        ("https://www.ruanyifeng.com/blog/atom.xml", "阮一峰的网络日志"),
        ("https://invalid-url-that-does-not-exist.com/rss", None),
        ("https://www.google.com", None),  # 非 RSS URL
    ]

    for url, expected_name in test_cases:
        print(f"\n测试 URL: {url}")
        print(f"期望结果: {'成功' if expected_name else '失败'}")

        is_valid, result = await validate_rss_url(url)

        if is_valid:
            print(f"✅ 验证通过 - Feed 标题: {result}")
        else:
            print(f"❌ 验证失败 - 错误信息: {result}")

        print("-" * 60)


if __name__ == "__main__":
    asyncio.run(test_validate_rss_url())
