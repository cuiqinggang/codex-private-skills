---
name: aios-skill-self-purification-governance
description: Use when running or installing AI Company OS / AIOS skill self-purification governance, SkillOpt reviews, weekly 30min skill checks, monthly 2H sample optimization, quarterly 4H governance, runtime-gated skill audits, accepted/rejected/needs-human patch buffers, do-not-auto-optimize policies, or any semi-automatic skill cleanup that must not auto-merge formal skills.
---

# AIOS Skill Self Purification Governance

Use this skill to govern long-term SkillOpt / AIOS skill self-purification. It preserves the successful V3 runtime-enforced workflow as a reusable mechanism.

## Non-Negotiables

1. Do not modify formal business skills during governance setup.
2. Do not auto-apply accepted candidates.
3. Generate candidate patches only.
4. Preserve `ACCEPTED_CANDIDATE`, `REJECTED_EDIT`, and `NEEDS_HUMAN_REVIEW`.
5. Preserve runtime gates for 30min, 2H, 4H, and 8H runs.
6. Preserve the do-not-auto-optimize list.
7. Never allow unattended auto-merge into formal skills.

## When Running Governance

- For major project closure or weekly checks, use `COMMAND-30MIN-LIGHT-CHECK.md`.
- For monthly sample optimization, use `COMMAND-MONTHLY-2H-SAMPLE-OPTIMIZATION.md`.
- For quarterly graph governance, use `COMMAND-QUARTERLY-4H-GRAPH-GOVERNANCE.md`.
- Before declaring PASS, read `ACCEPTANCE-GATE.md`.

## Runtime Gate

Use `RUNTIME-GATE-USAGE.md` and the runtime verifier from:

```text
${REDACTED_SECRET}
```

Runtime enforced tasks require `runtime-evidence.json`, checkpoint timeline, and enough elapsed time. Patch installation can finish quickly but must not pretend to be a runtime PASS.

## V3 Source Evidence

The successful V3 run:

```text
Task: AIOS_SKILLOPT_2H_SAMPLE_OPTIMIZATION_RUNTIME_ENFORCED_RERUN_V3
Elapsed: 120.02 minutes
Checkpoints: 9
Runtime gate: PASS
Formal skills modified: NO
```

Evidence root:

```text
HISTORY_ONLY: AIOS-SKILLOPT-2H-RUNTIME-ENFORCED-RERUN-20260614 (never use H as runtime input; require current C-drive evidence)
```

