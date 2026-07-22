# Pricing and Cost Control

## Core Rule

Do not let free users run unlimited Full A/B/C/D.

The product can be generous, but it cannot be financially self-destructive.

## Free vs Paid

Recommended user-facing tiers:

| Tier | User label | Internal behavior |
|---|---|---|
| Free | Quick Answer | lightweight enhanced answer, no full A/B/C/D |
| Low paid | Deep Answer | partial multi-step answer, limited cost |
| Full paid | Best Answer | full A/B/C/D UltraFusion |

Alternative simple labels:

```text
Quick
Deep
Best
```

## Why Credits Are Better Than Unlimited Plans

Full A/B/C/D costs vary by:

- question length;
- number of models;
- output length;
- retries;
- verification depth;
- model provider pricing.

Therefore early pricing should use credits or answer packs rather than unlimited usage.

Example:

```text
Quick Answer: free quota
Deep Answer: 1 credit
Best Answer: 5-10 credits
```

Do not finalize exact credit pricing until test cost data exists.

## Cost Protection Rules

Use these from the beginning:

1. Free mode has daily quotas.
2. Full mode requires credits or payment.
3. Estimate cost before expensive runs where possible.
4. Record model usage and cost per layer.
5. Stop or downgrade when a provider fails.
6. Do not retry indefinitely.
7. Do not allow abusive long prompts in free mode.
8. Add queueing for slow expensive tasks.

## Payment Strategy

Current stage:

```text
Payment stack matters, but answer validation comes first.
```

Likely mature path:

- Stripe Checkout / Payment Links for early paid tests;
- Stripe Billing or credit ledger after demand is proven;
- merchant-of-record style provider later if global tax/compliance becomes hard.

The user has Hong Kong banking access, which may help with international payment setup. Final setup still requires provider eligibility and KYC verification.

## Refund and Failure Handling

If a paid Best Answer run fails:

- return credit automatically when no usable answer is produced;
- mark provider failure;
- store failed run logs;
- do not call it a successful answer.

## Success Metric

A paid tier is viable only if:

```text
average revenue per Best Answer > average model cost + payment fees + failure allowance
```

Early tests must calculate this, even with estimated cost.
