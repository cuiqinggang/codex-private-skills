# Stage Gate Checklist

Before work:

- [ ] Load `mature-replication-four-column` and verify metadata `4.0.0`.
- [ ] Read `state/CURRENT-STATE.md` and `state/STAGE-LEDGER.json`.
- [ ] Confirm the target stage is unlocked.
- [ ] Confirm the TASK contract and timing start/end are frozen.
- [ ] Keep certification outside runtime timing unless the TASK explicitly includes it.
- [ ] Confirm no H/K access, environment mutation, dependency install, or protected-skill edit is implied.

Before optimization:

- [ ] CURRENT has real repeated measurements.
- [ ] EXTERNAL FRONTIER has sources and comparability.
- [ ] T_PHY/T_PHY_RANGE has an auditable derivation.
- [ ] ITERATIVE CONVERGENCE is unlocked.
- [ ] Exactly one local hypothesis is selected.

Before freeze:

- [ ] All results passed RESULT_VALIDITY_GATE.
- [ ] No changed TASK result entered the baseline.
- [ ] Comparable faster external results are resolved.
- [ ] PHYSICAL_GAP is recorded.
- [ ] Previous stable, fallback and archive are preserved.
