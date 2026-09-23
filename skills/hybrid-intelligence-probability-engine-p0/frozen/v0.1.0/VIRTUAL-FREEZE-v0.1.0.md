# 混合智能概率引擎 P0 v0.1.0 — Virtual Freeze

- Mother method: 整体闭环极限短时间引擎 v4.6
- Probability core: JEV Probability Engine P0 v0.4.0 (\`typesafe/jev-1.13\`), certified anchor \`T*=560.9819 ms\`, 30/30 PASS on PE-P0-GENERAL-01.
- High-intelligence baseline/residual: OpenAI \`gpt-5.6-sol\`, standard API path.
- P0 scope: canonical hybrid decision plane, not arbitrary Browser/Desktop/Search automation.

## Frozen runtime rule
1. Deterministic facts/rules -> CODE.
2. Only evidence-isomorphic JEV zone -> JEV: explicit state, finite Choice action ontology, no free-form generation, deterministic verifier, zero timed retry.
3. Everything else -> GPT residual.
4. JEV and GPT residual run concurrently where independent.
5. Final independent verifier defines VALID.
6. No JEV<->GPT oscillation. Failure -> Reality Delta -> STOP -> GPT page.

## Commercial gate
A candidate is VALID only when final verifier passes, critical uncaught errors are zero, and normalized hybrid list-cost is <= the same-task Full-GPT baseline. Only VALID candidates compete on wall-clock \`T_VALID\`.

## Evidence-bound comfort zone
v0.1.0 does not expand the production comfort zone to Noul/Score or unverified Choice shapes. Those remain future candidates despite public API support. The first reality certification tests only the Choice shape already evidenced by JEV P0 v0.4.0.

## Reality benchmark
A fixed 48-node canonical workload:
- 16 deterministic nodes;
- 24 semantic JEV Choice nodes over EXECUTE/HOLD/ROUTE/REJECT using natural-language request/evidence/constraints and a hidden deterministic oracle;
- 8 constructive regex-synthesis nodes routed to GPT and checked against positive/negative examples by a deterministic verifier.

Full-GPT baseline and Hybrid use the same public tasks and verifier. Hybrid runs two JEV shards plus one GPT-residual batch concurrently. One warmup is outside measured arrays; default measured runs = 10. All measured Full-GPT and Hybrid runs must be VALID. Hybrid normalized cost must not exceed Full-GPT baseline. Promotion additionally requires \`min(T_HYBRID) < min(T_FULL_GPT)\`.

## External-dependency closure
Auth availability is a measured reality property, not a design degree of freedom. Frozen environment variables: \`OPENAI_API_KEY\` and \`OPENROUTER_API_KEY\`. Missing auth -> exact Reality Delta and STOP; no probing of credential stores, no fallback model, no provider/model substitution.

## Time contract
Reality wrapper starts before the child runner and stops after the child has written the final result file and exited. Component timings are diagnostic only. The promotion metric is measured wall-clock \`T_VALID\` inside the fixed benchmark; process timing is separately reported.

## Freeze gate
\`VIRTUAL_MATURITY=PASS\` applies only to this P0 benchmark and runtime contract. It does not certify real performance. Reality may only execute the frozen files; any required design change returns to GPT.

## GPT/JEV commercial snapshot
For this freeze, normalized price constants are frozen to the current public model pages used on 2026-09-23:
- GPT-5.6 Sol: $4.00 / 1M input tokens, $20.00 / 1M output tokens.
- Jev 1.13 via OpenRouter: $0.042 / 1M input tokens, $0 output.
These constants are for normalized comparison only; actual account credits/discounts do not override the normalized commercial gate.

## Virtual evidence
The GPT-side structural self-test passed. Mock timings and mock costs are explicitly excluded from commercial/time promotion. Missing-auth failure injection returns a fixed Reality Delta and stops.