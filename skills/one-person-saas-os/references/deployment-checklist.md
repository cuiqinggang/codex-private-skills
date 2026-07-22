# Deployment Checklist

## Local

- Generate project with `scripts/create_one_person_saas_os.py`.
- Create `.env.local` from `.env.example` only after real keys are available.
- Run `npm install`.
- Run `npm run build`.
- Confirm `/api/health` returns `ok`.
- Confirm `/dashboard` redirects to Clerk when signed out.

## Clerk

- Create a Clerk application.
- Add publishable and secret keys to Vercel environment variables.
- Confirm the middleware file is under `src/middleware.ts` for the generated `src` app.

## Supabase

- Create a Supabase project.
- Add URL and anon key to Vercel environment variables.
- Keep service role keys out of browser-accessible code.

## PostHog

- Add `NEXT_PUBLIC_POSTHOG_PROJECT_TOKEN`.
- Add `NEXT_PUBLIC_POSTHOG_HOST`.
- Confirm local development does not crash when keys are absent.

## Vercel and GitHub

- Push the generated Git repository to GitHub.
- Import the repository into Vercel.
- Set environment variables in Vercel.
- Deploy and check `/api/health`.

## Customer-Facing Launch Gates

Use `references/prelaunch-risk-gate-checklist-20260706.md` before telling the
user a public SaaS, independent site, or client delivery is launch ready.

- HTTPS/custom domain: production URL opens over `https://` with no unsafe
  browser warning.
- Mobile: homepage, sign-in, dashboard, and any payment/result page work at
  narrow mobile widths.
- Payment: if payment is in scope, provider approval state and fallback path are
  known before launch.
- Backup: source, database, storage, product content, and env configuration have
  a recovery path.
- Legal/trust: paid or customer-facing launch has privacy, terms, refund or
  cancellation policy, contact, and delivery/access explanation.

## Acceptance Status

- `PASS`: generated, installed, built, and deployment checks pass.
- `REVIEW_READY`: generated and ready for install/build/deploy.
- `PARTIAL`: generated with missing required files or blocked dependency checks.
- `BLOCKED`: cannot generate because target directory or local tools are unavailable.
- `LAUNCH_READY`: applicable customer-facing launch gates also pass.
