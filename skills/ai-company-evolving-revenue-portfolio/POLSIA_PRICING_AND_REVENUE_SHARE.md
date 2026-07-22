# Polsia Pricing And Revenue Share

## Public Price Observed

Lowest public paid price observed: $49/month.

Public evidence says this covers one company and daily autonomous operation. Public frontend FAQ text says $49/month includes 1 company, 30 night shifts, and 5 task credits. Product Hunt maker comments also describe daily cycles across engineering, marketing, and operations.

## Credits / Task Allowance

Observed public claims:

- 5 task credits are included in the base plan.
- Task tiers can be upgraded for additional monthly cost.
- Product Hunt user feedback described cold outreach as a task that consumed 10 credits.

Interpretation:

- Credits represent full agentic tasks, not simple token usage.
- Credit cost and exact dashboard metering need login/paid confirmation.

## Revenue Share Evidence

Product Hunt maker reply states that Polsia takes 20% on revenue. Public FAQ text says the 20% applies when revenue is withdrawn.

Terms evidence shows:

- Customer payments are processed through Stripe.
- Stripe fees apply in addition to Polsia's platform fee.
- Refunds/disputes deduct the full gross amount from company balance, including any platform fee already retained.

## Revenue vs Net Profit

The 20% is more like gross revenue/customer-payment share than net profit share.

Reasons:

- It is described as revenue, not profit.
- Terms use customer payments and gross amount language.
- No public evidence says fulfillment cost, ad spend, labor, taxes, refunds, or Stripe fees are deducted before the 20%.

## Advertising Fee

Terms say advertising uses platform-managed ad accounts when enabled. Users set a daily budget. Polsia may spend up to the configured daily budget and charge an additional platform fee currently equal to 20% of the daily budget.

Ad spend is charged daily through Stripe using the saved payment method. This is separate from the revenue-share/payment layer.

## Stripe Connect

Withdrawals require Stripe Connect Express and identity verification. This makes the model US/Stripe-compatible by default and not automatically suitable for Chinese private-traffic products.

## Business Fit

Better fit:

- High-margin digital products.
- SaaS, templates, courses, paid communities, newsletters, lightweight services.
- Offers where support and fulfillment can be bounded.

Poor fit:

- Low-margin physical goods.
- High-refund or dispute-prone products.
- Businesses with large ad spend before revenue.
- Offline fulfillment or heavy service delivery.
- Regulated fields where AI-generated claims create legal risk.

## Local Reproduction Rule

Do not reproduce Stripe/revenue-share automation in Phase 1. Use a manual ledger first:

- Track revenue source.
- Track ad spend.
- Track refund risk.
- Track human-approved payouts.
- Keep payment collection outside automation until compliance is reviewed.
