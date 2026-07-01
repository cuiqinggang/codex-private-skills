---
name: ai-token-business
description: Use when the user asks about AI token business, low-cost API business, token source, API aggregation, model gateway, OpenRouter, LiteLLM, Vercel AI Gateway, Cloudflare AI Gateway, BYOK, virtual keys, budget/rate limits, or turning AI API cost advantages into a service.
---

# AI Token Business

## Positioning

This skill turns “AI token / low-cost API” ideas into a compliant technical-service route. It must not treat gray-market key resale as the plan. The mature route is gateway, cost control, model routing, customer isolation, budget, observability, and service packages.

## Core Judgment

Do not sell keys. Sell reliable AI API cost-control and delivery capability.

Recommended route:

```text
low-cost upstream models
-> gateway / BYOK / virtual keys
-> budget + rate limit + fallback
-> cost tracking + logs + redaction
-> customer packages + support
```

## Sources To Check

Read or search these first when current information matters:

- LiteLLM docs: virtual keys, budget, rate limits, routing, fallback.
- OpenRouter docs: provisioning keys, limits, credits, BYOK, usage.
- Vercel AI Gateway docs: unified API, BYOK, provider order/fallback, cost tracking.
- Cloudflare AI Gateway docs: logs, caching, limits, fallback, cost estimation.
- Portkey, Helicone, Langfuse docs: observability, gateway, cost attribution.
- OpenAI / Anthropic / provider service terms before any resale or customer-facing claim.

Use `templates/ai-token-business-info-card.md` for each source.

## Long-Term Update Mode

When the user wants to “keep it updated” or “collect all useful token business information”, do not deploy anything. Maintain a planning and evidence layer:

1. Search public docs, pricing pages, changelogs, GitHub issues, Product Hunt, Reddit/HN, videos, and Chinese public sources.
2. Score every item by whether it improves one of these: low-buy source, high-sell service, gateway operations, customer package, cost control, compliance, or risk avoidance.
3. Add useful items to the watchlist or reference notes.
4. Promote only verified, reusable patterns into this skill.
5. Keep New API production operations separate; do not touch `new-api-local-deploy` unless the task is explicitly local deployment or health.

Update cadence:

- Every system-evolution run: collect public signals and create report-only notes.
- Weekly or after major releases: refresh official docs, price/rate-limit changes, terms, and risk redlines.
- After any verified useful pattern: add it as a concise rule, template field, or validation task.

Useful information must be detailed enough to act on later: source link, what changed, why it matters, low-buy/high-sell relevance, risk, minimal validation, and whether it should become a skill rule.

## Required Output Structure

Every report must include:

1. 总判断：可做 / 观察 / 不做。
2. 低买：upstream, price, limits, stability, compliance, alternatives.
3. 高卖：customer pain, deliverables, packages, support, margin source.
4. 成熟案例：what can be replayed, what must be verified.
5. 风险红线：terms, account, data, cost runaway, model substitution.
6. 最小验证任务：no login, no payment, no real key unless approved.
7. Skill/script/process sedimentation candidate.

## Business Routes

| Route | Use When | First Validation |
|---|---|---|
| LiteLLM mock gateway | user wants self-hosted control | write mock config, no real key |
| BYOK managed setup | customer has own provider keys | produce setup checklist and risk boundary |
| Vercel/Cloudflare gateway | user wants hosted route | compare docs and limits |
| Cost audit package | customer already has usage | use redacted usage summary |
| Monthly maintenance | customer needs stability | define report, alert, model replacement flow |

## Current Watch Categories

| Category | Examples | Why it matters |
|---|---|---|
| Open-source gateway | LiteLLM, New API | Self-hosted control and local proof of concept |
| Hosted gateway | Vercel AI Gateway, Cloudflare AI Gateway | Faster customer delivery, BYOK, fallback, logs |
| Aggregator | OpenRouter and similar | Multi-model routing, credits, rate limits, provider abstraction |
| Observability | Helicone, Langfuse, Portkey | Cost attribution, prompt traces, customer billing support |
| Cost/risk signals | rate limits, BYOK fees, fallback charges, 429/5xx reports | Avoid unprofitable or unstable service promises |
| Terms/compliance | OpenAI, Anthropic, provider terms | Prevent account/key resale and unsafe claims |

## Forbidden By Default

- Selling, sharing, renting, or brokering raw API keys.
- Sharing personal/enterprise subscriptions.
- Promising unlimited, official-equivalent, or guaranteed-stable low-price access without evidence.
- Reading or storing customer secrets without explicit approval and isolation.
- Calling paid APIs, creating keys, registering accounts, purchasing credits, or changing production routing.
- Using opaque gray-market proxy services as a recommended route.

## Approval Required

Ask before:

- API key access or any paid call.
- logging into provider dashboards.
- creating customer-facing keys, credits, plans, invoices, or terms.
- deploying a long-running gateway or modifying production env vars.

## Minimal Safe Actions

Allowed without extra approval in system-evolution work:

- Read public docs and terms.
- Build report-only comparison tables.
- Create mock configs with placeholder keys.
- Draft customer package templates.
- Generate validation tasks.
- Update skill drafts and H-drive mirrors.

## Relationship With New API

New API is one possible local gateway implementation, not the whole business route.

Use `new-api-local-deploy` when the task is about:

- local server health,
- Docker Compose,
- PostgreSQL / Redis,
- localhost port binding,
- setup/login page,
- New API token or channel setup.

Use this skill when the task is about:

- whether a low-cost API service should exist,
- upstream/source comparison,
- BYOK / virtual key / budget / rate-limit strategy,
- customer packages,
- compliance and risk,
- business validation tasks.

Keep outputs separate. This skill may recommend New API as a local proof-of-concept, but it must not modify the New API deployment or read `.env`.
