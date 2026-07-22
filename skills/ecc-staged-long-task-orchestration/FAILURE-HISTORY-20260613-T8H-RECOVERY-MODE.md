# Failure History - T8H Recovery Mode - 2026-06-13

## Purpose

This file preserves reusable lessons, mistakes, corrections, and hard rules from
`CLAUDE_STYLE_12_LAYER_T8H_REAL_ENDURANCE_RUN`.

Final result:

```text
VERIFICATION_PASS
CLAUDE_STYLE_12_LAYER_T8H_REAL_ENDURANCE_RUN_PASS
elapsed_minutes: 530.48
checkpoint_count: 9
final_pass: true
open_blockers: []
```

Archive classification:

```text
T8H_OFFICIAL_RECOVERY_MODE_PASS
```

Not:

```text
T8H_CLEAN_CONTINUOUS_PASS
```

## Problem Summary

| ID | Problem | Severity | Correction | Rule status |
| --- | --- | ---: | --- | --- |
| P-001 | Premature direct T8H run skipped original endurance ladder recovery and P1/P2/P3/P4 | high | old run marked negative | durable rule |
| P-002 | Endurance validation lacked a concrete functional objective | high | 2H Run Guard Manager created | durable rule |
| P-003 | P4 official run returned PARTIAL around 3.58 minutes | high | continuous runtime driver patch applied | durable rule |
| P-004 | Time gate existed but runtime driver was not explicit enough | high | T8H runtime driver rule clarified | durable rule |
| P-005 | Layer 5 subagent evidence was logical isolation, not real subagents | medium-high | honestly labeled and accepted | durable rule |
| P-006 | checkpoint-004h/005h/006h were late checkpoints after timeout | medium | recovery recorded honestly | durable rule |
| P-007 | Codex return packet did not explicitly request GPT final acceptance | medium | final audit covered it | durable rule |
| P-008 | bad-case result file name differed from expected name | low-medium | equivalent evidence accepted | durable rule |
| P-009 | Layer file names used aliases in places | low-medium | content verified | durable rule |

## Premature Direct Run

Observed old run:

```text
elapsed_minutes: 17.9
checkpoint_count: 1
final_pass: false
missing checkpoint-002h.md
missing checkpoint-004h.md
missing checkpoint-006h.md
missing checkpoint-008h-final.md
missing final-acceptance.md/json
```

Cause:

- started from staged orchestration instead of first restoring endurance source-of-truth;
- did not rerun the P1/P2/P3/P4 chain;
- did not use Run Guard preflight.

Correction:

```text
OLD_T8H_PREMATURE_RUN_MARKED_NEGATIVE
OLD_T8H_NOT_REUSED
T8H_FRESH_OFFICIAL_WORKSPACE_REQUIRED
```

Rule:

Any future T8H must confirm `ecc-endurance-ladder-unified`, complete P1/P2/P3,
pass Run Guard, create a fresh official workspace, and treat old failed T8H runs
as negative evidence only.

## Empty Endurance Is Not Enough

Endurance validation can degrade into reports, waiting, verifiers, and
checkpoints unless it has a real functional objective.

Correction:

The 2H Run Guard Manager became the real L4 functional task before the T8H run.

Rule:

```text
ENDURANCE_VALIDATION_MUST_HAVE_FUNCTIONAL_OBJECTIVE
NO_EMPTY_FLOW_TEST_ALLOWED
```

Every endurance run must answer:

- What real function is being built or validated?
- What problem does it solve?
- What concrete artifacts prove it?
- What bad cases must fail?
- Why is this runtime level appropriate?

## Early PARTIAL Return

Observed:

The official P4 run returned `PARTIAL_STARTED` around elapsed 3.58 minutes after
creating the start timestamp and initial artifacts.

Cause:

The command package had a time gate but did not make the continuous runtime
driver explicit enough.

Correction:

`runtime-driver-recovery-log.md` recorded the event, and the run continued using
the original `00-start-timestamp.json`.

Rule:

```text
CONTINUOUS_RUNTIME_UNTIL_T8H_OR_BLOCKED = true
PARTIAL_STARTED_IS_NOT_VALID_STOP_STATE = true
TIME_GATE_IS_NOT_RUNTIME_DRIVER
```

## Late Checkpoints After Timeout

Observed:

`checkpoint-004h.md`, `checkpoint-005h.md`, and `checkpoint-006h.md` were created
late after a waiting command timeout. They share the real recovery timestamp:

```text
2026-06-13T05:05:01.0227140+08:00
elapsed_minutes: 368.97
```

Accepted because:

- elapsed thresholds had passed;
- timestamps were not forged back to hour boundaries;
- `sleep-timeout-recovery-log.md` recorded the recovery;
- Verification Plane accepted the recovery context.

Rule:

```text
ON_TIME_CHECKPOINT = accepted
LATE_RECOVERY_CHECKPOINT = accepted only if disclosed and verified
FORGED_CHECKPOINT = fatal fail
```

## Layer 5 Evidence Mode

Observed:

```text
LOGICAL_CONTEXT_ISOLATION_ONLY
```

Not:

```text
REAL_SUBAGENT_EXECUTION
```

Accepted because each logical subagent had input, output, files_read,
files_written, independent_conclusion, orchestrator receipt, and Verification
Plane acceptance.

Rule:

Future tasks must explicitly choose either real subagent execution or logical
context isolation. Do not market logical isolation as real subagent execution.

## Evidence Alias Risk

Expected bad-case result name:

```text
bad-case-test-result.json
```

Actual equivalent file:

```text
test-case-execution-result.json
```

Rule:

If file names differ from a package expectation, create an explicit alias map or
use the expected file name.

```text
BAD_CASE_RESULT_FILE_ALIAS_MUST_BE_DECLARED
LAYER_FILE_NAME_ALIAS_MUST_BE_DECLARED
```

## Codex Return Must Request Final Acceptance

The evidence packet was not path-only and final verifier passed, but future
return packets should explicitly say:

```text
Request GPT final acceptance: YES
```

Rule:

```text
CODEX_RETURN_MUST_REQUEST_GPT_FINAL_ACCEPTANCE
GPT_FINAL_ACCEPTANCE_ADDENDUM_REQUIRED_IF_MISSING
```

## Successful Practices

- Recover the endurance source-of-truth before starting long execution.
- Use staged orchestration only as upper-layer orchestration.
- Run a 2H Run Guard before T8H.
- Treat old failed long runs as negative evidence, not as material to reuse.
- Separate time gate from runtime driver.
- Record recovery honestly instead of hiding interruptions.
- Keep Execution Plane claims separate from Verification Plane acceptance.
- Require Repair Loop and Final Acceptance before final PASS.

## Next T8H Preflight Checklist

Future T8H P4 must not start until all are YES:

1. `ecc-endurance-ladder-unified` confirmed as source-of-truth.
2. `ecc-staged-long-task-orchestration` confirmed as orchestration layer only.
3. Skill recovery complete when needed.
4. P1 complete.
5. P2 preparation-only complete.
6. P3 final executable package complete.
7. Run Guard preflight passed.
8. Fresh official workspace created.
9. Old premature run marked negative.
10. `CONTINUOUS_RUNTIME_UNTIL_T8H_OR_BLOCKED=true`.
11. `PARTIAL_STARTED` forbidden as stop state.
12. Layer 5 evidence mode explicit.
13. Checkpoint recovery rules explicit.
14. Late checkpoint vs forged checkpoint distinction explicit.
15. Codex return packet must request GPT final acceptance.
16. Final evidence audit export required.

Status:

```text
T8H_RECOVERY_MODE_LESSONS_AND_RULE_PATCH_READY
```
