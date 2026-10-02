# CASE-H3-P1：首个有效图声对

CASE_ID=VETE-v0.5-CASE-H3-P1
PROJECT=H3-P1：首个有效图声对 v1.0.0
METHOD=整体闭环极限短时间引擎 v5.6.5
RESULT=REALITY_CERTIFIED

## VALID 规格

最终有效样本必须同时满足：
- 成年女性主体清楚；
- 正面对镜头；
- 挥手可辨识；
- 存在人声；
- 清楚说中文“你好”；
- 无目标提示 ASR 匹配“你好”；
- 说话动作与声音对应；
- 基本音画同步；
- 最低展示可用。

## 初始正式基线

```
T_VALID=T*=653921.787ms
```

## 关键 Reality 过程

### R1 分解
历史五阶段：
- PREP 80.637s
- GENERATE 258.413s
- DECODE 29.844s
- SAVE 2.046s
- VERIFY 92.042s

同口径未计入差额：
```
653921.787 - 462982.315 = 190939.472ms
```

结论：最大首要问题是编排空耗，而不是单纯 GPU 计算。

### R2：闭环与 12-step
建立单本机闭环 runner，并验证：
- history publication race 可通过同 prompt_id bounded polling 修复；
- 12-step 可以产生 VALID；
- 随机 seed 会引发 speech semantic drift；
- 已验证有效 seed：`2026090201`。

Reality04：
```
T_VALID=616191.785ms
```

首次正式打破旧 T*。

### R3：warm + lightweight verifier
Reality05：
```
T_VALID=358618.442ms
```

关键结果：
- PREP 2.567s
- GENERATE 180.515s
- DECODE 65.494s
- SAVE 13.001s
- VERIFY 90.901s
- T_UNACCOUNTED=0

说明有效 seed、12-step、warm path、轻量 verifier、单闭环可以在同一 VALID run 同时成立。

### R4：最佳阶段组合收敛
Reality06：
```
T_VALID=288281.990ms
```

阶段：
- PREP 2.280s
- GENERATE 201.506s
- HISTORY WAIT 3.997s
- DECODE 10.615s
- SAVE 3.591s
- VERIFY 66.256s
- CONTROL 0.037s
- T_UNACCOUNTED 0

结果：
```
OLD_T*=358618.442ms
NEW_T*=288281.990ms
IMPROVEMENT=70336.452ms
IMPROVEMENT_PERCENT=19.613172%
SPEEDUP=1.243985x
```

## 总体改善

```
INITIAL_T*=653921.787ms
FINAL_T*=288281.990ms
TOTAL_IMPROVEMENT=365639.797ms
TOTAL_IMPROVEMENT_PERCENT=55.914913%
TOTAL_SPEEDUP=2.268341x
```

约从 10.90 分钟降到 4.80 分钟。

## 被 Reality 证明的通用经验

1. 先消灭流程编排黑洞，再考虑更深模型优化。
2. 单闭环 runner 能把未解释编排时间压到 0。
3. 固定重复任务优先使用 warm service/model/conditioning。
4. 生成完成后 history/output 可能有发布竞态，必须有界等待，不可直接索引空结果。
5. 固定业务任务可 Freeze 已验证有效 seed，避免随机语义漂移带来的重试。
6. verifier 必须和业务 VALID 对齐，不把报告整理、ZIP、哈希、知识库检查计入 T_VALID。
7. 同一视频只 decode 一次；ASR 只做一次；独立 verifier 尽量并行。
8. 失败候选的阶段时间可以用于诊断，但绝不能成为正式 T*。
9. Reality 的阶段最佳值只有在同一次 VALID run 同时成立时才可以提升 T*。
10. 当剩余主要是运行波动或需高风险改参时，停止主动极限攻击。

## 当前结论

当前正式 Reality 收敛值：

```
T*=288281.990ms
```

约 263.164s 的阶段组合曾真实出现，但对应 run INVALID，只保留为近端性能参考。

在没有新的低风险、确定性优化开关前，H3-P1 主动攻击停止。
