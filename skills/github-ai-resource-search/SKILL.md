---
name: github-ai-resource-search
description: Use when the user wants to find, compare, or evaluate AI tools, MCP servers, Claude Code/Codex resources, n8n templates, automation workflows, prompt libraries, open-source tutorials, or GitHub repositories. Prioritize this skill for search/tool-discovery requests before broad web search when GitHub/open-source resources may be useful.
---

# GitHub AI 资源高级搜索与筛选

## 默认优先规则

这是本机 AI/open-source 资料源头搜索的默认前置技能。

当任务涉及“搜索、寻找、推荐、筛选、比较、发现资料源”且目标可能属于 AI 工具、开源项目、GitHub 仓库、MCP、Claude Code、Codex、n8n、自动化模板、prompt、agent workflow、开源教程、开发者资料、技术趋势、真实用户痛点时，先启动本技能，再决定是否需要普通网页搜索、GitHub 工具、浏览器、Firecrawl 或其他资料源。

不要把它用于所有搜索。餐厅、旅行、价格、政策、新闻、医疗、法律、金融、购物等普通时效搜索仍按对应规则直接查权威来源或实时网页。本技能优先覆盖“AI/开源/工具/教程/模板/工作流/需求挖掘”这一类资料源头。

## 触发条件

优先在这些场景调用：

- 用户要找 AI 工具、MCP Server、Claude Code/Codex 插件、n8n 自动化模板、开源教程、提示词库。
- 用户说“找找有没有开源项目 / GitHub 上有没有 / 有没有别人整理好的资源”。
- 用户要判断某个 AI 仓库是否靠谱、是否还在维护、是否适合非程序员。
- 用户要找可复用模板、工作流、教程案例、赚钱项目或趋势信号。

## 输入要求

- 主题关键词，例如 `MCP`、`Claude Code`、`Codex`、`n8n`、`AI agent`。
- 目标类型：资源合集、官方项目、模板、教程、代码库、需求/痛点。
- 成熟度偏好：成熟稳定 / 新兴小众 / 官方优先 / 中文友好。

## 执行流程

1. 先把用户的大词拆成 2-5 个搜索关键词，补充英文同义词。
2. 新领域优先查 `awesome + 关键词`，先找资源地图。
3. 用 `stars:` 粗筛关注度，用 `pushed:` 保证近期仍活跃。
4. 对变化快的 AI 方向，默认加入近期更新时间门槛，例如 `pushed:>2026-01-01`。
5. 官方资源优先用 `user:` 或 `org:` 限定，例如 `org:openai codex`。
6. 已知仓库内找入口时，用 `repo:owner/name install`、`repo:owner/name quickstart`、`repo:owner/name examples`。
7. 读取候选仓库时，优先看 README、Quickstart、Examples、截图、安装步骤、使用案例、近期提交、issue 维护情况。
8. 输出候选清单时，必须标注：用途、成熟度、最近活跃度、适合人群、风险、下一步验证动作。

## 常用搜索式

```text
awesome mcp stars:>100 pushed:>2026-01-01
awesome claude code stars:>50 pushed:>2026-01-01
ai agent stars:>500 pushed:>2026-01-01
org:openai codex
repo:openai/codex install
repo:openai/codex quickstart
repo:openai/codex examples
```

## 边界条件

- 不把 GitHub 搜索结果直接当成可安装结论；必须再做安全、许可、维护状态和本地适配检查。
- 不仅凭 star 排名做决定。
- 不在用户只要普通网页搜索、新闻、价格、政策时强行使用 GitHub。
- 私有仓库、付费代码、许可证不清晰的项目不直接复制或安装。

## 验收标准

一次合格输出至少包含搜索式、候选仓库筛选表、每个候选的 star/更新时间/README 状态、是否适合非程序员、下一步验证或安装建议。

## 关联技能

- `github-issues-demand-mining`: 当任务进入需求挖掘、选题、痛点分析时调用。
- `cangjie-skill`: 当找到高价值长文、教程、视频转写稿后，用它蒸馏成 skills。
- `video-audio-transcription`: 当来源是视频/录音时，先转文字再沉淀。
