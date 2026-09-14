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
| AUTH-AA-STAT-FINAL-40B | `authoritative-runs/AUTH-AA-STAT-FINAL-40B/` | `fcdae8b83d663a9185cc44a90d8b5c0bd91b6b8da069515a997f0167509f2c6b` | `09c2b56` | `NULL_CALIBRATION_PASS / AA_CALIBRATION_FAIL / CANDIDATE_LOCK_ON` |
| first label-blind repair | `scripts/run_measurement_v2.py` historical repair state | `8f5c3a592ba18a0570b5213996bdbb4f9618f178d0bd80af16f0c56e912d4062` | `UNCOMMITTED_INTERMEDIATE / preserved in audit` | `SUPERSEDED_LABEL_BLIND_RUNNER` |
| A/A arm-label leakage audit | `harness-root-cause-label-leak/ROOT-CAUSE-AUDIT.md`, `harness-manifest-label-blind.json` | `c43875c3db879a589156b249756c240dd025452942461128a9093a90392d0d54` | `3d4ef1c8e2c32c05c5400b019335dd4c1dca3aa6` | `HARNESS=81974d60e1aa54bac03e0d5c27556d87b4ff4e52e742d9e36156998de4b807bf / CURRENT_LABEL_BLIND_RUNNER / SELFTEST_PASS / FRESH_AA_BLOCKED_RUNTIME_PERMISSION` |
| AUTH-AA-LABEL-BLIND-40B-20260915 | `aa-lb-v3/paired-results.json` and complete `aa-lb-v3/` raw corpus; summary `references/AA-LABEL-BLIND-20260915.md` | `c43875c3db879a589156b249756c240dd025452942461128a9093a90392d0d54` | raw checkpoint `a5bb79c716bf28fa85f2b901afb3ed79df8b7c62`; evidence content `2bb023aac8c960ef0fb19f5d23eea112bc5f93bc` | `160/160 VALID / EFFECT=2.8688 / CI=[-0.847625,6.585225] / NOISE=3.7609 / ORDER_CI=[-3.081325,22.327025] / AA_INCONCLUSIVE / LABEL_FIX_CONFIRMED / LOCK_ON` |
| AUTH-AA-LABEL-BLIND-INDEPENDENT-40B | `a4/` | `c43875c3db879a589156b249756c240dd025452942461128a9093a90392d0d54` | final evidence commit pending | `160/160 VALID / EFFECT=-1.469375 / CI=[-3.10655,0.1678] / NOISE=1.637175 / ORDER_CI=[-0.839375,5.72315] / ENV_DRIFT_FAIL / AA_FAIL / LOCK_ON` |
| R6 search + two confirmations | `r6a/`, `r6c1/`, `r6c2/`, `P0-99-CERTIFICATION-STATUS-20260915.md` | candidate `33521ffba52d676fdb3dc1245e554aa44e31f3ae4602d31b20d2ba1f0cd319c7` | final evidence commit pending | `SEARCH_ONLY / 240/240 VALID / CONFIRMATION_EFFECTS=11.451175,8.465825 / BOTH_CI_POSITIVE / POOLED_B_P50=41.5258 / P0_99_NO` |

每次重要审计/修复后更新本表；commit 产生后把 pending 值替换成实际 SHA。原始 history/PNG/null distribution 不复制进技能包。
