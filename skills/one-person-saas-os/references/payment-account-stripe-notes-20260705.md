# 收费账户 / Stripe 注意事项

## Core Position

Payment is not removed from the SaaS roadmap. It is moved to v2 because payment adds legal, KYC, tax, refund, chargeback, webhook security, and account-risk complexity. v1 should prove that the site, login, data, analytics, and dashboard can run. v2 adds Stripe after the business identity and website trust surface are ready.

## Absorbed First-dollar Case Notes

Friend case:

- Tried Paddle first with an older product before the new website was ready, and was rejected.
- Then chose Stripe.
- Personally went to Hong Kong to open a Hong Kong bank card.
- Reported experience: Hong Kong bank card plus mainland China passport was enough for his Stripe verification path.
- Key warning: apply for any payment provider only after the website is complete, the product/service is clear, and privacy policy, terms of service, and refund policy are present.

Skill interpretation:

- Treat this as a successful anecdote, not a universal guarantee.
- Do not apply with an unfinished or placeholder site.
- The website trust surface is part of payment approval, not a later polish step.
- Payment provider approval differs by country, business category, documents, and current policy.

## Paddle / Creem / Stripe Route

| Route | Best Fit | Advantage | Main Risk | Skill Guidance |
|---|---|---|---|---|
| Paddle | Digital products, SaaS, indie global sales | Merchant-of-record style flow can reduce tax/VAT burden | Review can reject weak or unfinished sites | Prepare complete website and policies before applying. |
| Creem | Indie SaaS and creator-style paid tools | Often discussed by makers as a lightweight option | Availability, category support, payout and review rules may change | Verify current support and fees before implementation. |
| Stripe | SaaS with supported legal/bank route | Flexible Checkout, subscriptions, webhooks, customer portal | KYC, jurisdiction, payout, disputes, tax, restricted categories | Use as v2 when legal route and website trust surface are ready. |

## What Opening A Stripe Account Usually Requires

Stripe's exact requirements differ by country/region. Based on Stripe support and documentation, opening an account in another country generally requires:

- Legal entity in that country/region.
- Tax ID or registration number where required.
- Physical location/address in that country/region.
- Phone number.
- Government-issued ID for representatives/owners.
- Business/entity documents.
- Bank account documents or verified payout bank.
- Relationship proof, such as ownership/directorship, when requested.
- A business category that is not prohibited and that satisfies any restricted-business review.
- Accurate, complete, and current account information.

Official references:

- Stripe global availability: `https://stripe.com/global`
- Requirements to open a Stripe account in another country: `https://support.stripe.com/questions/requirements-to-open-a-stripe-account-in-another-country`
- Acceptable verification documents: `https://docs.stripe.com/acceptable-verification-documents`
- Verification support topic: `https://support.stripe.com/topics/verification`
- Prohibited and restricted businesses: `https://stripe.com/legal/restricted-businesses`
- Stripe Services Agreement: `https://stripe.com/legal/ssa`

## Hong Kong Account Notes

For a Hong Kong Stripe route, do not assume passport alone is always enough. Treat this as a real-business setup:

- Hong Kong company or supported legal entity.
- Business registration / company documents.
- Real business address or verifiable physical location.
- Hong Kong or supported payout bank route.
- Representative/beneficial-owner identity documents.
- Website that clearly explains the product, pricing, refund, delivery/access, privacy, and contact method.

Do not set Hong Kong as the account country if the legal entity, address, documents, and operating reality do not match.

## Residential IP and Fingerprint Browser

Friend's note: registration and use were done with a fingerprint browser and Hong Kong residential IP to reduce IP risk.

Compliant interpretation:

- A stable, real, low-risk network environment can reduce false-positive risk compared with noisy datacenter VPNs or constantly changing IPs.
- If the business is genuinely Hong Kong based, logging in from a consistent Hong Kong residential/business network may look more consistent.
- A fingerprint browser can isolate work profiles and cookies so one payment account does not mix with unrelated browser sessions.

Do not use these as a way to bypass eligibility, fake country, hide the real operator, or submit mismatched documents. Stripe can request documents and verify account information. Inconsistent country, IP, bank, address, website, or identity signals can create review risk.

Important: You do not "write the IP" into Stripe forms. Stripe and other payment platforms observe login/network metadata automatically. The account country and business address should be the real legal/business setup, not whatever IP is being used that day.

## Practical v2 Payment Route

1. Finish v1 website: landing page, dashboard, health, analytics, product page, privacy, terms, refund policy, contact, delivery/access explanation.
2. Decide payment provider: Paddle, Creem, or Stripe.
3. Decide legal route: Hong Kong company/bank route, Stripe Atlas/US company route, or another supported jurisdiction. Pick the route that matches real documents and payout capability.
4. Apply only with accurate information and a complete website.
5. Add Checkout for a simple paid plan.
6. Add Customer Portal or equivalent billing-management flow.
7. Add secure webhook endpoint.
8. Store subscription/customer state in Supabase.
9. Gate paid features in dashboard based on Supabase subscription state.
10. Test with sandbox/test mode.
11. Deploy env vars to Vercel and test live payment with a low-risk real transaction.

## Website Trust Checklist Before Applying

- Product page explains what the user gets.
- Pricing page or clear payment explanation exists.
- Terms, privacy policy, refund/cancellation policy exist.
- Contact email/domain email exists.
- Demo, screenshots, docs, or onboarding exist.
- Business name and website match Stripe account information.
- No prohibited/restricted content or misleading claims.

## Why Payment Was Excluded From v1

v1 target: one generation, high success rate, low-stable deployment. Payment is excluded from generated v1 code because:

- Webhooks require signature verification and production endpoint security.
- Stripe account approval depends on KYC, business category, website quality, and jurisdiction.
- Payment introduces refunds, disputes, taxes, and subscription state.
- A broken payment integration is worse than no payment integration.

Therefore the skill keeps payment as v2: deliberately added after the base SaaS is online and the account route is legally consistent.
