import logging
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""
    # OpenAI API
    OPENAI_API_KEY: str

    # 数据库
    DATABASE_URL: str = "sqlite:///./data/rss_aggregator.db"

    # 日志
    LOG_LEVEL: str = "INFO"

    # 应用
    PORT: int = 8000

    # RSS 配置
    RSS_FETCH_INTERVAL: int = 3600  # 1 小时
    RSS_TIMEOUT: int = 10  # 10 秒

    # 数据保留
    ARTICLE_RETENTION_DAYS: int = 7

    class Config:
        env_file = ".env"
        case_sensitive = True


# 加载配置
settings = Settings()

# 创建 logs 目录
Path("logs").mkdir(exist_ok=True)

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
