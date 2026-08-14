# 部署指南

## 📋 当前状态

- ✅ 代码已推送到 GitHub
- ✅ Docker 配置完成
- ⏳ CI/CD 配置待添加（需要 workflow 权限的 token）
- ⏳ 线上部署待完成

## 🚀 部署步骤

### 1. 添加 GitHub Actions CI/CD（手动）

由于当前 token 缺少 `workflow` 权限，需要在 GitHub 网页上手动添加：

1. 访问：https://github.com/7yaSHIKI/ai4se-final-project
2. 点击 "Add file" → "Create new file"
3. 文件路径：`.github/workflows/ci.yml`
4. 复制 `/home/seiha/Courses/AI4SE/ai4se-final-project/.github/workflows/ci.yml` 的内容
5. Commit 并 push

### 2. 部署到 Render

#### 步骤 A：创建 Web Service

1. 访问 https://render.com
2. 点击 "New +" → "Web Service"
3. 选择 "Deploy from a Git repository"
4. 连接 GitHub 账户并授权
5. 选择仓库：`7yaSHIKI/ai4se-final-project`

#### 步骤 B：配置服务

- **Name**: `rss-aggregator`
- **Region**: Singapore
- **Branch**: `main`
- **Runtime**: Docker
- **Instance Type**: Free

#### 步骤 C：设置环境变量

在 "Environment Variables" 中添加：

```
OPENAI_API_KEY=你的真实OpenAI API Key
PORT=8000
DATABASE_URL=sqlite:///./data/rss_aggregator.db
LOG_LEVEL=INFO
RSS_FETCH_INTERVAL=3600
ARTICLE_RETENTION_DAYS=7
```

**重要**：`OPENAI_API_KEY` 必须填写真实的 API Key

#### 步骤 D：部署

1. 点击 "Create Web Service"
2. 等待构建和部署（约 5-10 分钟）
3. 部署成功后会获得公网 URL：`https://rss-aggregator-xxxx.onrender.com`

#### 步骤 E：验证部署

访问以下 URL 验证：
- 健康检查：`https://你的URL/health`
- 首页：`https://你的URL/`
- API 文档：`https://你的URL/docs`

### 3. 使用应用

1. 访问首页
2. 点击 "订阅管理"
3. 添加 RSS 订阅源（推荐测试源）：
   ```
   名称：阮一峰的网络日志
   URL：https://www.ruanyifeng.com/blog/atom.xml
   标签：技术,博客
   ```
4. 点击 "🔄 刷新" 抓取文章
5. 返回首页查看文章和 AI 摘要

## ⚠️ 注意事项

### Render 免费计划限制

- 15 分钟无活动后会休眠
- 首次访问需要等待唤醒（约 30 秒）
- 每月 750 小时免费运行时间
- SQLite 数据库在重新部署时会丢失

### 数据持久化

Render 免费计划不支持持久化存储，有以下解决方案：

**方案 1（推荐）**：使用 PostgreSQL
- 在 Render 创建 PostgreSQL 数据库（免费）
- 修改 `DATABASE_URL` 为 PostgreSQL 连接串
- 修改代码支持 PostgreSQL（SQLAlchemy 已兼容）

**方案 2**：接受数据丢失
- 每次重新部署会清空数据
- 适合演示和测试

**方案 3**：升级到付费计划
- 提供持久化磁盘存储
- 每月 $7 起

## 📊 成本估算

### OpenAI API 成本

使用 gpt-4o-mini：
- 输入：$0.150 / 1M tokens
- 输出：$0.600 / 1M tokens

**月度成本**（50 篇文章/天）：
- 输入：~30,000 tokens = $0.0045
- 输出：~150,000 tokens = $0.09
- **总计**：~$0.10/月

### Render 成本

- 免费计划：$0/月
- Starter 计划（推荐）：$7/月（包含持久化存储）

## 🔗 相关链接

- GitHub 仓库：https://github.com/7yaSHIKI/ai4se-final-project
- Render 部署：待添加
- CI/CD 状态：待添加

## ✅ 提交前检查清单

- [x] 代码已推送到 GitHub
- [x] Docker 配置完成
- [ ] GitHub Actions CI/CD 已添加
- [ ] CI/CD 执行成功（绿色✓）
- [ ] 已部署到 Render
- [ ] 公网 URL 可访问
- [ ] WebUI 功能正常
- [ ] 更新 README.md 添加部署 URL
- [ ] 截图保存 CI/CD 执行记录
