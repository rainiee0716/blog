---
title: 'everything-claude-code 指南：让 Claude Code 变得更强的那套扩展'
description: 'Claude Code 生态里有个 GitHub Star 很高的项目 everything-claude-code，里面有几十个专业代理、上百个技能定义和一套兼容层。我从结构、能力、上手三个角度聊一下。'
pubDate: '2026-04-04'
heroImage: '../../../assets/hero-clawdbot.jpg'
category: 'AI 工具'
---

Claude Code 的生态里有一个项目 Star 数冲得很高——`everything-claude-code`，曾经在 Anthropic 官方黑客马拉松里拿过奖，被称为目前最强大的 Claude Code 增强工具。

这篇文章我做一次完整解析，看看它到底叠加了什么，以及怎么上手。

## 项目是什么

`everything-claude-code` 不是一个配置包，而是一套完整的 AI 代理性能优化系统。它给 Claude Code 叠加了：

- 技能（Skills）
- 本能（Instincts）
- 内存（Memory）
- 安全扫描
- 研究优先开发

兼容性也很广，Claude Code、Codex、Cowork 这些主流 AI 代理工具都支持。

## 数字一览

| 指标 | 数量 |
|------|------|
| 专业子代理 | 38 个 |
| 技能定义 | 156 项 |
| 命令兼容层 | 72 个 |
| 支持编程语言 | 10 种 |

覆盖的语言包括 TypeScript、Python、Go、Java、Perl、PHP、Kotlin、C++、Rust、Swift。

## 目录结构

```
everything-claude-code/
├── agents/          # 36 个专业子代理
│                    # 规划师、架构师、代码审查员、重构专家……
├── skills/          # 工作流定义和领域知识（156 项技能）
├── commands/        # 传统命令兼容层（72 个）
├── rules/           # 语言规则（common/typescript/python/golang/等）
├── hooks/           # 触发式自动化脚本
├── contexts/        # 动态系统提示注入上下文
├── examples/        # 示例配置和会话示例
├── mcp-configs/     # MCP 服务器配置
└── install.sh       # 安装脚本
```

## 几个值得展开的能力

### Token 优化

内置了 Token 消耗监控和智能压缩策略。每次会话追踪 Token 使用量，达到阈值时自动触发上下文压缩，避免溢出中断或重复劳动。

这套机制对长会话特别有用——开过 Claude Code 的人都知道，上下文不够的时候模型会开始"失忆"，反复要你重新解释背景。

### 子代理分工

38 个专业子代理覆盖了开发的常见角色：

- 规划师：拆解需求、生成实施步骤
- 架构师：做技术选型、画系统图
- 代码审查员：检查 PR、给出改进建议
- 重构专家：识别代码异味、给出重构方案
- 测试工程师：补单元测试、设计测试用例

每个代理都有自己的 prompt 和工具配置。调用时根据任务类型路由。

### 内存系统

这是我觉得最有意思的设计。`everything-claude-code` 实现了一套跨会话的"记忆"：

- **项目级记忆**：项目结构、约定、关键文件位置
- **会话级记忆**：最近的工作上下文
- **全局记忆**：用户偏好、常用工具配置

下次开新会话时，模型会自动加载这些记忆，省去重复说明。

### 技能系统

技能（Skills）是把"领域知识"封装成可复用的模块。比如：

- "React 组件审查"技能：自动检查 React 组件的可访问性、性能、规范
- "API 文档生成"技能：根据代码自动生成 OpenAPI 文档
- "数据库迁移"技能：检查迁移脚本的安全性、性能

每个技能都是一个独立 prompt 模板 + 工具集合。

## 安全设计

`everything-claude-code` 在安全上做了不少工作：

- **命令白名单**：危险命令（`rm -rf`、`chmod 777` 等）默认拦截
- **路径限制**：文件操作限制在项目目录内
- **敏感信息过滤**：自动识别 API Key、密码、token，防止泄露
- **审计日志**：所有工具调用都有完整记录

这些是默认开启的，不需要用户额外配置。

## 快速上手

### 1. 克隆仓库

```bash
git clone https://github.com/affaan-m/everything-claude-code.git
cd everything-claude-code
```

### 2. 运行安装脚本

```bash
./install.sh
```

脚本会交互式询问：

- 要安装哪些代理
- 要启用哪些技能
- 项目路径
- MCP 服务器配置

### 3. 配置 Claude Code

在 `~/.claude/settings.json` 里加入：

```json
{
  "agents": "/path/to/everything-claude-code/agents",
  "skills": "/path/to/everything-claude-code/skills",
  "commands": "/path/to/everything-claude-code/commands"
}
```

### 4. 测试

重启 Claude Code，试试：

```bash
claude "请规划一个用户认证模块的实现"
```

应该会自动调用"规划师"子代理。

## 实战经验

我用了一段时间，列几个观察：

**最有用的部分**：技能系统。比如"代码审查"技能，对 PR review 特别有效——自动检查代码风格、性能、安全、可访问性，给我一份结构化的审查报告。

**最惊喜的部分**：内存系统。跨会话的项目记忆让我不用每次重新解释"这个项目用什么 ORM、目录结构怎么组织的"。

**需要小心的部分**：子代理分工不要太细，否则任务被切得太碎反而拖慢效率。我后来只保留 5–6 个最常用的代理。

**性能开销**：开启全部技能后，启动时间和 Token 消耗都有明显增加。生产环境建议按项目需求裁剪。

## 适用人群

`everything-claude-code` 不是给所有人的——它最适合：

- **重度 Claude Code 用户**：每天要用几个小时的人
- **复杂项目维护者**：需要跨会话保持上下文的
- **团队 Leader**：想统一团队 AI 工具配置的人

如果你只是偶尔用 Claude Code 写写脚本，原生版本就够了。

## 总结

`everything-claude-code` 代表了一种思路：把 AI 编程工具的能力从"模型本身"扩展到"完整的工程系统"。子代理分工、技能复用、内存持久——这些设计让 Claude Code 从一个"工具"变成一个"工作流"。

它不解决 AI 编程的根本问题（理解需求、生成正确代码），但显著提升了**日常开发的效率**。

如果你打算长期用 Claude Code，建议至少挑它的几个核心能力（技能系统、内存系统）自己实现一遍——会比直接装现成的更理解背后的设计。