# Indie Site Risk Gates From Video 2026-07-06

## Source

- Material: WeChat MP4 `6c8a6505ca6a587a4728312d1a2a67c7.mp4`
- Duration: 59.77 seconds
- Processing: local Whisper large-v3 GPU transcript plus key-frame review
- Value judgment: `HIGH_VALUE`

## Why This Belongs In one-person-saas-os

The video is about first-year independent-site delivery failures. It is not a
Next.js tutorial, but the risks map directly onto a one-person SaaS launch:

1. A customer-facing site without HTTPS looks unsafe and loses trust.
2. A desktop-only check misses mobile layout and tap-target failures.
3. A single payment rail can block revenue when approval or checkout fails.
4. No backup means a small incident can erase product, order, or customer data.
5. Missing legal/trust pages weakens payment approval and customer dispute handling.

For `one-person-saas-os`, treat these as launch gates, not optional polish.

## Extracted Lessons

### 1. HTTPS Is A Trust Gate

Video pitfall: SSL was not installed, the browser showed an unsafe site, and
customers left.

SaaS translation:

- Vercel preview/deploy URLs usually have HTTPS, but a custom domain still needs
  DNS and certificate verification.
- Cloudflare can be used for DNS, SSL, and basic edge protection, but the exact
  setup must be verified in the browser.
- Before showing the site to users, open the production URL and confirm there is
  no unsafe certificate warning.

Avoid:

- Treating successful deployment as proof of secure public access.
- Sending customers an HTTP URL, broken custom domain, or pending certificate page.

### 2. Mobile Must Be Actually Tested

Video pitfall: mobile images overlapped, text overflowed, and buttons could not
be tapped.

SaaS translation:

- Test the app in Chrome DevTools mobile view and at least one real narrow
  viewport such as 360, 390, and 430 px width.
- Check landing page, sign-in flow, dashboard, pricing/payment page if present,
  and any result/download page.
- Verify tap targets, form fields, loading states, overflow, and fixed headers.

Avoid:

- Accepting a desktop screenshot as launch readiness.
- Only checking the homepage while dashboard or checkout remains broken.

### 3. Payment Needs A Fallback Path

Video pitfall: the site only connected Stripe; when Stripe review failed, users
could not pay.

SaaS translation:

- v1 of this skill still stays payment-free unless the user explicitly asks for
  a payment upgrade.
- When payment is requested, do not make the business depend on one unapproved
  rail. Prepare a fallback such as Paddle, Creem, PayPal, Stripe, or a manual
  invoice route depending on jurisdiction and product type.
- Payment approval should happen after the site has clear product description,
  policies, contact, delivery/access flow, and real public pages.

Avoid:

- Building Stripe-only checkout before account approval and trust pages exist.
- Treating a payment provider SDK install as the same thing as payable revenue.

### 4. Backups Are Part Of Launch Readiness

Video pitfall: server failure erased site content, products, and customer data.

SaaS translation:

- Source code must be in Git/GitHub.
- Supabase data needs a recovery plan: platform backup, SQL export, or documented
  manual export for tiny experiments.
- Environment variables and provider configuration need a secure inventory, not
  a single local `.env.local` that can disappear.
- For PostHog or analytics, know what is disposable and what must be exported.

Avoid:

- Saying "we are pre-revenue, backups can wait."
- Backing up code but not database rows, storage files, env var names, or
  customer/order records.

### 5. Legal And Trust Pages Are Commercial Infrastructure

Video pitfall: missing privacy policy, refund policy, and terms caused payment
review and customer-dispute problems.

SaaS translation:

- Before payment or customer-facing launch, include at least:
  - Privacy Policy
  - Terms of Service / Terms of Use
  - Refund or cancellation policy, even if the rule is "no refund after delivery"
  - Contact method
  - Clear delivery/access description
- For pure v1 demos without payment, legal pages can be recorded as launch gates
  rather than forced into the starter.

Avoid:

- Applying to payment providers with placeholder pages.
- Launching a paid SaaS with no refund, terms, contact, or privacy surface.

## Skill Rule Patch

When a user asks to launch, deploy publicly, collect payment, build an
independent site, or prepare a SaaS for customers, `one-person-saas-os` must run
the five risk gates before claiming launch readiness:

1. HTTPS/custom-domain check.
2. Mobile layout and tap-target check.
3. Payment fallback/readiness check when payment is in scope.
4. Backup/recovery check.
5. Legal/trust page check.

## Trigger Phrases

- `独立站避坑`
- `建站五个坑`
- `上线前检查`
- `客户建站交付`
- `SaaS 上线验收`
- `支付审核没过`
- `Stripe 被拒`
- `移动端按钮点不到`
- `没有法律页面`
- `网站备份`

## Preflight Action

Before customer-facing launch work:

1. Read `references/prelaunch-risk-gate-checklist-20260706.md`.
2. Check `references/deployment-checklist.md`.
3. If payment is requested, also read
   `references/payment-account-stripe-notes-20260705.md`.
4. If first-dollar distribution is requested, also read
   `references/first-dollar-launch-sop-20260705.md`.

## Failure Review Entry Point

If a launch fails because of HTTPS, mobile layout, payment approval, missing
backup, missing legal pages, or customer trust problems, record it in
`references/failure-review.md` under the launch-risk classification and then
update this file or the checklist so the failure cannot repeat silently.

## Acceptance Evidence

This lesson is considered deployed when:

- The analysis report exists in the active Codex output folder.
- This reference file exists in the skill package.
- The prelaunch checklist exists.
- `SKILL.md` references both files.
- `deployment-checklist.md` includes the customer-facing launch gates.
- `recent-use-log.md` records the update.
- A Knowledge Brain / Obsidian note records the new rule.
