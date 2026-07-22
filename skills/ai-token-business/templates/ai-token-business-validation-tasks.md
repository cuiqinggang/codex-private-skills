# AI token business validation tasks

## TASK-AI-TOKEN-001: LiteLLM mock gateway

- Goal: test whether LiteLLM fits as the self-hosted gateway route.
- Input: public LiteLLM docs and placeholder config only.
- Output: mock config, virtual key/budget/rate-limit/fallback explanation.
- Test: no real key, no model call, no long-running service.
- Success: route can explain customer isolation and cost control.
- Stop: needs secret, paid API, login, or production env change.

## TASK-AI-TOKEN-002: OpenRouter product replay

- Goal: replay the key/limit/usage/credit product structure.
- Input: public OpenRouter docs and terms.
- Output: product field map and risk notes.
- Test: read-only public docs.
- Success: customer-key lifecycle can be described.
- Stop: requires login or key creation.

## TASK-AI-TOKEN-003: Hosted gateway comparison

- Goal: compare Vercel AI Gateway and Cloudflare AI Gateway.
- Input: public docs.
- Output: BYOK, fallback, logging, limits, cost table.
- Test: read-only public docs.
- Success: route recommendation by use case.
- Stop: requires project creation or payment.

## TASK-AI-TOKEN-004: Customer package template

- Goal: turn technical capability into sellable service.
- Input: low-buy/high-sell findings.
- Output: starter/standard/advanced/monthly packages.
- Test: no claims without evidence.
- Success: each package has deliverables, cost, risk, acceptance.
- Stop: needs real customer data or payment.

## TASK-AI-TOKEN-005: Compliance redlines

- Goal: prevent gray-market token resale.
- Input: provider terms and risk cases.
- Output: allowed/approval/forbidden table.
- Test: cite public evidence or mark pending verification.
- Success: skill blocks unsafe routes.
- Stop: route depends on account sharing or opaque proxy resale.

