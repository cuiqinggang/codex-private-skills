# Failure Review Entry Points

## AMBIGUOUS_REVIEWER_FAILURE

Trigger when a run says “GPT reviewed”, “AI audited”, or “review passed” without naming the actual reviewer and review mode.

Repair:

1. Stop the final `PASS` claim.
2. Declare `PRIMARY_CONTROLLER`, `MODEL_ROLE`, `REVIEW_MODE`, and `REVIEWER`.
3. If multi-agent support exists, create a new read-only-first review agent.
4. Otherwise rerun a second-pass checklist and label it `SELF_REVIEW_FALLBACK`.
5. Reopen all P0/P1 findings until evidence closes them.

## SURFACE_HANDOFF_CONTEXT_LOSS

Trigger when work is moved between Codex and ChatGPT Work without the original goal, evidence, constraints, or open risks.

Repair: generate a `WORK_HANDOFF_PACKAGE` with `FROM / TO / INPUT / OUTPUT / EVIDENCE / OPEN_RISKS / NEXT_GATE` and restart the external review from the original goal.

