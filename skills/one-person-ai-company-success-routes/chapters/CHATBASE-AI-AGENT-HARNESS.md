# Chatbase AI Agent Harness 路线

检查日期：2026-06-01 Asia/Shanghai

来源：用户提供视频 `F:\000\xwechat_files\wxid_bq3n41o6t4o721_699b\msg\video\2026-06\b5736d53fac7c5f795dfdb89baab2197.mp4`，以及公开搜索核验资料。

整理口径：本章节只吸收 Chatbase / Yasser Elsaid 案例里的可复用机制，不登录 Chatbase，不调用 API，不接 Stripe/Zendesk/Salesforce/WhatsApp/Slack，不读取任何 API key。

## 一句话核心

Chatbase 的路线不是“做一个聊天机器人就结束”，而是先用极简单的文档问答切入，快速验证付费，再把产品从 chatbot 升级为面向客户体验的 AI agent harness：知识库、渠道、身份、联系人、工具调用、业务系统集成、人工升级、分析监控、计费风控和企业合规都在一个平台里。

## 为什么进入一人公司技能包

这个案例对一人 AI 公司有价值，是因为它展示了三个层次的跃迁：

1. 单人开发者可以在正确时间窗口内用很小的 MVP 切入高频需求。
2. 早期不要过度复杂，先让用户“上传资料 -> 得到可嵌入 chatbot -> 付费使用”。
3. 真正长期价值不在“包一层模型”，而在把 AI agent 接到真实业务系统，让它能行动、可审计、可升级给人。

## 路线结构

```text
ChatGPT / LLM 爆发窗口
  -> 极简 PDF / 网站知识库 chatbot
  -> 自助注册 + 快速付费
  -> RAG / 数据源 / 网站嵌入
  -> 客服场景聚焦
  -> API / custom actions / business tools
  -> contacts / identity / personalization
  -> human-in-the-loop / escalation
  -> analytics / billing / fraud / revenue recovery
  -> multi-channel: web, WhatsApp, Slack, Instagram, voice, email, messaging
  -> enterprise-ready customer-facing AI agent platform
```

## 可吸收机制

| 机制 | Chatbase 做法 | 本地吸收方式 |
|---|---|---|
| 极简 wedge | 先从“上传文档/网站 -> 生成 chatbot”开始 | 新产品先找一个最窄、最容易付费的入口 |
| 速度优先 | 视频强调早期速度大于完美，公开资料显示 MVP 很快上线 | 对新路线先做 48 小时 mock，不先做大平台 |
| 自助付费 | Stripe 案例显示早期就接入支付和自助套餐 | 本地只吸收计费状态模型，不接真实支付 |
| 从 chatbot 到 agent | 官方博客强调不只回答，还能连接系统执行动作 | Dashboard 增加 `Action Harness` 概念 |
| 业务系统连接 | Stripe、Cal.com、Zendesk、Salesforce、Shopify 等工具链 | 只建 mock connector registry，真实 connector 走审批 |
| 身份和联系人 | Contacts / identity 让 agent 识别用户并个性化处理 | 建立 `contact_context` 字段，不放真实 PII |
| 人工升级 | Anthropic 客户案例强调 human-in-the-loop 和一键确认 | 进入审批门、人工接管、升级规则 |
| 多渠道复用 | Voice 发布稿强调同一知识库、actions、升级逻辑复用于电话 | AICompany Dashboard 做统一 agent config，不为每个渠道复制一套 |
| 运营分析 | Docs 包含 analytics/monitoring，Stripe 案例包含收入恢复、欺诈下降 | run history + revenue metrics + fraud/risk fields |
| 上市场转型 | 从 SMB 自助到 enterprise onboarding | Watchlist 标记“什么时候该转企业/高端市场” |

## 适合进入 Polsia / AICompany Dashboard 的模块

| 模块 | 字段 |
|---|---|
| Agent Profile | 名称、目标用户、品牌语气、默认边界 |
| Knowledge Sources | 文档、网站、数据库、FAQ、版本 |
| Channels | Web、微信/社群 mock、邮件 mock、voice mock、Slack/WhatsApp mock |
| Actions | 查询订单、退款、开票、预约、创建 ticket、查账户状态 |
| Contacts | external_id、segment、权限、上下文摘要 |
| Escalation | 触发条件、人工审批、一键确认、人工接管 |
| Analytics | 会话数、解决率、升级率、满意度、成本、收入 |
| Billing Model | 自助套餐、用量、add-ons、企业定制 |
| Compliance | 数据边界、审计日志、PII 脱敏、权限 |

## 本地执行规则

1. 只做 mock/read-only/demo。
2. 不登录 Chatbase、Stripe、Zendesk、Salesforce、Shopify、Slack、WhatsApp、Twilio。
3. 不调用 Chatbase API；文档中的 API key 示例只作为风险提示。
4. 不复制或保存任何真实客户数据。
5. 所有 connector 都先建“能力卡”和“审批门”，不做真实动作。
6. 先复刻业务结构，再判断是否值得实现代码。

## 进入技能包的判断

推荐动作：`ABSORB`。

原因：Chatbase 是“一人 AI 公司”从单点工具到 Agent 平台的典型路线。它补上此前案例里的一个关键环节：外部 agent 公司不是只靠多 Agent 编排，而是靠“业务系统连接 + 可行动 + 可监督 + 可计费 + 可转企业”的产品化能力。

状态码：`ONE_PERSON_AI_COMPANY_ROUTES_CHATBASE_HARNESS_ABSORB_PASS`
