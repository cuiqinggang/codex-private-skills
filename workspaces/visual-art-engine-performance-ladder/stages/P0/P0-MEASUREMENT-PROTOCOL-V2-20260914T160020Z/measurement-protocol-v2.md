# P0 Measurement Protocol V2

状态：`STATISTICAL_REPAIR_IN_PROGRESS / FINAL_MDE_UNKNOWN / AA_NOT_AUTHORITATIVE / CANDIDATE_LOCK_ON`

本协议替代“历史固定 baseline + 单批 candidate + 2% Median”作为新裁决方法，但不删除或篡改任何旧实验。`CURRENT_OFFICIAL_BASELINE_MS=32.55975` 仅保留为历史正式值，不再作为微优化裁决分母。

## 固定任务与有效性

- workload：`LoadImage -> SaveImage`，输入为固定 256×256 PNG。
- 每次必须有唯一 prompt、matching completed history、唯一 SaveImage 输出。
- 输出必须属于该 prompt，PNG CRC 与完整 zlib 解码通过，尺寸为 256×256，并记录 SHA-256。
- 不跳过真实执行、history 或验证；不减少工作量；失败不补跑；慢样本不删除。
- 权威 A/A 使用 3 次公共 warmup，不进入正式统计；随后固定至少 40 个四次 block，共 80 A + 80 B attempts。

## 同期配对

固定 seed 在 `ABBA` 与 `BAAB` 之间生成平衡顺序。每个四次 block 形成两个方向校正的相邻 pair：`ABBA` 为 `pos1-pos2`、`pos4-pos3`；`BAAB` 为 `pos2-pos1`、`pos3-pos4`。

统一定义 `delta = A_time - B_time`，正值代表 B 更快。bootstrap 以完整四次 block 为重采样单元，不能把共享环境的 40 对误当独立 IID。

## A/A 校准

A1/A2 调用完全相同实现；标签只能进入元数据，不能进入执行分支。必须记录 runner、workflow、fixture、验证器和计时边界的 SHA-256 身份证明。

A/A、E4、E7 与 Track B 的两臂使用同一 client_id，消除无关身份差异；E5 因 B 的持久 WebSocket 与 A 的短连接同时存在，必须使用隔离 client_id 防止事件争用，并将该差异作为候选语义的一部分报告。

- `AA_NOISE_FLOOR_MS`：对 A/A block 做标签交换（block sign-flip）零分布后，`abs(median(delta*))` 的 95 分位。
- `MINIMUM_DETECTABLE_EFFECT_MS`：在相同 block 数、相同 bootstrap CI 与 KEEP 判定器下，对中心化 A/A block 残差注入正向效应；在预注册网格上达到至少 80% power 的最小效应。
- 正式统计管线为 `BLOCK_SIGN_RANDOMIZATION_LOCATION_CI`：先把每个四次 block 的两个 paired delta 合成一个 block 中位，再跨 block 取中位；所有符号随机化均作用于完整 block。正式正向 KEEP 判据是双侧 95% CI 的 lower bound 严格大于 0。
- null calibration 使用固定且相互独立的 calibration seed 与 validation seed，各按冻结的 20,000 次 block-sign randomization 运行同一生产函数。必须同时报告 positive false KEEP（目标单侧 2.5%，容差 1.5%–3.5%）与 any-direction rejection（目标双侧 5%，容差 4%–6%）。
- 只有 null calibration PASS 后才计算 MDE。MDE 是同一 null validation 分布在生产 lower-bound KEEP 判据下，达到至少 80% power 的最小注入真实 gain；保存完整 effect-size→observed-power curve。
- Order effect 使用每个四次 block 的 paired-delta 中位作为独立 contrast。保存 effect、20,000 次 block bootstrap CI 和 exact/randomization permutation p。等价界限为 `0.5 * FINAL_MDE_MS`；只有整个 CI 落入等价区间才 PASS，越界但证据不足为 INCONCLUSIVE，充分越界为 FAIL。
- A/A 为三态：`PASS`、`FAIL`、`INCONCLUSIVE`。`p >= 0.05` 绝不自动等于 PASS；order-effect CI 未整体进入等价界且也未充分越界时为 `INCONCLUSIVE`，只能增加 A/A blocks。
- 任一 attempt 无效、实现身份不一致、paired bootstrap CI 不含 0，或环境漂移以冻结检验充分成立，则 `AA_CALIBRATION=FAIL`；顺序项按上述等价性三态单独裁决。只要总体不为 PASS 就停止候选裁决。

## 候选裁决

- `KEEP`：100% 有效；gain > 0；block-bootstrap 95% CI 全大于 0；gain 同时超过 noise floor 与 MDE；随后两个独立 confirmation batch 方向一致，且合并 block-bootstrap CI > 0。
- `INCONCLUSIVE_BELOW_MEASUREMENT_RESOLUTION`：`abs(gain) < MDE`。
- `INVALID_ENVIRONMENT_DRIFT`：同期 A 的 Theil–Sen 预测全程漂移超过 MDE，且 10,000 次时间顺序置换检验双侧 p < 0.05。early-vs-late 继续报告，但不单独否决。
- `INVALID_CANDIDATE_CORRECTNESS`：任一正确性门禁失败。
- `ROLLBACK`：只有负向效应的稳健证据、幅度超过噪声/MDE，才作为性能回滚。

## 双轨

- `TRACK_A_CONTRACT_PRESERVING`：保留 P0-CONTROL-V1 的 history 与 /view 结果取得语义；重测 E4、E5、E7。
- `TRACK_B_ARCHITECTURE_FRONTIER`：E2 进入 `P0-CONTROL-V2-CANDIDATE`。history 完成后按 history 精确结果身份从受限 output root 读取同一文件；防路径逃逸，并用同一 prompt 的 HTTP/本地双取 SHA 一致性作非计时等价验证。

`TARGET_IMPROVEMENT_PERCENT=30` 仅为工程目标，不是数据筛选门槛。

Bracket 是候选的独立 `A_before,B,A_after` 三次运行单元，不从 ABBA/BAAB 的边界跨 block 拼接。每个 triple 独立计算 local baseline、drift 与 gain，batch bootstrap 以完整 triple 为单位。

在本轮完成前固定：`P0_99=NO`、`P0_FREEZE=NO`、`P1_UNLOCKED=NO`。

## 审计返修记录

独立审计发现初版 history 门禁接受缺失 completed/status_str 的响应，且未保存 history 正文；同时 MDE 模拟次数没有完整外显。2026-09-15 返修后，history 必须明确 `completed=true` 且 `status_str=success`，逐 run 无损保存 prompt 对应 history response 与 SHA-256；MDE 固定为 20,000 次模拟并保存完整 power curve。返修前所有批次保留但标为 `PREAUDIT_EVIDENCE_ONLY`，权威统计必须用返修后新 runner SHA 重新采集。

第一次权威 A/A 又出现 A/B 标签显著假差异；检查发现两臂使用不同 client_id，而这不是 A/A 所需变量。其 paired CI=[1.6799,6.418715] ms，校准 FAIL，证据保留。随后把非 E5 的两臂 client_id 统一并重新校准；不得把失败批改写为 PASS。

`AUTH-AA` 与 `AUTH-AA-SHARED-CLIENT` 均固定为 `PILOT_CALIBRATION_ONLY`。此前 40/80-block 权威尝试以及 2.4 ms MDE 全部固定为 `SUPERSEDED_BY_STATISTICAL_AUDIT`：其原始证据保留，但不得进入 FINAL_MDE 或候选裁决。新权威 A/A 必须使用通过纯统计自测的新 runner SHA。
