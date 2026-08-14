#!/usr/bin/env python3
"""
数据库初始化脚本
创建所有表和索引
"""
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.database import init_db
from src.config import logger

if __name__ == "__main__":
    logger.info("开始初始化数据库...")
    try:
        init_db()
        logger.info("✓ 数据库初始化成功")
        logger.info("✓ 所有表和索引已创建")
    except Exception as e:
        logger.error(f"✗ 数据库初始化失败: {e}")
        sys.exit(1)
