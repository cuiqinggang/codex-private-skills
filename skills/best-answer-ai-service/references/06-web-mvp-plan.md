# Web MVP Plan

## Product Shape

The MVP should be one web service, not an app.

Minimum useful page:

```text
Best Answer AI
Not a bigger model. A better answer process.

[Question input box]
[Mode selector: Quick / Deep / Best]
[Submit button]
```

## First Output Format

Use a final-answer report format:

```text
Final Answer
Why this is the best current answer
Key assumptions
Counterarguments
Risks and caveats
Confidence
What would change the answer
Next action
```

Avoid making the result look like a generic chat reply.

## Suggested Stack

Use mature and common tools:

```text
Next.js
Vercel or Cloudflare Pages
Supabase for database/auth
Stripe for payments
OpenRouter or direct model APIs
Queue for slow Full A/B/C/D jobs
```

Do not over-optimize stack before validation.

## MVP Modes

### Quick Answer

Purpose:

- free experience;
- fast;
- show value without burning cost.

Output:

- answer;
- assumptions;
- one counterargument;
- confidence.

### Deep Answer

Purpose:

- low-cost paid or limited free trial;
- partial multi-step improvement.

Output:

- stronger structure;
- counterarguments;
- decision notes;
- confidence.

### Best Answer

Purpose:

- full paid high-value answer.

Internal:

```text
Full UltraFusion A/B/C/D
```

Output:

- polished final answer;
- evidence-aware reasoning;
- strongest counterarguments;
- final recommendation.

## Queue Requirement

Full A/B/C/D can be slow. It should not be treated like an instant chat call.

Show:

```text
Your Best Answer is being prepared.
Estimated time: 3-8 minutes.
```

Use email or account history for long runs if needed.

## What to Avoid

Do not build:

- mobile app;
- multi-page marketing site;
- complex dashboard;
- community features;
- plugin marketplace;
- team workspace;
- expensive design system.

First prove:

```text
input -> answer -> user says this is better -> user may pay
```
