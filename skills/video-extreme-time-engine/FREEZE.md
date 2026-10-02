# 视频极限短时间引擎 v0.5 Freeze

VERSION=0.5
STATUS=FROZEN
FREEZE_ID=VETE-v0.5-H3P1-R1
METHOD_PARENT=first-principles-physical-limit-convergence-v5.6.5

## 固定原则

- 唯一目标：`T*=min(T_VALID)`。
- 只比较同一 VALID 规格。
- GPT 负责虚拟攻击、Freeze、最终审核。
- Reality Executor 只执行冻结方案，最高合法状态为 40。
- `T_FLOW` 与 `T_VALID` 分离。
- `T_VALID` 必须由真实 `T_VALID_START/T_VALID_END` 机械计算。
- Reality 具体实现失败时只做局部最小修复，不扩大架构。
- 普通生产态优先使用 warm path；认证不得靠复用旧最终输出。
- verifier 只保留必要有效性检查，不允许报告/ZIP/哈希整理拖长 `T_VALID`。

## v0.5 冻结的通用性能模式

```
single local closed-loop runner
+ warm service/model reuse
+ safe conditioning/static-node reuse
+ new sampler execution
+ bounded history/output publication wait
+ single decode
+ single unprompted ASR where speech text matters
+ parallel independent verification
+ VALID_END at last required verifier PASS
```

## 首个正式案例结论

CASE=H3-P1
VALID=成年女性正面对镜头挥手并清楚说“你好”，基本音画同步与最低展示可用均通过。

INITIAL_T_STAR_MS=653921.787
FINAL_T_STAR_MS=288281.990
TOTAL_IMPROVEMENT_MS=365639.797
TOTAL_IMPROVEMENT_PERCENT=55.914913
TOTAL_SPEEDUP=2.268341

FROZEN_H3_PARAMETERS:
- steps=12
- seed=2026090201
- width=608
- height=352
- length=73
- fps=24
- sampler=res_multistep
- scheduler=beta
- denoise=1.0

说明：以上 H3 参数只属于首个 Reality 案例，不是所有视频任务的全局固定值。

## 收敛边界

Reality 曾出现约 263.164s 的更快阶段组合，但该 run 最终 INVALID，因此不得作为正式 T*。

当前 288281.990ms 是首个案例的正式 Reality 收敛值。

若后续正常使用自然产生更短、同 VALID 的完整有效结果，可重新开启：
`STATE=10 → 虚拟审查 → 新 Freeze → Reality`。

在没有新证据前，不为追求理论 217–257s 区间主动扩大 steps/resolution/model/sampler 攻击。
