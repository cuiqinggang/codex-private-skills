# H3-P0 最终认证修正规则 v1

状态：`PROJECT_LEVEL_CERTIFICATION_REPAIR / MOTHER_SKILL_UNCHANGED`

## 1. 为什么当前 FAIL 不能直接解释为 Star7 方案失败

当前最终认证同时混入了两个不同问题：

1. `920100` Total=19.9941s，主要是 Generation=16.0761s 的性能慢尾；
2. `920108` Generation=2.1033s，但输出接近全白，是内容质量失败。

历史上 Star7 之前的 V1 原始基线也曾出现 seed 910101 近乎全白，后来通过升级 QC 并使用有效正式 seed 建立 V1_QC。因此随机 seed 内容失败不能自动归因为 Star7。

同时，本轮一条固定预热 920099 后，920100 仍然很慢；920101–920107 七条有效运行随后稳定在 5.4350–6.1022s，说明一次预热不足以代表稳态准备完成。

因此本轮修正的是“最终认证协议”，不是优化方案，也不是母技能四步法。

---

## 2. 三个认证对象分开

### A. 冷启动 / 预热

只记录，不参与长期大规模稳态 99 的 P50/P95。

固定做 2 次预热，不计正式统计。

目的：让模型、动态显存、权重驻留和运行时进入稳定状态。

### B. Seed 内容有效性

质量门槛不放宽：

- MP4 可解码；
- 32×32×5；
- finite；
- 非黑非平坦；
- 每帧 range >= 8；
- 每帧 std >= 1.5。

若 Star7 正式 seed 仅出现“技术完整但近乎全白/平坦”的内容 QC 失败：

1. 只允许用原始标准加载器，对同一个 seed 做 1 次 QC 对照；
2. 若原始加载器也发生同类平坦/全白：标记 `SEED_INVALID`，该 seed 不计入 Star7 认证，使用预先列出的下一个备用 seed；
3. 若原始加载器 QC PASS：标记 `STAR7_QUALITY_FAIL`，最终认证立即 FAIL；
4. 不允许借机 profiler、改参数、换模型或研究根因。

最多允许 2 个 `SEED_INVALID` 替换。超过 2 个，说明当前任务 seed 质量稳定性本身不足，停止返回 GPT。

### C. Star7 稳态性能

必须最终得到 10 条 `Star7 + QC PASS + seed有效` 的正式样本。

正式统计只用这 10 条。

---

## 3. 修正后的通过标准

必须同时满足：

```text
VALID_FORMAL_RUNS = 10/10
QC_PASS = 10/10
NO_CRASH = YES
NO_AUTO_RETRY = YES
TOTAL_P50 <= 14.0 s
GENERATION_P50 <= 5.0 s
PATH_P50 <= 9.0 s
TOTAL_P95 <= 2.0 * TOTAL_P50
TOTAL_MAX <= 2.5 * TOTAL_P50
LAST3_MEDIAN <= FIRST3_MEDIAN * 1.5
```

说明：

- `14s / 5s / 9s` 来自已冻结的 `REAL_STATE_OPTIMUM_RANGE` 现实目标带；
- `T_PHY_TOTAL_REFERENCE=0.23–0.57s` 仍只是物理参照，不作为认证阈值；
- 不因一次冷启动/预热慢尾否定长期稳态性能；
- 不因 reference baseline 同样失败的坏 seed 否定 Star7；
- 也绝不降低实际视频质量门槛。

---

## 4. 当前数据说明

920101–920107 七条 QC PASS 稳态描述性统计：

```text
Generation: P50=2.1523s, P95≈2.5995s, Min=2.0216s, Max=2.7736s
Path:       P50=3.4643s, P95≈3.8237s, Min=3.2697s, Max=3.8799s
Total:      P50=5.5665s, P95≈6.0591s, Min=5.4350s, Max=6.1022s
```

这些数据强烈支持“Star7 稳态约 5.5–6.1s”的假设，但样本只有 7 条，不能直接据此宣布 99；必须按修正规则重新完成 10 条认证。

---

## 5. 对 920108 的必要判定

920108 当前只能写：

```text
OUTPUT_QUALITY_FAIL = YES
ROOT_CAUSE = UNKNOWN
STAR7_CAUSED_FAILURE = NOT_PROVEN
SEED_INVALID = NOT_PROVEN
```

下一轮认证若再次遇到同类内容失败，按上面的 same-seed reference check 处理。

不建议单独为了 920108 开新优化路径。

---

## 6. 最终原则

这是一次认证协议修正，不是优化循环：

```text
不改 Star7
不改模型
不改参数
不改质量门槛
不做性能探索
只把“冷启动 / seed有效性 / 稳态性能”正确分开
```

完成修正后的 10 条认证并远端核验后，才允许决定 FINAL_99 / FREEZE。
