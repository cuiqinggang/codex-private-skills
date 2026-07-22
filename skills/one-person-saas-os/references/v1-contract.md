# One Person SaaS OS v1 Contract

## Goal

Generate a deployable SaaS base for one-person operation:

idea -> code -> GitHub -> Vercel -> login -> data -> analytics -> dashboard

## Required Stack

- Frontend: Next.js App Router, TypeScript, Tailwind
- Auth: Clerk
- Database client: Supabase
- Analytics: PostHog
- Deployment: Vercel
- Version control: Git/GitHub-ready

## Required Files

- `src/app/page.tsx`
- `src/app/dashboard/page.tsx`
- `src/app/api/health/route.ts`
- `src/core/db/supabase.ts`
- `src/core/auth/middleware.ts`
- `src/core/analytics/posthog.ts`
- `.env.example`

## Forbidden in v1

- Payment systems
- Stripe checkout or webhooks
- Redis, Upstash, queues, or cache layers
- Vector databases such as Pinecone
- Multi-service orchestration
- Complex backend frameworks

## Upgrade Path

- v2: Stripe payment and subscription state
- v3: AI agent capability and answer-quality workflow
- v4: SaaS product factory and repeatable product generation

## Source Notes

The user's source material frames one-person SaaS as a company-function automation loop, not a cost list. v1 captures only the low-stable foundation. Growth, payment, monitoring, email, cache, and AI retrieval remain explicit later layers.
