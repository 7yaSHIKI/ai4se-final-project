# AI-Powered RSS Aggregator

> AI4SE 期末项目（B 方向 - 应用类项目）

订阅多个信息源（博客、新闻），AI 自动生成摘要，在统一界面查看，节省阅读时间，精准获取信息。

## 🌐 在线演示

**线上地址**：https://ai4se-final-project.onrender.com

> 注意：Free tier 实例会在闲置后休眠，首次访问可能需要等待 50 秒唤醒

## ✨ 功能特性

- 📰 **订阅管理**：添加/删除 RSS 订阅源，支持自定义标签
- 🤖 **AI 摘要**：使用 DeepSeek API 自动生成 100-200 字中文摘要
- 🏷️ **标签筛选**：按标签分类查看文章
- 🔄 **自动刷新**：每小时自动抓取新文章
- 🗑️ **自动清理**：保留最近 7 天文章，自动删除过期内容
- 📱 **响应式设计**：支持桌面端和移动端

## 🛠️ 技术栈

- **后端**：FastAPI 0.104.1 + Python 3.11
- **数据库**：SQLite + SQLAlchemy 2.0
- **AI**：DeepSeek API (deepseek-chat)
- **RSS 解析**：feedparser 6.0.10
- **前端**：原生 HTML/CSS/JavaScript + Jinja2
- **部署**：Docker + Render

## 📦 快速开始

### 本地开发

1. **克隆项目**

```bash
git clone https://github.com/7yaSHIKI/ai4se-final-project.git
cd ai4se-final-project
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

3. **配置环境变量**

复制 `.env.example` 为 `.env`，填入你的 DeepSeek API Key：

```bash
cp .env.example .env
# 编辑 .env 文件，填入：OPENAI_API_KEY=your_deepseek_api_key_here
```

> 注意：虽然变量名为 OPENAI_API_KEY，但应填入 DeepSeek API Key

4. **初始化数据库**

```bash
python scripts/init_db.py
```

5. **启动应用**

```bash
python -m uvicorn src.main:app --reload
```

访问 http://localhost:8000

### Docker 部署

1. **构建镜像**

```bash
docker-compose build
```

2. **启动容器**

```bash
# 设置环境变量
export OPENAI_API_KEY=your_api_key_here

docker-compose up -d
```

3. **查看日志**

```bash
docker-compose logs -f
```

## 🧪 运行测试

```bash
# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=src --cov-report=html

# 查看覆盖率报告
open htmlcov/index.html
```

## 📚 API 文档

启动应用后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 主要接口

- `POST /api/feeds` - 添加订阅
- `GET /api/feeds` - 获取订阅列表
- `DELETE /api/feeds/{id}` - 删除订阅
- `POST /api/refresh` - 手动刷新所有订阅
- `GET /api/articles` - 获取文章列表（支持标签筛选）

## 🚀 部署到 Render

1. **推送代码到 GitHub**

```bash
git push origin main
```

2. **在 Render 创建服务**

- 访问 https://render.com
- 点击 "New +" → "Web Service"
- 连接 GitHub 仓库
- 选择 `ai4se-final-project`
- Render 会自动检测 `render.yaml`

3. **设置环境变量**

在 Render 控制台添加环境变量：
- `OPENAI_API_KEY`: 你的 DeepSeek API Key（从 https://platform.deepseek.com 获取）

4. **部署**

点击 "Create Web Service"，等待部署完成。

## ⚠️ 安全提示

**重要：本项目为个人使用设计，存在以下安全限制：**

1. **凭据管理**：使用明文 `.env` 文件存储 API Key，仅适用于个人项目
2. **无身份验证**：无用户登录系统，任何人访问 URL 都能使用
3. **不适用于生产环境**：请勿在公开服务器部署或存储敏感数据

**生产环境建议**：
- 使用密钥管理服务（如 AWS Secrets Manager）
- 添加用户认证系统（OAuth 2.0）
- 启用 HTTPS
- 实现 API 限流

## 💰 成本估算

使用 DeepSeek API (deepseek-chat)：
- 输入（缓存未命中）：$0.22 / 1M tokens
- 输出：$0.66 / 1M tokens

**月度成本**（50 篇文章/天）：
- 输入：~30,000 tokens/月 = $0.0066
- 输出：~150,000 tokens/月 = $0.099
- **总计**：~$0.11/月

> 比 OpenAI GPT-4o-mini 更经济实惠

## 📖 项目文档

- [完整设计规格](SPEC.md)
- [实现计划](PLAN.md)
- [规格制定过程](SPEC_PROCESS.md)
- [冷启动验证报告](project-docs/COLD_START_VALIDATION.md)
- [项目进度跟踪](project-docs/PROJECT_PROGRESS.md)

## 📄 许可证

MIT License

## 👨‍💻 作者

7yaSHIKI - AI4SE 期末项目

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代 Python Web 框架
- [DeepSeek](https://www.deepseek.com/) - AI 摘要生成
- [feedparser](https://feedparser.readthedocs.io/) - RSS 解析
- [Superpowers](https://github.com/cline/superpowers) - 开发方法论
