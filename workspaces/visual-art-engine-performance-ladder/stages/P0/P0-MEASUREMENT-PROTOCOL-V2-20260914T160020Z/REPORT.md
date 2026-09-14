# P0 Measurement Protocol V2 — Authoritative A/A Stop Report

生产同路径统计 selftest 与 null Type-I calibration 均 PASS；Measurement Protocol V2 实现验收 PASS，但权威 A/A FAIL，因此候选锁保持 ON。

- `RUNNER_SHA=fcdae8b83d663a9185cc44a90d8b5c0bd91b6b8da069515a997f0167509f2c6b`
- `AA_VALID_RUNS=160`（80 A1 + 80 A2）
- `NULL_SIMULATION_ITERATIONS=20000`
- `NULL_POSITIVE_FALSE_KEEP_RATE=0.0222`
- `NULL_ANY_DIRECTION_REJECTION_RATE=0.04575`
- `FINAL_MDE_MS=4.4`
- `MDE_TARGET_POWER=0.80`，observed power=0.82245
- `ORDER_EFFECT_MS=-3.71155`
- `ORDER_EFFECT_95CI=[-8.0174,3.6105]`
- order state=`INCONCLUSIVE`，没有以 p>0.05 冒充等价。

同一实现的 formal block effect=3.24545 ms，95% CI=[0.579475,5.953475]，且超过 A/A noise floor 2.665975 ms，因此 `AA_CALIBRATION=FAIL`。环境 drift 门禁未触发；FAIL 来自测量标签/顺序体系仍产生可裁决假差异。

160/160 measured run 的原始 history 正文/SHA、exact prompt、completed/success、唯一输出、完整 PNG decode、256×256 与输出 SHA 全量复核通过。未运行任何候选。

`MEASUREMENT_PROTOCOL_V2=PASS`

`CANDIDATE_LOCK=ON`

`P0_99=NO / P0_FREEZE=NO / P1_UNLOCKED=NO`
