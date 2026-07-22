---
name: one-person-saas-os
description: Generate and evolve a deployable low-stable one-person SaaS starter. Use when the user says "RUN one-person-saas-os", asks to create a SaaS OS skill pack, scaffold a Next.js App Router SaaS with Clerk, Supabase, PostHog, Vercel, and GitHub, update the one-person SaaS deployment workflow, preserve first-dollar SaaS case studies, or plan overseas launch/payment/growth for the low-cost multi-agent answer project.
---

# One Person SaaS OS

## Purpose

Create a low-complexity SaaS v1 base that can be deployed quickly and improved over time:

- Next.js App Router, TypeScript, Tailwind
- Clerk identity
- Supabase data client
- PostHog analytics
- Vercel-ready project files
- Git-initialized repository

Keep v1 intentionally small. Do not add Stripe, webhooks, Redis, vector databases, queues, multi-service orchestration, or a complex backend unless the user explicitly upgrades the skill to a later version.

## Fast Path

When the user says `RUN one-person-saas-os`:

1. Choose a project output directory. If the user does not specify one, create it under the active Codex workspace.
2. Run:

```powershell
${REDACTED_SECRET}
```

3. Inspect the generated summary and required file checklist.
4. If deployment preparation is requested, run dependency install and build in the generated project:

```powershell
npm install
npm run build
```

5. Keep `.env.example`; create `.env.local` only when real keys are provided by the user.
6. Commit the generated base after validation.

## Generation Contract

The generated project must include:

- `src/app/page.tsx`
- `src/app/dashboard/page.tsx`
- `src/app/api/health/route.ts`
- `src/core/db/supabase.ts`
- `src/core/auth/middleware.ts`
- `src/core/analytics/posthog.ts`
- `.env.example`
- Clerk provider wiring
- Clerk dashboard protection
- PostHog initialization
- Supabase client initialization
- Git repository initialization

Also generate compatibility files needed by the actual framework, such as `src/middleware.ts`, `src/app/layout.tsx`, `src/app/providers.tsx`, package files, TypeScript config, Tailwind/PostCSS config, and Vercel metadata.

## Implementation Rules

- Prefer the bundled generator script over hand-writing the same boilerplate again.
- Keep the first run deployable and boring. Make the landing page and dashboard useful, but avoid marketing-heavy layout.
- Use Clerk as the identity source of truth and Supabase as the business data client.
- Treat PostHog as optional at runtime: the app must not crash when analytics keys are absent in local development.
- Keep all public browser variables prefixed with `NEXT_PUBLIC_`.
- Never include real secrets in generated files.
- Do not add payment, Stripe webhook, Redis, Pinecone, Upstash, Resend, Sentry, or AI-agent runtime in v1. Record those as upgrade candidates instead.

## References

Read only when needed:

- `references/v1-contract.md`: exact v1 scope and upgrade boundaries.
- `references/deployment-checklist.md`: local, Vercel, GitHub, Clerk, Supabase, and PostHog deployment checks.
- `references/overseas-link-platforms-20260705.md`: copyable overseas free link-distribution table and posting SOP.
- `references/payment-account-stripe-notes-20260705.md`: Stripe/payment account compliance notes and v2 payment route.
- `references/case-study-first-usd-codex-saas-20260705.md`: complete preserved friend case study and executable first-dollar extraction.
- `references/first-dollar-launch-sop-20260705.md`: step-by-step idea-to-first-USD workflow absorbed from the case study.
- `references/indie-site-risk-gates-video-20260706.md`: converted independent-site failure video into SaaS launch risk gates.
- `references/prelaunch-risk-gate-checklist-20260706.md`: HTTPS, mobile, payment fallback, backup, and legal/trust prelaunch checklist.
- `references/failure-review.md`: failure review entry point for future deployment mistakes.
- `references/lesson-extraction-20260705.md`: source lesson converted from the user's SaaS stack material.
- `references/recent-use-log.md`: append each meaningful use or update.

## Customer-Facing Launch Gates

When the user asks to launch publicly, deliver a customer site, add payment,
prepare overseas collection, or avoid independent-site mistakes, read
`references/prelaunch-risk-gate-checklist-20260706.md` before claiming readiness.

Do not mark a public launch `LAUNCH_READY` until the applicable gates are checked:

- HTTPS/custom-domain safety.
- Mobile usability and tap targets.
- Payment readiness plus fallback when payment is in scope.
- Backup/recovery for code, data, content, and env configuration.
- Legal/trust pages for paid or customer-facing launch.

For v1 generation, keep the starter low-stable and payment-free unless the user
explicitly requests payment. Record missing payment/legal/backups as launch gates
instead of quietly expanding the base architecture.

## Acceptance

Mark a run `PASS` only when:

- The generator completes without errors.
- The required file checklist is present.
- Git initialization is attempted and the result is reported.
- No forbidden v1 components are generated.
- A local install/build check is run when deployment readiness is requested.
- Customer-facing launch gates are checked when the user asks for public launch,
  payment, client delivery, or independent-site readiness.

Use `REVIEW_READY` if the project is generated but dependency install or build was intentionally skipped. Use `PARTIAL` if any required file is missing.
