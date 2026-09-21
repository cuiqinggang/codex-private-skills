# Reality Delta — Codex credential boundary

## Observed reality

The first STEP 3 attempt did not start the frozen benchmark.

Codex security policy blocked even a boolean existence check of `OPENROUTER_API_KEY` because credential access is outside the allowed automation boundary.

Observed result:

```text
RUNNER_FINAL_SUMMARY=NOT_STARTED
RESULT_PATH=NONE
```

Therefore:

```text
CANDIDATE_EXECUTED=NO
REALITY_RESULT=NOT_MEASURED
CANDIDATE_STATUS=UNCHANGED
VIRTUAL_99_STATUS=UNCHANGED
```

This is a validation-channel Reality Delta, not a candidate performance failure.

## Frozen correction

Do not change:
- candidate source;
- model;
- topology;
- payload design;
- scheduler;
- verifier;
- benchmark;
- T0/T1;
- promotion gate.

Only change responsibility boundary:

```text
USER POWERSHELL
  owns secret-bearing execution
  -> runs the already frozen runner exactly once

CODEX
  owns no credential
  -> performs post-run read-only evidence verification
  -> no network/API call
  -> no redesign
```

This correction belongs to STEP 2 because the STEP 3 execution channel required alteration after a Reality Delta.
