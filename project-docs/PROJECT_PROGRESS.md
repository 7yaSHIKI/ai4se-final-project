# 项目进度跟踪

> **最后更新**：2026-08-13  
> **项目方向**：B - 应用类项目  
> **当前阶段**：阶段 0 - 准备与环境搭建

---

## 📊 总体进度

```
[████████░░░░░░░░░░░░] 40% 完成

阶段 0: 准备与环境搭建       [██████████] 100% ✅
阶段 1: Brainstorming        [████████░░]  80%
阶段 2: Writing Plans        [░░░░░░░░░░]  0%
阶段 3: 冷启动验证           [░░░░░░░░░░]  0%
阶段 4: 实现工作流           [░░░░░░░░░░]  0%
阶段 5: 测试与 CI/CD         [░░░░░░░░░░]  0%
阶段 6: 分发与部署           [░░░░░░░░░░]  0%
阶段 7: 反思报告             [░░░░░░░░░░]  0%
```

---

## ✅ 已完成内容

### 阶段 0：准备与环境搭建（✅ 100% 完成）

- [x] 创建项目文档目录结构 (`project-docs/`)
- [x] 合并通用要求和 B 方向要求为完整指南 (`PROJECT_GUIDE_B.md`)
- [x] 创建项目进度跟踪文档 (`PROJECT_PROGRESS.md`)
- [x] 创建交付物检查清单 (`DELIVERABLES_CHECKLIST.md`)
- [x] 安装 Superpowers 插件到 Claude Code（技能已复制到 `.claude/skills/`）
- [x] 创建 GitHub 公开仓库（https://github.com/7yaSHIKI/ai4se-final-project）
- [x] 克隆仓库到本地
- [x] 首次提交并推送到 GitHub（commit: 7ef6b6a）
- [ ] 确定最终项目选题
- [ ] 阅读 Superpowers 文档和示例

---

## 📋 当前任务

### 项目选题已确定 ✅

**项目名称**：RSS 聚合器 + AI 摘要  
**英文名称**：AI-Powered RSS Aggregator  
**30秒说明**：订阅多个信息源（博客、新闻），AI 自动生成摘要，在统一界面查看，节省阅读时间，精准获取信息。

**核心功能模块（3个）**：
1. **订阅管理**：添加/删除/查看 RSS 订阅源，分类管理
2. **内容抓取与 AI 摘要**：定时抓取 RSS，调用 LLM 生成摘要，去重存储
3. **WebUI 展示**：文章列表、摘要显示、筛选、标记已读

**技术栈初步方案**：
- 后端：Python + FastAPI
- RSS 解析：feedparser
- LLM：OpenAI API
- 存储：SQLite 或 JSON
- 前端：HTML + CSS + JavaScript（或 Jinja2 模板）
- 部署：Docker

---

### 立即执行（今天）

**🎯 阶段 1：Brainstorming - 需求分析与设计**

我将按照 Superpowers brainstorming 技能的要求，通过提问来帮你完善：

---

## 🎯 接下来需要完成的内容

### 本周目标（Week 1）

#### 阶段 1：Brainstorming（2-3 天）
- [ ] 触发 `/brainstorming` 技能
- [ ] 与 AI 协作明确项目需求
- [ ] 定义用户故事（至少 5 个）
- [ ] 设计系统架构
- [ ] 确定技术栈
- [ ] 完成 `SPEC.md`
- [ ] 记录过程到 `SPEC_PROCESS.md`

#### 阶段 2：Writing Plans（1-2 天）
- [ ] 触发 `/writing-plans` 技能
- [ ] 将设计分解为 task 列表（每个 2-5 分钟）
- [ ] 标注 task 依赖关系
- [ ] 标注可并行部分
- [ ] 完成 `PLAN.md`

#### 阶段 3：冷启动验证（1 天）
- [ ] 选择不同的 AI agent（Cursor/GitHub Copilot CLI）
- [ ] 启动全新 session（不导入历史）
- [ ] 仅提供 SPEC.md + PLAN.md
- [ ] 让其实现 1-2 个 task
- [ ] 记录暴露的 spec 缺陷
- [ ] 修订 SPEC 和 PLAN
- [ ] 更新 `SPEC_PROCESS.md`

### 第二周目标（Week 2）

#### 阶段 4：实现工作流（7-10 天）
- [ ] 触发 `/using-git-worktrees` 创建工作区
- [ ] 按 PLAN 执行 task（使用 subagent）
- [ ] 严格遵循 TDD（红-绿-重构）
- [ ] 每个 task 完成后进行两阶段评审
- [ ] 持续更新 `AGENT_LOG.md`
- [ ] 持续更新 `PLAN.md`（标记完成状态）
- [ ] 为每个功能模块创建 PR

### 第三周目标（Week 3）

#### 阶段 5：测试与 CI/CD（1-2 天）
- [ ] 编写单元测试和集成测试
- [ ] 配置 GitHub Actions
- [ ] 确保 unit-test job 通过
- [ ] 确保测试覆盖率 >70%

#### 阶段 6：分发与部署（1-2 天）
- [ ] 编写 Dockerfile 和 docker-compose.yml
- [ ] 构建并推送 Docker 镜像
- [ ] 部署到线上（Render/Railway/Fly.io）
- [ ] 完善 README.md
- [ ] 提供公网可访问的 WebUI

#### 阶段 7：反思报告（1-2 天）
- [ ] 撰写 `REFLECTION.md`（1500-2500 字）
- [ ] 回答所有必答问题
- [ ] 诚实反思 Superpowers 工作流

---

## 🚧 当前阻塞项

**无阻塞项**

---

## 📝 重要决策记录

### 2026-08-13

- **决策**：选择 B 方向（应用类项目）
- **理由**：相比 A 方向（Coding Agent Harness）更简单、更容易上手，技术栈更灵活
- **影响**：无需实现完整的 agent harness 内核，无需 mock LLM 单元测试

- **安装**：Superpowers 插件安装完成
- **方法**：由于 VS Code 扩展环境中 `/plugin` 命令不可用，采用手动克隆方式
- **步骤**：
  1. 克隆 Superpowers 仓库到 `~/.claude/plugins/marketplaces/superpowers/`
  2. 更新 `~/.claude/plugins/known_marketplaces.json` 添加 superpowers 配置
  3. 确认插件配置文件存在 (`.claude-plugin/plugin.json`)
- **结果**：技能已复制到项目 `.claude/skills/` 目录

- **GitHub 仓库创建**：https://github.com/7yaSHIKI/ai4se-final-project
- **首次提交**：commit 7ef6b6a
  - 添加 Superpowers 技能（55 个文件）
  - 添加项目文档（PROJECT_GUIDE_B.md, PROJECT_PROGRESS.md, DELIVERABLES_CHECKLIST.md）
  - 添加 CLAUDE.md 工作流指南
- **推送成功**：所有文件已同步到 GitHub

---

## ⚠️ 风险与注意事项

### 高风险项
1. **选题太大，做不完** → 从 MVP 开始，逐步迭代
2. **冷启动验证失败** → SPEC 不够清晰，需要大幅修订
3. **LLM API 成本** → 开发阶段频繁调用
4. **凭据泄露到 Git** → 严重违规
5. **CI 最后一次不是 pass** → 不满足交付要求

### 缓解措施
- 严格遵循冷启动验证流程
- 使用 `.gitignore` 排除敏感文件
- 提交前使用 `git-secrets` 扫描
- 留出足够的 buffer 时间修复 CI

---

## 📈 时间规划

| 阶段 | 预计耗时 | 开始日期 | 结束日期 | 状态 |
|------|---------|---------|---------|------|
| 阶段 0：准备 | 1 天 | 2026-08-13 | 2026-08-13 | 🟡 进行中 |
| 阶段 1：Brainstorming | 2-3 天 | TBD | TBD | ⚪ 未开始 |
| 阶段 2：Writing Plans | 1-2 天 | TBD | TBD | ⚪ 未开始 |
| 阶段 3：冷启动验证 | 1 天 | TBD | TBD | ⚪ 未开始 |
| 阶段 4：实现工作流 | 7-10 天 | TBD | TBD | ⚪ 未开始 |
| 阶段 5：测试与 CI/CD | 1-2 天 | TBD | TBD | ⚪ 未开始 |
| 阶段 6：分发与部署 | 1-2 天 | TBD | TBD | ⚪ 未开始 |
| 阶段 7：反思报告 | 1-2 天 | TBD | TBD | ⚪ 未开始 |
| **总计** | **14-21 天** | 2026-08-13 | TBD | 🟡 20% |

---

## 📌 下一步行动

### 今天必须完成
1. ✅ 安装 Superpowers 插件
2. ✅ 创建 GitHub 仓库
3. ✅ 确定项目选题

### 明天开始
4. 🚀 启动 `/brainstorming` 技能
5. 🚀 开始编写 `SPEC.md`

---

## 💡 学习与反思

### 经验教训
- （待记录）

### 最佳实践
- （待记录）

### 待改进项
- （待记录）
