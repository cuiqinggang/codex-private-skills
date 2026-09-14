# Measurement Protocol V2 Evidence Map

状态：`UNDER_VALIDATION`

Stage 根：`workspaces/visual-art-engine-performance-ladder/stages/P0/P0-MEASUREMENT-PROTOCOL-V2-20260914T160020Z/`

| RUN_ID / 结论 | GitHub path | Runner SHA | Commit SHA | Audit status |
|---|---|---|---|---|
| E8-E11 unchanged baseline drift | prior P0 convergence audit + current Stage references | `8c792c...` | `40527b7a2ff7477f3f0c91db2aa3cb2a5002403c` | confirmed historical evidence |
| AUTH-AA | `authoritative-runs/AUTH-AA` | preserved in batch identity | `11445741477d024a764eaa5a4ad796a1d7672d0e` | `PILOT_CALIBRATION_ONLY / INCONCLUSIVE_ORDER_EFFECT` |
| AUTH-AA-40B-V2 / AUTH-AA-80B-V2 | `authoritative-runs/` | `52357b5b...` | `11445741477d024a764eaa5a4ad796a1d7672d0e` | `SUPERSEDED_BY_STATISTICAL_AUDIT` |
| null false-positive 11.185% finding | `statistical-selftest.json`, audit record and superseded batch | superseded runners | `11445741477d024a764eaa5a4ad796a1d7672d0e` | audit confirmed invalid MDE pipeline |
| current statistical repair | `decision-rules.json`, `scripts/run_measurement_v2.py`, `scripts/bracket_summary.py` | `fcdae8b83d663a9185cc44a90d8b5c0bd91b6b8da069515a997f0167509f2c6b` | `11445741477d024a764eaa5a4ad796a1d7672d0e` | `UNDER_VALIDATION / STATISTICAL_SELFTEST_PASS` |
| AUTH-AA-STAT-FINAL-40B | `authoritative-runs/AUTH-AA-STAT-FINAL-40B/` | `fcdae8b83d663a9185cc44a90d8b5c0bd91b6b8da069515a997f0167509f2c6b` | pending final A/A sync | `NULL_CALIBRATION_PASS / AA_CALIBRATION_FAIL / CANDIDATE_LOCK_ON` |

每次重要审计/修复后更新本表；commit 产生后把 pending 值替换成实际 SHA。原始 history/PNG/null distribution 不复制进技能包。
