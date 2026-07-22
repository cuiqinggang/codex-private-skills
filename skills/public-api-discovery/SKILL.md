---
name: public-api-discovery
description: Discover and compare public or free-tier APIs from a local read-only catalog. Use when a user asks to find, recommend, compare, or replace a public API; needs an external data source such as weather, maps, exchange rates, news, images, music, test data, geocoding, document processing, or machine learning; or asks for a no-key or CORS-compatible API. Do not trigger when one API is already fixed and only coding help is needed, local data is sufficient, or the request attempts to bypass payment, authentication, rate limits, or access controls.
---

# Public API Discovery

Use the local catalog only to discover candidates. Treat every catalog field as unverified until the current official documentation is opened and checked.

## Workflow

1. Classify the request with `scripts/route_public_api.py`. Exit on P0; mention the option once on P3.
2. Search `C:\AI\resources\public-apis\generated\public_apis_index.json` with `scripts/search_public_apis.py`.
3. Return only 3–8 candidates. Prefer HTTPS=Yes, low authentication cost, explicit CORS, clear documentation and active maintenance.
4. Label catalog-only facts as `目录信息（未复核）`.
5. Before recommending actual integration, open official documentation for the top 1–3 candidates and verify price/free tier, registration, authentication, rate limits, region restrictions, data license, privacy policy, terms, stability and commercial permission. Label those facts `已复核官方信息` and record the verification date.
6. Provide a minimal example only after verification and use environment-variable placeholders for secrets.
7. Never register, purchase, call, load-test or bypass controls on a third-party API without task-specific user authorization.

## Risk Gate

Raise the review threshold for finance, medical, legal, security, payment and identity use. Never select a production dependency in these areas from this catalog alone.

“Free” does not mean permanently free. The MIT license covers the catalog repository, not every listed API or its data.

Read `references/verification-checklist.md` before actual integration. Read `references/routing-policy.md` when trigger behavior is ambiguous. Record failures in `references/FAILURE-REVIEW.md` and material uses in `references/RECENT-USE-LOG.md`.

## Commands

```powershell
${REDACTED_SECRET}
${REDACTED_SECRET}
```

Update the catalog manually only when starting a new API-dependent project, the mirror is over 90 days old, many links fail, or the user explicitly requests it. Inspect upstream changes before `git pull --ff-only` and rebuild the index afterward.
