# UltraFusion V7.5 Baseline Gain 评分规则

状态：active

本文件是 `V7_Baseline_Gain_Scoring_Rule.md` 的中文审校版，保留 V7.0 原始判断逻辑。

## 公式

```text
Gain = SCORE_FINAL - Score_0
```

字段解释：

- `Score_0`：普通答案在进入 A/B/C/D 前的质量分。
- `SCORE_FINAL`：D 层最终收敛答案的质量分。
- `Gain`：完整 ABCD 链路带来的质量增益。

## 判定规则

```text
If Gain < 2.0 -> INVALID_CHAIN
If Gain >= 2.0 -> EFFECTIVE_CHAIN
```

中文解释：如果多模型 ABCD 链路没有比普通答案至少提升 2 分，就不能因为流程复杂而假装成功，必须诚实判定为无效链路。

## 评分纪律

- 使用 0-10 分；
- 不因流程更长就抬高 `SCORE_FINAL`；
- 事实错误、伪造引用、缺少限定、推理薄弱、融合浅、过度自信都要扣分；
- 长答案但真实增益小，仍可判定为 `INVALID_CHAIN`；
- 如果基线答案已经很好，可以建议停止，不强行跑低收益 ABCD。

## 最终必须输出

```text
Score_0:
SCORE_FINAL:
Gain:
Chain verdict: EFFECTIVE_CHAIN | INVALID_CHAIN
Reason:
```