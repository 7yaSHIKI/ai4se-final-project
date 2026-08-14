from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.config import settings, logger
from src.database import init_db
from src.routers import api
import asyncio

# 创建 FastAPI 应用
app = FastAPI(
    title="AI-Powered RSS Aggregator",
    description="订阅多个信息源，AI 自动生成摘要，统一界面查看",
    version="1.0.0"
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# 配置模板
templates = Jinja2Templates(directory="src/templates")

# 注册 API 路由
app.include_router(api.router)


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    init_db()
    logger.info("✓ 数据库初始化完成")
    logger.info(f"✓ 应用启动成功，监听端口 {settings.PORT}")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("应用已关闭")


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "service": "rss-aggregator",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True
    )