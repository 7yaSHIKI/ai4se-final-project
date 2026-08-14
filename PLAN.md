# PLAN.md - AI-Powered RSS Aggregator Implementation Plan

> **项目名称**：AI-Powered RSS Aggregator  
> **版本**：1.0  
> **创建日期**：2026-08-13  
> **状态**：规划中

---

## 📋 任务总览

**总任务数**：45 个  
**预计总工时**：40-50 小时  
**目标完成时间**：14 天

### 进度统计

| 状态 | 数量 | 百分比 |
|------|------|--------|
| ✅ 已完成 | 0 | 0% |
| 🟡 进行中 | 0 | 0% |
| ⬜ 未开始 | 45 | 100% |

---

## 🗂️ 任务分组

### 阶段 A：项目基础设施（7 个任务）
- 环境搭建、目录结构、基础配置

### 阶段 B：数据层（5 个任务）
- 数据库设计、ORM 模型

### 阶段 C：核心服务层（12 个任务）
- 订阅管理、RSS 抓取、AI 摘要

### 阶段 D：API 层（6 个任务）
- FastAPI 路由、接口实现

### 阶段 E：前端 UI（6 个任务）
- 模板、静态资源、页面实现

### 阶段 F：后台任务（3 个任务）
- 定时抓取、清理任务

### 阶段 G：测试（4 个任务）
- 单元测试、集成测试

### 阶段 H：部署（2 个任务）
- Docker、云端部署

---

## 📝 详细任务列表

---

## 阶段 A：项目基础设施

### Task A1：创建项目目录结构

**目标**：建立完整的项目目录

**文件**：
```
src/
├── __init__.py
├── main.py
├── config.py
├── database.py
├── models.py
├── schemas.py
├── services/
│   └── __init__.py
├── routers/
│   └── __init__.py
├── templates/
└── static/
    ├── css/
    └── js/
tests/
└── __init__.py
logs/
data/
```

**实现要点**：
- 使用 `mkdir -p` 创建嵌套目录
- 创建所有 `__init__.py` 文件

**验证**：
```bash
tree src/
ls -la tests/
```

**依赖**：无  
**可并行**：否  
**预计耗时**：2 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task A2：配置 .gitignore

**目标**：防止敏感文件和临时文件提交到 Git

**文件**：
- `.gitignore`

**实现要点**：
```
# 环境变量
.env
*.key

# Python
__pycache__/
*.py[cod]
*.so
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/

# 数据库
*.db
*.sqlite

# 日志
logs/
*.log

# 系统
.DS_Store
Thumbs.db
```

**验证**：
```bash
cat .gitignore
git status  # 确认 .env 不在追踪列表
```

**依赖**：无  
**可并行**：是  
**预计耗时**：2 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task A3：创建 .env.example

**目标**：提供环境变量模板

**文件**：
- `.env.example`

**实现要点**：
```bash
# OpenAI API Key (必需)
OPENAI_API_KEY=your_api_key_here

# 数据库 URL (可选，默认使用 SQLite)
DATABASE_URL=sqlite:///./data/rss_aggregator.db

# 日志级别 (可选，默认 INFO)
LOG_LEVEL=INFO

# 应用端口 (可选，默认 8000)
PORT=8000
```

**验证**：
```bash
cat .env.example
```

**依赖**：无  
**可并行**：是  
**预计耗时**：2 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task A4：创建 requirements.txt

**目标**：定义项目依赖

**文件**：
- `requirements.txt`

**实现要点**：
```
# Web 框架
fastapi==0.104.1
uvicorn[standard]==0.24.0

# 数据库
sqlalchemy==2.0.23
alembic==1.12.1

# RSS 解析
feedparser==6.0.10

# LLM
openai==1.3.5

# HTTP 客户端
httpx==0.25.1

# 环境变量
python-dotenv==1.0.0

# 模板引擎
jinja2==3.1.2

# 测试
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0

# 代码质量
black==23.11.0
flake8==6.1.0
```

**验证**：
```bash
pip install -r requirements.txt
pip list
```

**依赖**：无  
**可并行**：是  
**预计耗时**：2 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task A5：配置日志系统

**目标**：统一的日志记录

**文件**：
- `src/config.py`

**实现要点**：
```python
import logging
import os
from pathlib import Path

# 创建 logs 目录
Path("logs").mkdir(exist_ok=True)

# 配置日志
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

**验证**：
```python
from src.config import logger
logger.info("Test log")
# 检查 logs/app.log 文件
```

**依赖**：Task A1  
**可并行**：否  
**预计耗时**：3 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task A6：配置环境变量加载

**目标**：从 .env 加载配置

**文件**：
- `src/config.py`（追加）

**实现要点**：
```python
from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/rss_aggregator.db")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    @property
    def is_api_key_configured(self) -> bool:
        return bool(self.OPENAI_API_KEY)

settings = Settings()

# 启动检查
if not settings.is_api_key_configured:
    logger.warning("⚠️  OpenAI API Key 未配置，请创建 .env 文件并设置 OPENAI_API_KEY")
else:
    logger.info("✓ OpenAI API Key: 已配置")
```

**验证**：
```python
from src.config import settings
print(settings.is_api_key_configured)
```

**依赖**：Task A3, Task A5  
**可并行**：否  
**预计耗时**：3 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task A7：创建 FastAPI 应用骨架

**目标**：初始化 FastAPI 应用

**文件**：
- `src/main.py`

**实现要点**：
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.config import settings, logger

app = FastAPI(
    title="AI-Powered RSS Aggregator",
    version="1.0.0",
    description="订阅多个信息源，AI 自动生成摘要"
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# 模板引擎
templates = Jinja2Templates(directory="src/templates")

@app.get("/")
async def root():
    return {"message": "AI-Powered RSS Aggregator API"}

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "api_key_configured": settings.is_api_key_configured
    }

if __name__ == "__main__":
    import uvicorn
    logger.info(f"启动应用，端口：{settings.PORT}")
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
```

**验证**：
```bash
python src/main.py
# 访问 http://localhost:8000
# 访问 http://localhost:8000/health
```

**依赖**：Task A1, Task A4, Task A6  
**可并行**：否  
**预计耗时**：5 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

## 阶段 B：数据层

### Task B1：设计数据库模型

**目标**：定义 ORM 模型

**文件**：
- `src/models.py`

**实现要点**：
```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Feed(Base):
    __tablename__ = "feeds"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False, unique=True)
    tags = Column(Text)  # JSON 数组字符串
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    articles = relationship("Article", back_populates="feed", cascade="all, delete-orphan")

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    feed_id = Column(Integer, ForeignKey("feeds.id"), nullable=False)
    title = Column(String(500), nullable=False)
    link = Column(String(1000), nullable=False, unique=True)
    content = Column(Text)
    summary = Column(Text)
    summary_status = Column(String(20), default="pending")  # pending/success/failed
    published_at = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    feed = relationship("Feed", back_populates="articles")
```

**验证**：
```python
from src.models import Base, Feed, Article
print(Feed.__tablename__)
print(Article.__tablename__)
```

**依赖**：Task A4  
**可并行**：否  
**预计耗时**：5 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task B2：配置数据库连接

**目标**：建立数据库连接

**文件**：
- `src/database.py`

**实现要点**：
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import settings
from src.models import Base
from pathlib import Path

# 确保 data 目录存在
Path("data").mkdir(exist_ok=True)

# 创建引擎
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# 创建 Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建表
def init_db():
    Base.metadata.create_all(bind=engine)

# 依赖注入
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**验证**：
```python
from src.database import init_db, get_db
init_db()  # 创建表
# 检查 data/rss_aggregator.db 文件存在
```

**依赖**：Task B1  
**可并行**：否  
**预计耗时**：3 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task B3：创建 Pydantic Schemas

**目标**：定义 API 数据模型

**文件**：
- `src/schemas.py`

**实现要点**：
```python
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional, List

# Feed schemas
class FeedBase(BaseModel):
    name: str
    url: str
    tags: Optional[str] = None

class FeedCreate(FeedBase):
    pass

class FeedResponse(FeedBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Article schemas
class ArticleBase(BaseModel):
    title: str
    link: str
    published_at: datetime

class ArticleResponse(ArticleBase):
    id: int
    feed_id: int
    summary: Optional[str] = None
    summary_status: str
    created_at: datetime
    feed_name: Optional[str] = None  # 关联的订阅源名称
    
    class Config:
        from_attributes = True
```

**验证**：
```python
from src.schemas import FeedCreate, ArticleResponse
feed = FeedCreate(name="Test", url="http://example.com/rss")
print(feed.model_dump())
```

**依赖**：Task B1  
**可并行**：是  
**预计耗时**：4 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task B4：添加数据库索引

**目标**：优化查询性能

**文件**：
- `src/models.py`（修改）

**实现要点**：
在 `Article` 模型中添加索引：
```python
from sqlalchemy import Index

# 在 Article 类底部添加
__table_args__ = (
    Index('idx_published_at', 'published_at'),
    Index('idx_feed_id', 'feed_id'),
    Index('idx_summary_status', 'summary_status'),
)
```

**验证**：
```python
from src.database import engine
from sqlalchemy import inspect
inspector = inspect(engine)
print(inspector.get_indexes('articles'))
```

**依赖**：Task B2  
**可并行**：否  
**预计耗时**：2 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task B5：数据库初始化脚本

**目标**：一键初始化数据库

**文件**：
- `scripts/init_db.py`（新建）

**实现要点**：
```python
#!/usr/bin/env python3
from src.database import init_db
from src.config import logger

if __name__ == "__main__":
    logger.info("初始化数据库...")
    init_db()
    logger.info("✓ 数据库初始化完成")
```

**验证**：
```bash
python scripts/init_db.py
ls data/rss_aggregator.db
```

**依赖**：Task B2  
**可并行**：是  
**预计耗时**：2 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

## 阶段 C：核心服务层

### Task C1：订阅管理服务 - 添加订阅

**目标**：实现添加 RSS 订阅功能

**文件**：
- `src/services/feed_service.py`（新建）

**实现要点**：
```python
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
```

**验证**：
- 单元测试（Task G1）

**依赖**：Task B2, Task B3  
**可并行**：否  
**预计耗时**：8 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task C2：订阅管理服务 - 删除订阅

**目标**：实现删除订阅功能

**文件**：
- `src/services/feed_service.py`（追加）

**实现要点**：
```python
def delete_feed(db: Session, feed_id: int) -> bool:
    """删除订阅源（级联删除文章）"""
    feed = db.query(Feed).filter(Feed.id == feed_id).first()
    if not feed:
        raise ValueError("订阅源不存在")
    
    db.delete(feed)
    db.commit()
    
    logger.info(f"✓ 删除订阅源：{feed.name}")
    return True
```

**验证**：
- 单元测试

**依赖**：Task C1  
**可并行**：否  
**预计耗时**：3 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task C3：订阅管理服务 - 查询与更新

**目标**：实现订阅的查询和更新

**文件**：
- `src/services/feed_service.py`（追加）

**实现要点**：
```python
def get_all_feeds(db: Session) -> list[Feed]:
    """获取所有订阅源"""
    return db.query(Feed).order_by(Feed.created_at.desc()).all()

def get_feed_by_id(db: Session, feed_id: int) -> Feed:
    """根据 ID 获取订阅源"""
    feed = db.query(Feed).filter(Feed.id == feed_id).first()
    if not feed:
        raise ValueError("订阅源不存在")
    return feed

def update_feed_tags(db: Session, feed_id: int, tags: str) -> Feed:
    """更新订阅源标签"""
    feed = get_feed_by_id(db, feed_id)
    feed.tags = json.dumps(tags.split(',') if tags else [])
    db.commit()
    db.refresh(feed)
    
    logger.info(f"✓ 更新订阅源标签：{feed.name}")
    return feed
```

**验证**：
- 单元测试

**依赖**：Task C1  
**可并行**：否  
**预计耗时**：4 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task C4：RSS 抓取服务 - 解析 RSS

**目标**：实现 RSS 内容抓取

**文件**：
- `src/services/rss_service.py`（新建）

**实现要点**：
```python
from sqlalchemy.orm import Session
from src.models import Feed, Article
from src.config import logger
import feedparser
import httpx
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime

async def fetch_rss_content(url: str) -> dict:
    """抓取 RSS 内容"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
        
        feed = feedparser.parse(response.text)
        if feed.bozo:
            raise ValueError(f"RSS 解析失败：{feed.bozo_exception}")
        
        return feed
    except Exception as e:
        logger.error(f"抓取 RSS 失败 ({url}): {str(e)}")
        raise

async def fetch_feed_articles(db: Session, feed: Feed) -> int:
    """抓取单个订阅源的文章"""
    try:
        rss_data = await fetch_rss_content(feed.url)
        new_count = 0
        cutoff_date = datetime.utcnow() - timedelta(days=7)
        
        for entry in rss_data.entries:
            # 提取文章信息
            link = entry.get('link')
            if not link:
                continue
            
            # 检查是否已存在
            existing = db.query(Article).filter(Article.link == link).first()
            if existing:
                continue
            
            # 解析发布时间
            published_at = None
            if 'published_parsed' in entry:
                published_at = datetime(*entry.published_parsed[:6])
            elif 'updated_parsed' in entry:
                published_at = datetime(*entry.updated_parsed[:6])
            else:
                published_at = datetime.utcnow()
            
            # 只抓取 7 天内的文章
            if published_at < cutoff_date:
                continue
            
            # 提取内容
            content = entry.get('summary', '') or entry.get('description', '')
            if 'content' in entry and entry.content:
                content = entry.content[0].value
            
            # 创建文章
            article = Article(
                feed_id=feed.id,
                title=entry.get('title', 'Untitled'),
                link=link,
                content=content,
                published_at=published_at,
                summary_status='pending'
            )
            db.add(article)
            new_count += 1
        
        db.commit()
        logger.info(f"✓ 抓取 {feed.name}：新增 {new_count} 篇文章")
        return new_count
        
    except Exception as e:
        logger.error(f"抓取订阅源失败 ({feed.name}): {str(e)}")
        return 0
```

**验证**：
- 单元测试

**依赖**：Task B2, Task C1  
**可并行**：否  
**预计耗时**：10 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task C5：RSS 抓取服务 - 批量抓取

**目标**：抓取所有订阅源

**文件**：
- `src/services/rss_service.py`（追加）

**实现要点**：
```python
async def refresh_all_feeds(db: Session) -> dict:
    """刷新所有订阅源"""
    feeds = db.query(Feed).all()
    total_new = 0
    success_count = 0
    fail_count = 0
    
    for feed in feeds:
        try:
            new_count = await fetch_feed_articles(db, feed)
            total_new += new_count
            success_count += 1
        except Exception:
            fail_count += 1
    
    logger.info(f"✓ 刷新完成：成功 {success_count}，失败 {fail_count}，新增 {total_new} 篇文章")
    return {
        "success": success_count,
        "failed": fail_count,
        "new_articles": total_new
    }
```

**验证**：
- 单元测试

**依赖**：Task C4  
**可并行**：否  
**预计耗时**：4 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task C6：AI 摘要服务 - LLM 调用

**目标**：调用 OpenAI API 生成摘要

**文件**：
- `src/services/summary_service.py`（新建）

**实现要点**：
```python
from openai import AsyncOpenAI
from src.config import settings, logger
import asyncio

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_summary(content: str, max_retries: int = 3) -> tuple[bool, str]:
    """生成文章摘要"""
    if not settings.is_api_key_configured:
        return False, "OpenAI API Key 未配置"
    
    # 检测语言（简单规则：中文字符占比 > 30% 则为中文）
    chinese_chars = len([c for c in content if '一' <= c <= '鿿'])
    is_chinese = chinese_chars / len(content) > 0.3 if content else False
    language = "中文" if is_chinese else "English"
    
    # 构建 prompt
    prompt = f"""请为以下文章生成一个简短摘要（100-200字），用{language}：

{content[:5000]}  # 限制输入长度
"""
    
    # 重试逻辑
    for attempt in range(max_retries):
        try:
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "你是一个专业的文章摘要助手。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.5
            )
            
            summary = response.choices[0].message.content.strip()
            logger.info(f"✓ 生成摘要成功（尝试 {attempt + 1}/{max_retries}）")
            return True, summary
            
        except Exception as e:
            logger.warning(f"生成摘要失败（尝试 {attempt + 1}/{max_retries}）: {str(e)}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # 指数退避
            else:
                return False, f"LLM 调用失败：{str(e)}"
    
    return False, "LLM 调用失败"
```

**验证**：
- 单元测试（mock OpenAI API）

**依赖**：Task A6  
**可并行**：否  
**预计耗时**：8 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task C7：AI 摘要服务 - 为文章生成摘要

**目标**：为数据库中的文章生成摘要

**文件**：
- `src/services/summary_service.py`（追加）

**实现要点**：
```python
from sqlalchemy.orm import Session
from src.models import Article

async def generate_article_summary(db: Session, article: Article) -> bool:
    """为单篇文章生成摘要"""
    # 检查是否已有摘要
    if article.summary and article.summary_status == 'success':
        return True
    
    # 获取内容
    content = article.content or article.title
    if not content:
        article.summary = "无内容"
        article.summary_status = 'failed'
        db.commit()
        return False
    
    # 生成摘要
    success, result = await generate_summary(content)
    
    if success:
        article.summary = result
        article.summary_status = 'success'
    else:
        # 降级：显示原文前 200 字
        article.summary = f"⚠️ {result}\n\n{content[:200]}..."
        article.summary_status = 'failed'
    
    db.commit()
    return success
```

**验证**：
- 单元测试

**依赖**：Task C6  
**可并行**：否  
**预计耗时**：4 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task C8：自动清理旧文章

**目标**：删除 7 天前的文章

**文件**：
- `src/services/cleanup_service.py`（新建）

**实现要点**：
```python
from sqlalchemy.orm import Session
from src.models import Article
from src.config import logger
from datetime import datetime, timedelta

def cleanup_old_articles(db: Session, days: int = 7) -> int:
    """清理超过指定天数的文章"""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    # 查询旧文章
    old_articles = db.query(Article).filter(Article.published_at < cutoff_date).all()
    count = len(old_articles)
    
    if count > 0:
        for article in old_articles:
            db.delete(article)
        db.commit()
        logger.info(f"✓ 清理旧文章：删除 {count} 篇")
    else:
        logger.info("无需清理")
    
    return count
```

**验证**：
- 单元测试

**依赖**：Task B2  
**可并行**：是  
**预计耗时**：3 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task C9：RSS 自动发现功能

**目标**：从网站 URL 自动检测 RSS

**文件**：
- `src/services/feed_service.py`（追加）

**实现要点**：
```python
from bs4 import BeautifulSoup

async def discover_rss_from_url(url: str) -> list[str]:
    """从网站 URL 自动发现 RSS"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        rss_links = []
        
        # 查找 <link rel="alternate" type="application/rss+xml">
        for link in soup.find_all('link', rel='alternate'):
            if 'rss' in link.get('type', '').lower() or 'atom' in link.get('type', '').lower():
                rss_url = link.get('href')
                if rss_url:
                    # 处理相对 URL
                    if not rss_url.startswith('http'):
                        from urllib.parse import urljoin
                        rss_url = urljoin(url, rss_url)
                    rss_links.append(rss_url)
        
        return rss_links
    except Exception as e:
        logger.error(f"RSS 自动发现失败：{str(e)}")
        return []
```

**验证**：
- 单元测试

**依赖**：Task C1  
**可并行**：否  
**预计耗时**：5 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

(PLAN.md continues with Stages D through H...)

## 阶段 D：API 层

### Task D1：API 路由 - 添加订阅

**目标**：实现添加订阅的 API 接口

**文件**：
- `src/routers/api.py`（新建）

**实现要点**：
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas import FeedCreate, FeedResponse
from src.services import feed_service

router = APIRouter(prefix="/api", tags=["API"])

@router.post("/feeds", response_model=FeedResponse)
async def add_feed(feed_data: FeedCreate, db: Session = Depends(get_db)):
    """添加订阅源"""
    try:
        feed = await feed_service.create_feed(db, feed_data)
        return feed
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误：{str(e)}")
```

**验证**：
```bash
curl -X POST http://localhost:8000/api/feeds \
  -H "Content-Type: application/json" \
  -d '{"name":"测试","url":"https://www.ruanyifeng.com/blog/atom.xml","tags":"技术"}'
```

**依赖**：Task C1, Task A7  
**可并行**：否  
**预计耗时**：4 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task D2：API 路由 - 获取订阅列表

**目标**：获取所有订阅源

**文件**：
- `src/routers/api.py`（追加）

**实现要点**：
```python
@router.get("/feeds", response_model=list[FeedResponse])
async def list_feeds(db: Session = Depends(get_db)):
    """获取所有订阅源"""
    feeds = feed_service.get_all_feeds(db)
    return feeds
```

**验证**：
```bash
curl http://localhost:8000/api/feeds
```

**依赖**：Task D1  
**可并行**：否  
**预计耗时**：2 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task D3：API 路由 - 删除订阅

**目标**：删除指定订阅源

**文件**：
- `src/routers/api.py`（追加）

**实现要点**：
```python
@router.delete("/feeds/{feed_id}")
async def remove_feed(feed_id: int, db: Session = Depends(get_db)):
    """删除订阅源"""
    try:
        feed_service.delete_feed(db, feed_id)
        return {"success": True, "message": "删除成功"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
```

**验证**：
```bash
curl -X DELETE http://localhost:8000/api/feeds/1
```

**依赖**：Task D1  
**可并行**：否  
**预计耗时**：2 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task D4：API 路由 - 刷新订阅

**目标**：手动触发刷新所有订阅源

**文件**：
- `src/routers/api.py`（追加）

**实现要点**：
```python
from src.services import rss_service

@router.post("/refresh")
async def refresh_feeds(db: Session = Depends(get_db)):
    """刷新所有订阅源"""
    result = await rss_service.refresh_all_feeds(db)
    return {
        "success": True,
        "new_articles": result["new_articles"],
        "success_count": result["success"],
        "failed_count": result["failed"]
    }
```

**验证**：
```bash
curl -X POST http://localhost:8000/api/refresh
```

**依赖**：Task C5  
**可并行**：否  
**预计耗时**：3 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task D5：API 路由 - 获取文章列表

**目标**：获取文章列表（支持按标签筛选）

**文件**：
- `src/routers/api.py`（追加）

**实现要点**：
```python
from src.schemas import ArticleResponse
from src.models import Article, Feed
from datetime import datetime, timedelta
import json

@router.get("/articles", response_model=list[ArticleResponse])
async def list_articles(tag: str = None, db: Session = Depends(get_db)):
    """获取文章列表"""
    # 基础查询：最近 7 天
    cutoff = datetime.utcnow() - timedelta(days=7)
    query = db.query(Article).filter(Article.published_at >= cutoff)
    
    # 按标签筛选
    if tag:
        feeds_with_tag = db.query(Feed).filter(Feed.tags.contains(f'"{tag}"')).all()
        feed_ids = [f.id for f in feeds_with_tag]
        query = query.filter(Article.feed_id.in_(feed_ids))
    
    # 按时间倒序
    articles = query.order_by(Article.published_at.desc()).all()
    
    # 附加 feed_name
    result = []
    for article in articles:
        article_dict = ArticleResponse.from_orm(article).model_dump()
        article_dict['feed_name'] = article.feed.name
        result.append(article_dict)
    
    return result
```

**验证**：
```bash
curl http://localhost:8000/api/articles
curl http://localhost:8000/api/articles?tag=技术
```

**依赖**：Task C4  
**可并行**：否  
**预计耗时**：5 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task D6：注册 API 路由到主应用

**目标**：将 API 路由挂载到 FastAPI 应用

**文件**：
- `src/main.py`（修改）

**实现要点**：
```python
from src.routers import api

# 注册路由
app.include_router(api.router)
```

**验证**：
```bash
curl http://localhost:8000/docs  # 查看自动生成的 API 文档
```

**依赖**：Task D1-D5  
**可并行**：否  
**预计耗时**：2 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

## 阶段 E：前端 UI

### Task E1：创建基础 HTML 模板

**目标**：创建页面基础布局

**文件**：
- `src/templates/base.html`（新建）

**实现要点**：
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}AI-Powered RSS Aggregator{% endblock %}</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <h1 class="logo">📰 RSS Aggregator</h1>
            <ul class="nav-links">
                <li><a href="/">首页</a></li>
                <li><a href="/feeds">订阅管理</a></li>
                <li><button onclick="refreshFeeds()" class="btn-refresh">🔄 刷新</button></li>
            </ul>
        </div>
    </nav>
    
    <main class="container">
        {% block content %}{% endblock %}
    </main>
    
    <script src="/static/js/main.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
```

**验证**：
- 访问任意页面，检查布局

**依赖**：Task A1  
**可并行**：是  
**预计耗时**：4 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task E2：创建 CSS 样式

**目标**：美化页面样式

**文件**：
- `src/static/css/style.css`（新建）

**实现要点**：
```css
:root {
    --primary: #4f46e5;
    --bg: #f9fafb;
    --text: #1f2937;
    --border: #e5e7eb;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: var(--bg);
    color: var(--text);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

.navbar {
    background: white;
    border-bottom: 1px solid var(--border);
    padding: 1rem 0;
}

.nav-links {
    display: flex;
    list-style: none;
    gap: 1.5rem;
    align-items: center;
}

.article-card {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    border: 1px solid var(--border);
}

.article-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.article-title a {
    color: var(--text);
    text-decoration: none;
}

.article-title a:hover {
    color: var(--primary);
}

.article-meta {
    color: #6b7280;
    font-size: 0.875rem;
    margin-bottom: 1rem;
}

.article-summary {
    line-height: 1.6;
    color: #4b5563;
}

.tag {
    display: inline-block;
    background: #e0e7ff;
    color: var(--primary);
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.875rem;
    margin-right: 0.5rem;
}

.btn-refresh {
    background: var(--primary);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
}

.btn-refresh:hover {
    background: #4338ca;
}

/* 响应式 */
@media (max-width: 768px) {
    .article-card {
        padding: 1rem;
    }
}
```

**验证**：
- 刷新页面，检查样式

**依赖**：Task E1  
**可并行**：是  
**预计耗时**：5 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task E3：创建首页 - 文章列表

**目标**：显示文章列表页面

**文件**：
- `src/templates/index.html`（新建）
- `src/routers/web.py`（新建）

**实现要点**：

`src/templates/index.html`:
```html
{% extends "base.html" %}

{% block content %}
<div class="filters">
    <button class="filter-btn active" data-tag="">全部</button>
    {% for tag in tags %}
    <button class="filter-btn" data-tag="{{ tag }}">{{ tag }}</button>
    {% endfor %}
</div>

<div id="articles-container">
    {% for article in articles %}
    <div class="article-card">
        <h2 class="article-title">
            <a href="{{ article.link }}" target="_blank">{{ article.title }}</a>
        </h2>
        <div class="article-meta">
            <span class="tag">{{ article.feed_name }}</span>
            <span>{{ article.published_at|format_time }}</span>
        </div>
        <div class="article-summary">
            {% if article.summary %}
                {{ article.summary }}
            {% else %}
                <em>加载摘要中...</em>
            {% endif %}
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

`src/routers/web.py`:
```python
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.main import templates
from src.models import Article, Feed
from datetime import datetime, timedelta
import json

router = APIRouter(tags=["Web"])

@router.get("/")
async def index(request: Request, tag: str = None, db: Session = Depends(get_db)):
    """首页"""
    # 获取所有标签
    feeds = db.query(Feed).all()
    all_tags = set()
    for feed in feeds:
        tags_list = json.loads(feed.tags) if feed.tags else []
        all_tags.update(tags_list)
    
    # 获取文章
    cutoff = datetime.utcnow() - timedelta(days=7)
    query = db.query(Article).filter(Article.published_at >= cutoff)
    
    if tag:
        feeds_with_tag = db.query(Feed).filter(Feed.tags.contains(f'"{tag}"')).all()
        feed_ids = [f.id for f in feeds_with_tag]
        query = query.filter(Article.feed_id.in_(feed_ids))
    
    articles = query.order_by(Article.published_at.desc()).limit(50).all()
    
    # 为未生成摘要的文章生成摘要（异步）
    from src.services import summary_service
    for article in articles:
        if article.summary_status == 'pending':
            await summary_service.generate_article_summary(db, article)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "articles": articles,
        "tags": sorted(all_tags),
        "current_tag": tag
    })
```

**验证**：
- 访问 http://localhost:8000

**依赖**：Task E1, Task C7  
**可并行**：否  
**预计耗时**：8 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task E4：创建订阅管理页面

**目标**：订阅源的增删改查界面

**文件**：
- `src/templates/feeds.html`（新建）
- `src/routers/web.py`（追加）

**实现要点**：

`src/templates/feeds.html`:
```html
{% extends "base.html" %}

{% block content %}
<h2>订阅管理</h2>

<div class="add-feed-form">
    <h3>添加订阅</h3>
    <form id="addFeedForm">
        <input type="text" id="feedUrl" placeholder="RSS URL 或网站 URL" required>
        <input type="text" id="feedTags" placeholder="标签（逗号分隔）">
        <button type="submit">添加</button>
    </form>
</div>

<div class="feeds-list">
    <h3>订阅列表 ({{ feeds|length }})</h3>
    {% for feed in feeds %}
    <div class="feed-item">
        <div class="feed-info">
            <h4>{{ feed.name }}</h4>
            <p>{{ feed.url }}</p>
            <div class="feed-tags">
                {% for tag in feed.tags|from_json %}
                <span class="tag">{{ tag }}</span>
                {% endfor %}
            </div>
        </div>
        <button onclick="deleteFeed({{ feed.id }})" class="btn-delete">删除</button>
    </div>
    {% endfor %}
</div>
{% endblock %}

{% block scripts %}
<script>
document.getElementById('addFeedForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const url = document.getElementById('feedUrl').value;
    const tags = document.getElementById('feedTags').value;
    
    const response = await fetch('/api/feeds', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({url, tags})
    });
    
    if (response.ok) {
        location.reload();
    } else {
        const error = await response.json();
        alert('添加失败：' + error.detail);
    }
});

async function deleteFeed(id) {
    if (!confirm('确定删除该订阅源吗？')) return;
    
    const response = await fetch(`/api/feeds/${id}`, {method: 'DELETE'});
    if (response.ok) {
        location.reload();
    }
}
</script>
{% endblock %}
```

`src/routers/web.py`:
```python
@router.get("/feeds")
async def feeds_page(request: Request, db: Session = Depends(get_db)):
    """订阅管理页面"""
    from src.services import feed_service
    feeds = feed_service.get_all_feeds(db)
    return templates.TemplateResponse("feeds.html", {
        "request": request,
        "feeds": feeds
    })
```

**验证**：
- 访问 http://localhost:8000/feeds

**依赖**：Task E1, Task D1  
**可并行**：否  
**预计耗时**：8 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task E5：创建 JavaScript 交互

**目标**：实现前端交互逻辑

**文件**：
- `src/static/js/main.js`（新建）

**实现要点**：
```javascript
// 刷新所有订阅源
async function refreshFeeds() {
    const btn = event.target;
    btn.disabled = true;
    btn.textContent = '⏳ 刷新中...';
    
    try {
        const response = await fetch('/api/refresh', {method: 'POST'});
        const result = await response.json();
        
        if (result.success) {
            alert(`刷新完成！新增 ${result.new_articles} 篇文章`);
            location.reload();
        }
    } catch (error) {
        alert('刷新失败：' + error.message);
    } finally {
        btn.disabled = false;
        btn.textContent = '🔄 刷新';
    }
}

// 标签筛选
document.addEventListener('DOMContentLoaded', () => {
    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tag = btn.dataset.tag;
            const url = tag ? `/?tag=${encodeURIComponent(tag)}` : '/';
            window.location.href = url;
        });
    });
});

// 相对时间格式化
function formatTime(datetime) {
    const now = new Date();
    const past = new Date(datetime);
    const diff = Math.floor((now - past) / 1000);
    
    if (diff < 60) return '刚刚';
    if (diff < 3600) return `${Math.floor(diff / 60)} 分钟前`;
    if (diff < 86400) return `${Math.floor(diff / 3600)} 小时前`;
    if (diff < 604800) return `${Math.floor(diff / 86400)} 天前`;
    return past.toLocaleDateString();
}
```

**验证**：
- 测试刷新按钮
- 测试标签筛选

**依赖**：Task E3  
**可并行**：否  
**预计耗时**：4 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task E6：注册 Web 路由

**目标**：将 Web 路由挂载到主应用

**文件**：
- `src/main.py`（修改）

**实现要点**：
```python
from src.routers import web

app.include_router(web.router)
```

**验证**：
- 访问所有页面，确保路由正常

**依赖**：Task E3, Task E4  
**可并行**：否  
**预计耗时**：2 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

## 阶段 F：后台任务

### Task F1：后台定时抓取任务

**目标**：每小时自动抓取 RSS

**文件**：
- `src/background_tasks.py`（新建）

**实现要点**：
```python
import asyncio
from src.database import SessionLocal
from src.services import rss_service
from src.config import logger

async def background_fetch_task():
    """后台定时抓取任务"""
    logger.info("启动后台抓取任务")
    
    while True:
        try:
            logger.info("开始抓取 RSS...")
            db = SessionLocal()
            await rss_service.refresh_all_feeds(db)
            db.close()
            logger.info("抓取完成，等待 1 小时")
        except Exception as e:
            logger.error(f"后台抓取失败：{str(e)}")
        
        # 等待 1 小时
        await asyncio.sleep(3600)
```

**验证**：
- 启动应用，观察日志

**依赖**：Task C5  
**可并行**：否  
**预计耗时**：3 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task F2：后台定时清理任务

**目标**：每天凌晨清理旧文章

**文件**：
- `src/background_tasks.py`（追加）

**实现要点**：
```python
from src.services import cleanup_service
from datetime import datetime

async def background_cleanup_task():
    """后台定时清理任务"""
    logger.info("启动后台清理任务")
    
    while True:
        try:
            # 等到凌晨 3 点
            now = datetime.now()
            target = now.replace(hour=3, minute=0, second=0, microsecond=0)
            if target < now:
                target = target + timedelta(days=1)
            
            wait_seconds = (target - now).total_seconds()
            logger.info(f"等待 {wait_seconds/3600:.1f} 小时后执行清理")
            await asyncio.sleep(wait_seconds)
            
            # 执行清理
            logger.info("开始清理旧文章...")
            db = SessionLocal()
            cleanup_service.cleanup_old_articles(db)
            db.close()
            
        except Exception as e:
            logger.error(f"后台清理失败：{str(e)}")
            await asyncio.sleep(3600)  # 失败后 1 小时重试
```

**验证**：
- 单元测试

**依赖**：Task C8  
**可并行**：否  
**预计耗时**：4 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task F3：启动后台任务

**目标**：在应用启动时启动后台任务

**文件**：
- `src/main.py`（修改）

**实现要点**：
```python
from src.background_tasks import background_fetch_task, background_cleanup_task

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    from src.database import init_db
    init_db()
    logger.info("✓ 数据库初始化完成")
    
    # 启动后台任务
    asyncio.create_task(background_fetch_task())
    asyncio.create_task(background_cleanup_task())
    logger.info("✓ 后台任务已启动")
```

**验证**：
- 启动应用，检查日志

**依赖**：Task F1, Task F2  
**可并行**：否  
**预计耗时**：2 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

## 阶段 G：测试

### Task G1：订阅管理服务单元测试

**目标**：测试订阅的增删改查

**文件**：
- `tests/test_feed_service.py`（新建）

**实现要点**：
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base, Feed
from src.services import feed_service
from src.schemas import FeedCreate

@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.mark.asyncio
async def test_create_feed(db):
    feed_data = FeedCreate(
        name="测试订阅",
        url="https://www.ruanyifeng.com/blog/atom.xml",
        tags="技术,博客"
    )
    feed = await feed_service.create_feed(db, feed_data)
    assert feed.id is not None
    assert feed.name == "测试订阅"

def test_delete_feed(db):
    # 创建测试数据
    feed = Feed(name="测试", url="http://test.com/rss", tags='["技术"]')
    db.add(feed)
    db.commit()
    
    # 删除
    feed_service.delete_feed(db, feed.id)
    assert db.query(Feed).filter(Feed.id == feed.id).first() is None
```

**验证**：
```bash
pytest tests/test_feed_service.py -v
```

**依赖**：Task C1-C3  
**可并行**：否  
**预计耗时**：6 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task G2：RSS 抓取服务单元测试

**目标**：测试 RSS 抓取逻辑

**文件**：
- `tests/test_rss_service.py`（新建）

**实现要点**：
```python
import pytest
from src.services import rss_service
from src.models import Feed
from unittest.mock import Mock, patch

@pytest.mark.asyncio
async def test_fetch_rss_content():
    mock_response = """<?xml version="1.0"?>
    <rss version="2.0">
      <channel>
        <item>
          <title>Test Article</title>
          <link>http://example.com/1</link>
          <pubDate>Mon, 13 Aug 2026 12:00:00 GMT</pubDate>
        </item>
      </channel>
    </rss>"""
    
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value.text = mock_response
        mock_get.return_value.raise_for_status = Mock()
        
        result = await rss_service.fetch_rss_content("http://test.com/rss")
        assert len(result.entries) > 0
```

**验证**：
```bash
pytest tests/test_rss_service.py -v
```

**依赖**：Task C4  
**可并行**：是  
**预计耗时**：5 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task G3：AI 摘要服务单元测试

**目标**：测试摘要生成（Mock OpenAI）

**文件**：
- `tests/test_summary_service.py`（新建）

**实现要点**：
```python
import pytest
from src.services import summary_service
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_generate_summary():
    with patch('src.services.summary_service.client.chat.completions.create') as mock_create:
        mock_create.return_value = AsyncMock(
            choices=[AsyncMock(message=AsyncMock(content="这是测试摘要"))]
        )
        
        success, summary = await summary_service.generate_summary("测试内容")
        assert success is True
        assert "测试摘要" in summary
```

**验证**：
```bash
pytest tests/test_summary_service.py -v
```

**依赖**：Task C6  
**可并行**：是  
**预计耗时**：4 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task G4：集成测试与覆盖率

**目标**：运行所有测试并生成覆盖率报告

**文件**：
- `pytest.ini`（新建）

**实现要点**：
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
```

**验证**：
```bash
pytest tests/ --cov=src --cov-report=html
# 查看 htmlcov/index.html
```

**依赖**：Task G1-G3  
**可并行**：否  
**预计耗时**：3 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

## 阶段 H：部署

### Task H1：创建 Dockerfile 和 docker-compose.yml

**目标**：容器化部署

**文件**：
- `Dockerfile`（新建）
- `docker-compose.yml`（新建）

**实现要点**：

`Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY src/ ./src/
COPY scripts/ ./scripts/

# 创建必要目录
RUN mkdir -p data logs

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

`docker-compose.yml`:
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=sqlite:///./data/rss_aggregator.db
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
```

**验证**：
```bash
docker-compose up --build
curl http://localhost:8000/health
```

**依赖**：所有核心功能完成  
**可并行**：否  
**预计耗时**：5 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

### Task H2：部署到 Render/Railway

**目标**：线上部署，提供公网 URL

**文件**：
- `render.yaml`（新建，如使用 Render）

**实现要点**：

`render.yaml`:
```yaml
services:
  - type: web
    name: rss-aggregator
    env: docker
    plan: free
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: PORT
        value: 8000
```

**部署步骤**：
1. 推送代码到 GitHub
2. 在 Render/Railway 创建新服务
3. 连接 GitHub 仓库
4. 设置环境变量（OPENAI_API_KEY）
5. 部署

**验证**：
- 访问公网 URL
- 测试所有功能

**依赖**：Task H1  
**可并行**：否  
**预计耗时**：10 分钟  
**状态**：⬜ 未开始  
**Commit**：-

---

## 📊 任务依赖图

```
A1 → A5 → A6 → A7 ─┐
A2 ─┘     │    │    │
A3 ─┘     │    │    │
A4 ───────┘    │    │
               │    ├─→ D1 → D2 → D3 → D4 → D5 → D6 ─┐
B1 → B2 → B4   │    │                                 │
B1 → B3        │    │                                 │
B2 → B5        │    │                                 ├─→ E6 → F3
               │    │                                 │
C1 → C2        │    │                                 │
C1 → C3        │    │                                 │
C1 → C4 → C5 ──┘    │                                 │
C6 → C7 ────────────┘                                 │
C1 → C9                                               │
C8 (独立)                                             │
                                                      │
E1 → E2 → E3 ───────────────────────────────────────┤
E1 → E4 ────────────────────────────────────────────┤
E3 → E5 ────────────────────────────────────────────┘

F1 ─┐
F2 ─┴→ F3

G1, G2, G3 → G4

H1 → H2
```

---

## 🎯 里程碑

| 里程碑 | 完成标准 | 预计日期 |
|--------|---------|---------|
| **M1: 基础设施完成** | 阶段 A 全部完成，应用可启动 | Day 1 |
| **M2: 数据层完成** | 阶段 B 全部完成，数据库可用 | Day 2 |
| **M3: 核心服务完成** | 阶段 C 全部完成，业务逻辑可用 | Day 5 |
| **M4: API 完成** | 阶段 D 全部完成，接口可调用 | Day 6 |
| **M5: UI 完成** | 阶段 E 全部完成，页面可访问 | Day 8 |
| **M6: 后台任务完成** | 阶段 F 全部完成，自动化运行 | Day 9 |
| **M7: 测试完成** | 阶段 G 全部完成，覆盖率 >70% | Day 11 |
| **M8: 部署完成** | 阶段 H 全部完成，公网可访问 | Day 14 |

---

## 📝 更新记录

每完成一个 task，更新状态为 ✅，并记录 commit hash。

**示例**：
```
Task A1: ✅ 已完成 (commit: abc1234)
```

---

**文档状态**：✅ 已完成  
**最后更新**：2026-08-13  
**下一步**：冷启动验证
