# Measurement Protocol V2（UNDER_VALIDATION）

## 使用条件

本协议用于 P0-P3 的毫秒级性能裁决。当前状态是 `UNDER_VALIDATION`；三门未同时 PASS 前只允许校准，不允许候选裁决。

## 成熟流程

1. 固定 workload、结果语义、计时边界、runner/workflow/fixture SHA 和环境；每次保存 monotonic 原始时间。
   权威记录必须同时包含 `RUNNER_SHA` 与 `HARNESS_MANIFEST_SHA`；后者确定性覆盖
   runner、两层启动器、decision rules、bracket summary、workflow 与 fixture。
   任一受覆盖文件变化，均视为新的 benchmark harness 身份。
2. 先跑完全同实现的 interleaved A/A；A1/A2 只能是逻辑标签，同生命周期、runner、HTTP session 与 warmed environment。
   A/B 标签只能存在于计时外 metadata，不得进入 workflow JSON、`filename_prefix`、
   HTTP path/query、计时内 raw/evidence 路径或 client/session identifier。归一化
   opaque run token 后的 A/B workflow SHA 必须 byte-equivalent，三类 label leak
   计数必须全部为 0。
3. 正式比较采用固定 seed 的 ABBA/BAAB 四次 block；block 是最小独立单元，禁止把 block 内 observations 当 IID。
4. null calibration 必须调用与生产 KEEP 相同的统计函数。正向 KEEP 定义为双侧 95% CI lower bound > 0；同时报告 `NULL_POSITIVE_FALSE_KEEP_RATE`（目标约 2.5%）与 `NULL_ANY_DIRECTION_REJECTION_RATE`（目标约 5%）。
5. null calibration PASS 后才计算 FINAL_MDE：在相同依赖结构和 KEEP 规则下达到 power≥0.80 的最小真实 gain，并保存完整 power curve。
6. order effect 使用独立 block-level contrast。`p>0.05` 不证明等价；只有 95% CI 完整落入 ±`0.5*FINAL_MDE` 才 PASS，否则按证据判 INCONCLUSIVE 或 FAIL。
7. 环境漂移使用同期 A 的时间顺序稳健趋势和置换检验；异常漂移写 `INVALID_ENVIRONMENT_DRIFT`，不得归罪 candidate。
8. 普通候选用同时期 paired A/B；短候选另做显式 `A_before,B,A_after` bracket。若 comparisons 共享 A，必须作为同一 cluster 重采样；优先让每个 ABA triple 独立。
9. KEEP 要求 100% 输出有效、正向 effect、正式 CI 不跨 0、超过 A/A noise 与 MDE，并有两个独立 confirmation batches 同向。
10. 低于 MDE 写 `INCONCLUSIVE_BELOW_MEASUREMENT_RESOLUTION`；只有稳健负向且超过 resolution 才 ROLLBACK。

三门是相互独立的串行门禁：统计 selftest 证明实现逻辑，null calibration 证明 Type-I error，A/A 证明真实执行环境与标签/顺序没有可裁决假差异。前两门 PASS 不能覆盖第三门 FAIL。

## 结果门禁

每 run 必须 exact prompt_id match、`completed=true`、`status_str=success`、唯一 expected output、完整 PNG zlib decode、固定尺寸与 SHA-256。保存原始 history response 正文或无损 JSON及其 SHA；失败不补跑、慢样本不删除。

## 冻结与升级

`STATISTICAL_SELFTEST=PASS` + `NULL_CALIBRATION=PASS` + `AA_CALIBRATION=PASS` 后冻结 V2，P1/P2/P3 默认复用。发现新缺陷时保留旧版本和全部证据，记录 repair reason/diff，产生新 runner SHA，重新完成三门。

## Windows evidence-path preflight

权威测试启动前必须实际创建并删除一个 deepest expected evidence path 探针，覆盖
Stage root、批次目录、最深子目录和最长文件名。若失败，正式批次不得启动；应改用
短、中性、label-blind evidence root。路径缩短不得改变 arm、workflow、order seed、
统计规则、workload 或计时语义。

## 当前权威 A/A（2026-09-15）

`AA_VALID_RUNS=160`，formal effect=`2.8688 ms`，95% CI=
`[-0.847625,6.585225]`，noise floor=`3.7609 ms`。旧 CI 全正假效应已消失，
`LABEL_BLIND_FIX_CAUSALLY_CONFIRMED=YES`。order effect=`6.619075 ms`，95% CI=
`[-3.081325,22.327025]`，未整体进入冻结等价区间，因此
`AA_CALIBRATION=INCONCLUSIVE / CANDIDATE_LOCK=ON`；不得启动候选。

## 2026-09-15 SEARCH_ONLY 与最终认证边界

新的独立 40-block A/A `a4` 虽然 formal CI 跨 0，但 frozen environment
drift gate 触发，最终为 `AA_CALIBRATION=FAIL`。按预声明停止继续扩张
calibration，候选仅作 SEARCH_ONLY。R6 的两个独立 confirmation 均有全正
paired CI，但这只能证明相对收益；在 A/A FAIL、candidate lock ON 且 pooled
absolute P50 慢于历史参考时，禁止写 KEEP、99 或 FREEZE。

成功态调度经验：SaveImage `executed` 后立即并发 history 与 `/view`
会争用发布路径；等待 matching `execution_success` 后先读取本地 bytes、
再确认 history，可保留完整语义并明显缩短控制链。HTTP/local byte equality
必须在计时后逐 run 验证，不能因移出计时而删除。
