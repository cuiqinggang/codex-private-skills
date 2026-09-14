# Measurement Protocol V2（UNDER_VALIDATION）

## 使用条件

本协议用于 P0-P3 的毫秒级性能裁决。当前状态是 `UNDER_VALIDATION`；三门未同时 PASS 前只允许校准，不允许候选裁决。

## 成熟流程

1. 固定 workload、结果语义、计时边界、runner/workflow/fixture SHA 和环境；每次保存 monotonic 原始时间。
2. 先跑完全同实现的 interleaved A/A；A1/A2 只能是逻辑标签，同生命周期、runner、HTTP session 与 warmed environment。
3. 正式比较采用固定 seed 的 ABBA/BAAB 四次 block；block 是最小独立单元，禁止把 block 内 observations 当 IID。
4. null calibration 必须调用与生产 KEEP 相同的统计函数。正向 KEEP 定义为双侧 95% CI lower bound > 0；同时报告 `NULL_POSITIVE_FALSE_KEEP_RATE`（目标约 2.5%）与 `NULL_ANY_DIRECTION_REJECTION_RATE`（目标约 5%）。
5. null calibration PASS 后才计算 FINAL_MDE：在相同依赖结构和 KEEP 规则下达到 power≥0.80 的最小真实 gain，并保存完整 power curve。
6. order effect 使用独立 block-level contrast。`p>0.05` 不证明等价；只有 95% CI 完整落入 ±`0.5*FINAL_MDE` 才 PASS，否则按证据判 INCONCLUSIVE 或 FAIL。
7. 环境漂移使用同期 A 的时间顺序稳健趋势和置换检验；异常漂移写 `INVALID_ENVIRONMENT_DRIFT`，不得归罪 candidate。
8. 普通候选用同时期 paired A/B；短候选另做显式 `A_before,B,A_after` bracket。若 comparisons 共享 A，必须作为同一 cluster 重采样；优先让每个 ABA triple 独立。
9. KEEP 要求 100% 输出有效、正向 effect、正式 CI 不跨 0、超过 A/A noise 与 MDE，并有两个独立 confirmation batches 同向。
10. 低于 MDE 写 `INCONCLUSIVE_BELOW_MEASUREMENT_RESOLUTION`；只有稳健负向且超过 resolution 才 ROLLBACK。

## 结果门禁

每 run 必须 exact prompt_id match、`completed=true`、`status_str=success`、唯一 expected output、完整 PNG zlib decode、固定尺寸与 SHA-256。保存原始 history response 正文或无损 JSON及其 SHA；失败不补跑、慢样本不删除。

## 冻结与升级

`STATISTICAL_SELFTEST=PASS` + `NULL_CALIBRATION=PASS` + `AA_CALIBRATION=PASS` 后冻结 V2，P1/P2/P3 默认复用。发现新缺陷时保留旧版本和全部证据，记录 repair reason/diff，产生新 runner SHA，重新完成三门。
