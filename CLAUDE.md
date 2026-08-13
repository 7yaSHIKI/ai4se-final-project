# AI4SE Final Project - Superpowers Workflow

> 本项目严格遵循 Superpowers 方法论完成 AI4SE 期末项目（B 方向 - 应用类项目）

## 项目指南

完整的项目要求请参考：[PROJECT_GUIDE_B.md](project-docs/PROJECT_GUIDE_B.md)

## Superpowers 工作流

本项目必须按照以下 Superpowers 七步工作流执行：

### 1. Brainstorming（需求分析与设计）
- **触发时机**：项目开始，在编写任何代码之前
- **目标**：通过提问细化需求，生成清晰的 SPEC.md
- **技能位置**：`.claude/skills/brainstorming/`
- **关键活动**：
  - 追问"你究竟想做什么"
  - 分块呈现设计供逐步签字确认
  - 生成用户故事（至少 5 个）
  - 定义系统架构、数据模型、技术栈
  - 明确凭据管理和分发方案
- **交付物**：`SPEC.md`, `SPEC_PROCESS.md`

### 2. Writing Plans（编写实现计划）
- **触发时机**：SPEC 完成并签字确认后
- **目标**：将设计分解为可执行的任务列表
- **技能位置**：`.claude/skills/writing-plans/`
- **关键活动**：
  - 每个 task 2-5 分钟可完成
  - 明确文件路径、实现要点、验证步骤
  - 标注依赖关系和可并行部分
- **交付物**：`PLAN.md`

### 3. 冷启动验证
- **触发时机**：PLAN 完成后，正式实现前
- **目标**：用陌生 agent 验证 SPEC/PLAN 清晰度
- **关键活动**：
  - 使用不同类型的 AI agent
  - 仅提供 SPEC + PLAN，无历史上下文
  - 让其实现 1-2 个 task
  - 记录暴露的缺陷并修订
- **更新**：`SPEC_PROCESS.md`

### 4. Using Git Worktrees（工作区隔离）
- **触发时机**：开始实现前
- **目标**：为每个功能模块创建隔离的工作区
- **技能位置**：`.claude/skills/using-git-worktrees/`
- **关键活动**：
  - 每个 worktree 对应一个 PR
  - 隔离不同功能的开发

### 5. Subagent-Driven Development（子代理驱动开发）
- **触发时机**：执行 PLAN 中的 task
- **目标**：派发 subagent 自主完成单一任务
- **技能位置**：`.claude/skills/subagent-driven-development/` 或 `.claude/skills/executing-plans/`
- **关键活动**：
  - 每个 task 派一个新鲜 subagent
  - 在 worktree 中工作
  - 记录到 AGENT_LOG.md

### 6. Test-Driven Development（测试驱动开发）
- **触发时机**：每个 task 实现时
- **目标**：强制执行红-绿-重构循环
- **技能位置**：`.claude/skills/test-driven-development/`
- **关键活动**：
  - 红：先写失败测试
  - 绿：写最少代码使其通过
  - 重构：优化代码结构
  - **绝不先写实现再补测试**

### 7. Requesting Code Review（代码评审）
- **触发时机**：每个 task 完成后
- **目标**：两阶段评审确保质量
- **技能位置**：`.claude/skills/requesting-code-review/`
- **关键活动**：
  - 第一阶段：Spec 合规检查
  - 第二阶段：代码质量检查
  - Critical issue 必须修复

### 8. Finishing a Development Branch（完成分支）
- **触发时机**：所有 task 完成后
- **目标**：决定 merge/PR/保留/丢弃
- **技能位置**：`.claude/skills/finishing-a-development-branch/`
- **关键活动**：
  - 验证所有测试通过
  - 创建 PR 并标注 subagent 信息

## 当前项目状态

**阶段**：阶段 0 - 准备与环境搭建（90% 完成）

**已完成**：
- ✅ 创建项目文档结构
- ✅ 合并项目指南
- ✅ 安装 Superpowers（技能已复制到 `.claude/skills/`）

**下一步**：
1. 创建 GitHub 仓库
2. 确定项目选题
3. 开始 Brainstorming

## 技能调用方式

由于 `/brainstorming` 等命令在当前环境不可用，请通过以下方式引导工作流：

**示例对话**：
```
用户：现在开始 brainstorming 阶段，帮我分析需求并生成 SPEC.md
AI：好的！让我按照 brainstorming 技能的要求开始...
```

## 重要提醒

- **在 SPEC 与 PLAN 完成并通过冷启动验证之前，禁止编写任何实现代码**
- **严格遵循 TDD：先红、再绿、再重构**
- **持续更新 AGENT_LOG.md 和 PLAN.md**
- **所有凭据绝不提交到 Git**

---

更多详情请参考：
- [项目完整指南](project-docs/PROJECT_GUIDE_B.md)
- [项目进度跟踪](project-docs/PROJECT_PROGRESS.md)
- [交付物检查清单](project-docs/DELIVERABLES_CHECKLIST.md)
