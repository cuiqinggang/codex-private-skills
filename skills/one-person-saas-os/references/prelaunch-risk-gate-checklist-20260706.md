# Prelaunch Risk Gate Checklist 2026-07-06

Use this before saying a one-person SaaS, independent site, or customer-facing
landing page is ready to launch.

## Gate 1: HTTPS And Domain

- Production URL opens over `https://`.
- Browser does not show an unsafe certificate warning.
- Custom domain DNS resolves to the intended deployment.
- No customer-facing link uses `http://`.
- If Cloudflare is used, SSL mode and redirects are verified in the browser.

## Gate 2: Mobile Usability

- Homepage checked at 360, 390, and 430 px widths.
- Sign-in and dashboard checked on mobile.
- Primary CTA button is visible and tappable.
- Forms, long words, pricing cards, result pages, and modals do not overflow.
- Images do not overlap text or buttons.
- Sticky headers/footers do not cover actions.

## Gate 3: Payment Readiness And Fallback

Only apply this gate when payment is in scope.

- Payment provider account status is known: approved, pending, rejected, or not
  yet applied.
- At least one fallback path is selected before launch: Paddle, Creem, PayPal,
  Stripe, manual invoice, or waitlist/manual fulfillment.
- Pricing and delivery/access rules are visible before checkout.
- Refund/cancellation rules are visible before checkout.
- A failed payment-provider review does not make the whole product unusable.

## Gate 4: Backup And Recovery

- Source code is pushed to Git/GitHub.
- Environment variable names are documented without exposing secrets.
- Supabase tables/storage that matter have a backup or export plan.
- Product content, prompts, pricing copy, and legal pages are stored in the repo
  or a durable note.
- A recovery owner and recovery path are clear.

## Gate 5: Legal And Trust Pages

For paid or customer-facing launch:

- Privacy Policy exists.
- Terms of Service / Terms of Use exists.
- Refund or cancellation policy exists.
- Contact method exists.
- Delivery/access method is clear.
- The website has no placeholder legal pages.

## Status Labels

- `LAUNCH_READY`: all applicable gates passed.
- `REVIEW_READY`: product works, but non-critical launch evidence still needs
  human review.
- `PARTIAL`: one or more gates are missing.
- `BLOCKED`: payment approval, domain/SSL, data recovery, or legal/trust surface
  blocks launch.

## Copyable Review Table

| Gate | Status | Evidence | Fix Needed |
|---|---|---|---|
| HTTPS/domain |  |  |  |
| Mobile usability |  |  |  |
| Payment fallback |  |  |  |
| Backup/recovery |  |  |  |
| Legal/trust pages |  |  |  |
