# P0 Measurement Protocol V2 — Statistical Repair Checkpoint

`MEASUREMENT_PROTOCOL_V2=STATISTICAL_REPAIR_IN_PROGRESS`

`FINAL_MDE_MS=UNKNOWN`

`AA_CALIBRATION=NOT_AUTHORITATIVE`

`CANDIDATE_LOCK=ON`

旧 AUTH-AA、shared-client、40B 和 80B 批全部保留为 `SUPERSEDED_BY_STATISTICAL_AUDIT`；原始证据不删除，但不得进入 FINAL_MDE 或候选裁决。

当前 runner SHA-256：`fcdae8b83d663a9185cc44a90d8b5c0bd91b6b8da069515a997f0167509f2c6b`。

纯统计生产同路径 selftest 已 PASS：20,000 次 null validation 的 positive false KEEP=0.01925、any-direction rejection=0.04025；null FAIL→MDE null、small/MDE/large gain、order、synthetic drift、固定 seed、独立 ABA cluster 与错误/共享 bracket 拒绝均通过。

下一步只允许在该 runner SHA 下运行新权威 A/A；不运行 E4/E5/E7/Track B。

`P0_99=NO`

`P0_FREEZE=NO`

`P1_UNLOCKED=NO`
