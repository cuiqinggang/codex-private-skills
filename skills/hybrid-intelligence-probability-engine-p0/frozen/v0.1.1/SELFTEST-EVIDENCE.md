# HIPE P0 v0.1.1 — GPT-side Prevalidation Evidence

## Triggering Reality Delta

The prior v0.1.0 Reality attempt did not execute the frozen paid-network runner.

REAL_VALID=NOT_TESTED
REALITY_DELTA=FROZEN_RUNNER_DENIED_BY_AUTO_REVIEW_CREDENTIAL_AND_PAID_NETWORK_ACTION
RESULT_SHA256=NOT_CREATED
OUTER_PROCESS_MS=189343.144

This is classified as execution-boundary failure, not HIPE algorithm/performance failure.

## GPT-side benchmark audit

- TOTAL_NODES=48
- DETERMINISTIC_NODES=16
- JEV_CHOICE_NODES=24
- GPT_REGEX_NODES=8

Deterministic threshold oracle:
16/16 PASS.

JEV semantic oracle:
The six unique cases resolve to:
EXECUTE / HOLD / HOLD / ROUTE / REJECT / HOLD.
They repeat four times in the frozen benchmark.
24/24 semantic oracle check PASS.

GPT constructive regex residual:
8/8 deterministic verifier PASS using valid patterns for the frozen positive/negative examples.

## Public contract check — 2026-09-24

Verified against current OpenRouter public material:

- GPT model ID: openai/gpt-5.6-sol
- GPT chat endpoint: https://openrouter.ai/api/v1/chat/completions
- GPT response_format supports JSON object / structured output
- Jev model ID: typesafe/jev-1.13
- Jev Decisions endpoint: https://openrouter.ai/api/alpha/decisions
- Choice answers expose answers.<id>.choice
- Jev usage includes cost/input-token information
- GPT normalized snapshot: $2/M input, $10/M output
- Jev normalized snapshot: $0.042/M input, $0 output

No paid inference was performed by this GPT-side check.

## Local structural verification

Candidate runner:
HIPE-P0-v0.1.1-real-verify.py

Python compile:
PASS

Selftest:
STRUCTURAL_SELFTEST=PASS
COMMERCIAL_GATE=NOT_EVALUATED_IN_SELFTEST
CRITICAL_UNCAUGHT_ERROR=0

Missing-auth injection:
REAL_VALID=FAIL
REALITY_DELTA=OPENROUTER_AUTH_MISSING
ACTION=STOP
RETURN_TO_GPT=YES

Candidate runner SHA256 from GPT-side test build:
C5400C1E47C96EB34FCDD1D539EE4128455B267F3A9F5C7312BA5B26B0D93B17

Candidate GUI launcher syntax compile:
PASS

Candidate launcher SHA256 from GPT-side test build:
D4FE6BF6AB1BAACA324B8F230CFE083D791F9D8A3AF52878B9C48095B1A8A42F

Git content must be re-read after final closeout; Git blob SHA and local SHA256 are different identifiers.

## v0.1.1 hardening

Added controlled Reality Delta classes for:
- auth rejected
- payment required
- rate limit
- upstream HTTP failure
- generic HTTP failure
- network error
- timeout
- invalid JSON
- response schema failure
- GPT parse/schema/usage failure
- JEV parse/schema/usage failure
- unclassified runtime exception

Added:
CRITICAL_UNCAUGHT_ERROR
S_E2E_COST

No benchmark/model/endpoint/runs/Verifier change was introduced.

## Gate

VIRTUAL_PREVALIDATION=PASS
STRUCTURAL_SELFTEST=PASS
PAID_NETWORK_INFERENCE=NOT_RUN_IN_VIRTUAL
REALITY_CERTIFICATION=PENDING
