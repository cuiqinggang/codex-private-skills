# REAL-HANDOFF — HIPE P0 v0.1.1

## Label

【混合智能概率引擎｜冻结方案现实验证｜3｜实】

## Principle

Reality is still a frozen execution only.
No design, repair, model change, threshold change, benchmark change, fallback, or Virtual-99 is allowed here.

## Execution-boundary correction

Codex is allowed to:
- fetch/materialize the exact frozen source;
- verify exact commit and file hashes;
- read results after execution.

Codex is NOT allowed to:
- read, discover, request, print, or handle OPENROUTER_API_KEY;
- initiate paid OpenRouter inference;
- change the frozen design after any failure.

Credential-bearing network execution is performed only by the user-confirmed local GUI launcher:

HIPE-P0-v0.1.1-reality-launcher.pyw

The launcher:
- requires explicit user confirmation before paid requests;
- uses an inherited OPENROUTER_API_KEY or requests a one-run masked value;
- never writes the key to disk;
- starts outer Reality timing only after user confirmation/key entry;
- launches only HIPE-P0-v0.1.1-real-verify.py with --mode live --runs 10;
- removes stale result/evidence files before the run;
- reports child exit code, outer timing and RESULT_SHA256;
- ends with the four-field label using 实.

## Frozen runner

HIPE-P0-v0.1.1-real-verify.py

Fixed:
- mode=live
- runs=10
- GPT=openai/gpt-5.6-sol
- JEV=typesafe/jev-1.13
- GPT endpoint=https://openrouter.ai/api/v1/chat/completions
- JEV endpoint=https://openrouter.ai/api/alpha/decisions
- benchmark=48 nodes
- verifier=frozen
- pricing snapshot=frozen

## Failure policy

Any failure:
REAL_VALID=FAIL or NOT_TESTED
REALITY_DELTA=<exact observed delta>
ACTION=STOP
RETURN_TO_GPT=YES

No second attempt with a changed design.

## PASS evidence

A PASS must include at least:

REAL_VALID=PASS
COMMERCIAL_GATE=PASS
CRITICAL_UNCAUGHT_ERROR=0
T_FULL_GPT_MIN_MS
T_HYBRID_MIN_MS
T_FULL_GPT_P50_MS
T_HYBRID_P50_MS
COST_FULL_GPT_MIN_USD
COST_HYBRID_MAX_USD
S_ZONE_TIME
S_ZONE_COST
S_E2E_TIME
S_E2E_COST
OUTER_PROCESS_MS
RESULT_SHA256
REALITY_DELTA=NONE
ACTION=STOP
RETURN_TO_GPT=NO

Reality result must not be interpreted as certified until the frozen result/evidence is returned to the GPT page for closeout.
