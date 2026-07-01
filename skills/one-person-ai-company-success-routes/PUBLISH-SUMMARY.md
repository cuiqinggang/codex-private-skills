# 一人 AI 公司成功路线技能包发布摘要

更新时间：2026-06-13

## 这个文件是干嘛的

`PUBLISH-SUMMARY.md` 是本技能包的固定发布入口。

它的作用不是替代详细报告，而是给人、Obsidian、恢复脚本和后续自动索引一个稳定文件名，用来快速判断：

- 这个技能包当前发布版在哪里。
- 哪些文件是核心入口。
- 哪些案例和路线已经入库。
- 新资料应该追加到哪里。
- 当前包是否可以继续维护。

如果只保留 `PUBLISH-SUMMARY-20260528.md` 这种带日期文件，后续扫描会知道“历史发布页存在”，但不知道哪一个是当前默认入口。所以本文件补成 canonical index，当前默认指向 2026-05-28 发布版，并串起后续新增发布页。

## 当前主路径

```text
H:\AI\skills\one-person-ai-company-success-routes
```

恢复包和重新激活报告：

```text
H:\AI\_recovery\one-person-ai-company-skill-reactivation-20260613
```

Obsidian 入口：

```text
H:\AI\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS\00_INDEX\一人AI公司资料包入口.md
```

## 当前默认发布版

- 主发布摘要：`PUBLISH-SUMMARY-20260528.md`
- 极简创业 10 skills 发布页：`PUBLISH-MINIMALIST-ENTREPRENEUR-10-SKILLS-20260530.md`
- 刘小排 AI 公司运营方法发布页：`PUBLISH-LIU-XIAOPAI-AI-COMPANY-OPERATIONS-20260530.md`
- Chatbase / Yasser AI Agent Harness 发布页：`PUBLISH-CHATBASE-YASSER-AI-AGENT-HARNESS-20260601.md`

## 核心入口文件

| 文件 | 用途 |
|---|---|
| `SKILL.md` | 技能触发入口和使用边界。 |
| `README.md` | 普通阅读入口，说明这个包是什么、怎么更新。 |
| `RUNBOOK.md` | 执行一次搜索、判断、吸收、同步的流程。 |
| `SOURCE-OF-TRUTH-MAP.md` | 来源证据地图。 |
| `CASES.md` | 已入库案例索引。 |
| `ROUTE-MATRIX.md` | 路线矩阵和推荐动作。 |
| `WATCHLIST.md` | 后续观察列表。 |
| `ABSORPTION-RULES.md` | ABSORB / REPLAY / WATCH / REJECT 判断规则。 |
| `REPLAY-METHOD.md` | 安全 replay 方法。 |
| `GOVERNANCE.md` | 审批门、安全边界、密钥规则。 |
| `GLOSSARY-ZH.md` | 中文术语表。 |
| `CHANGELOG.md` | 更新历史。 |

## 已覆盖资料范围

- 外国公司 / 开源项目案例：HiveWard、MetaGPT、ChatDev、CrewAI、AutoGen、LangGraph、n8n、Dify、Flowise、Polsia / POSA、Chatbase 等。
- 国内个人 / 运营公司资料：刘小排 AI 公司运营方法等。
- 商业想法和收益路径：极简创业 10 skills、Chatbase 早期付费和企业化路径、AI 公司运营闭环等。
- 技术路线：Agent Company OS、多 Agent 软件公司、可视化 AI 工作流、AgentOps / trace / eval / HITL、本地执行体映射。
- 本机体系映射：Hermes、Codex Desktop、OpenClaw、ComfyUI、ECC、Obsidian Knowledge OS、AI Company Dashboard。

## 后续追加规则

1. 新资料先进入 `WATCHLIST.md`，记录来源、摘要、证据和初步判断。
2. 可复现路线进入 `ROUTE-MATRIX.md`，写清机制、价值、风险和推荐动作。
3. 有明确主体、证据、路径和结果的资料进入 `CASES.md` 或 `references/CASE-*.md`。
4. 已经稳定复用的流程再进入 `SKILL.md` / `RUNBOOK.md`。
5. 新的可阅读发布页使用 `PUBLISH-主题-日期.md`，并在本文件中追加链接。
6. 不移动旧资料，不覆盖旧版本；多版本先写对照，再决定是否合并。

## 安全边界

- 不读取、不记录、不复制 API key、token、密码、cookie、`.env` 或 credentials。
- 不修改 Hermes、OpenClaw、New API、ComfyUI、Codex、ECC 的生产配置。
- 不真实发送微信、飞书、Telegram、邮件、短信、广告、支付或客户触达。
- 所有真实接入前必须经过 `GOVERNANCE.md` 的人工审批门。

## 当前状态

```text
ONE_PERSON_AI_COMPANY_SKILL_PUBLISH_SUMMARY_CANONICAL_READY
```

本文件是在 2026-06-13 恢复/重新激活过程中补齐的固定发布摘要入口。补齐后，恢复检查不应再因为缺少 `PUBLISH-SUMMARY.md` 标记为缺核心文件。
