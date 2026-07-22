# Lesson Extraction 2026-07-05

## Value Judgment

HIGH_VALUE.

The material defines a repeatable one-person SaaS operating stack and the user explicitly requested a deployable, updatable skill pack. It can become a SOP, project template, checklist, and future trigger.

## Core Lesson

One-person SaaS is not only a tool list. It is a closed loop:

idea -> AI coding -> GitHub versioning -> Vercel deployment -> user login -> Supabase data -> PostHog analysis -> iteration

## v1 Reduction

The full stack includes payment, email, monitoring, cache, vector search, and AI retrieval. The deployable v1 must stay low-stable:

- Build layer: Codex/Claude-generated Next.js
- Identity layer: Clerk
- Data layer: Supabase client
- Analytics layer: PostHog
- Deployment layer: Vercel and GitHub

## Triggers

- `RUN one-person-saas-os`
- `一人公司 SaaS`
- `SaaS 操作系统`
- `低成本 SaaS 部署`
- `多智能体极限低成本答案 项目部署`
- `Next.js Clerk Supabase PostHog Vercel`

## AGENTS.md Patch Draft

For future global rules, add a compact trigger:

```markdown
When the user asks to generate or deploy a one-person SaaS base, use
${REDACTED_SECRET}
Next.js App Router, Clerk, Supabase, PostHog, Vercel, GitHub. Do not add
Stripe, Redis, vector DB, or multi-service backend unless the user explicitly
requests the upgrade path.
```
