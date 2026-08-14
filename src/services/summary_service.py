"""
AI 摘要生成服务
使用 OpenAI API 生成文章摘要
"""
from openai import AsyncOpenAI
from sqlalchemy.orm import Session
from src.models import Article
from src.config import settings, logger
from typing import Tuple
import re


# 初始化 OpenAI 客户端
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


def strip_html_tags(text: str) -> str:
    """移除 HTML 标签"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


async def generate_summary(content: str, title: str = "") -> Tuple[bool, str]:
    """
    调用 OpenAI API 生成摘要

    Args:
        content: 文章内容
        title: 文章标题（可选）

    Returns:
        (成功状态, 摘要文本或错误信息)
    """
    try:
        # 清理 HTML 标签
        clean_content = strip_html_tags(content)

        # 截取前 2000 字符（控制成本）
        clean_content = clean_content[:2000]

        # 构建提示词
        prompt = f"请用 100-200 字总结以下文章的核心内容：\n\n标题：{title}\n\n内容：{clean_content}"

        # 调用 OpenAI API
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是一个专业的内容总结助手，擅长提取文章核心信息。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )

        summary = response.choices[0].message.content.strip()
        logger.info(f"✓ 摘要生成成功（{len(summary)} 字）")
        return True, summary

    except Exception as e:
        error_msg = f"LLM 调用失败: {str(e)}"
        logger.error(error_msg)
        return False, error_msg


async def generate_article_summary(db: Session, article: Article, retry_count: int = 3) -> bool:
    """
    为单篇文章生成摘要并保存

    Args:
        db: 数据库会话
        article: Article 对象
        retry_count: 重试次数

    Returns:
        是否成功
    """
    # 如果已有摘要，跳过
    if article.summary_status == 'success':
        return True

    # 如果没有内容，标记失败
    if not article.content or len(article.content.strip()) < 50:
        article.summary_status = 'failed'
        article.summary = "内容过短，无法生成摘要"
        db.commit()
        return False

    # 重试机制
    for attempt in range(retry_count):
        success, result = await generate_summary(article.content, article.title)

        if success:
            article.summary = result
            article.summary_status = 'success'
            db.commit()
            logger.info(f"✓ 文章摘要生成成功: {article.title[:30]}...")
            return True
        else:
            if attempt < retry_count - 1:
                logger.warning(f"重试 {attempt + 1}/{retry_count}: {article.title[:30]}...")
            else:
                # 最后一次失败，显示原文前 200 字
                article.summary_status = 'failed'
                clean_content = strip_html_tags(article.content)[:200]
                article.summary = f"⚠️ LLM 调用失败，显示原文前 200 字：\n\n{clean_content}..."
                db.commit()
                logger.error(f"✗ 文章摘要生成失败（已重试 {retry_count} 次）: {article.title[:30]}...")
                return False

    return False


async def batch_generate_summaries(db: Session, limit: int = 10) -> int:
    """
    批量生成待处理文章的摘要

    Args:
        db: 数据库会话
        limit: 每次处理数量

    Returns:
        成功生成的数量
    """
    # 查询待处理的文章
    pending_articles = db.query(Article).filter(
        Article.summary_status == 'pending'
    ).limit(limit).all()

    if not pending_articles:
        logger.info("没有待生成摘要的文章")
        return 0

    logger.info(f"开始批量生成摘要，共 {len(pending_articles)} 篇...")

    success_count = 0
    for article in pending_articles:
        if await generate_article_summary(db, article):
            success_count += 1

    logger.info(f"✓ 批量摘要生成完成：成功 {success_count}/{len(pending_articles)}")
    return success_count
