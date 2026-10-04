# LTMVH v0.7.0｜Node R1 Freeze

```ini
VERSION=0.7.0
VERSION_STATE=SAVED_NOT_FROZEN
NODE=R1
NODE_STATE=REALITY_PASS_FROZEN
PROJECT_FINAL_VALID=NO
NEXT_NODE=R2
```

## 结论

R1 对同一父状态、同一下一节点、同一有效结果做了 3 对 Reality：

| Trial | Current Page | Frozen Node + True New Chat |
|---|---:|---:|
| 1 | 7,395.270 ms | 31,627.009 ms |
| 2 | 7,543.929 ms | 41,995.381 ms |
| 3 | 5,476.361 ms | 15,512.132 ms |
| 平均 | **6,805.187 ms** | **29,711.507 ms** |
| 中位数 | **7,395.270 ms** | **31,627.009 ms** |

Rotate 路平均多 **22,906.321 ms**，相对 Current Page 慢 **336.60%**（约 4.366×）。

B 路每次都满足：true New Chat、minimal handoff、submission_count=1、marker_count=1、branch=false。最终恢复 1 个空白 ChatGPT 根页。

因此本节点冻结：

```text
SMALL_TIGHTLY_COUPLED_NEXT_NODE
→ CONTINUE_CURRENT_PAGE is faster in this Reality set.

NODE_COMPLETE != ALWAYS_ROTATE
SEMANTIC_BOUNDARY is a decision point, not a mandatory rotation trigger.
```

本结果只覆盖“小、紧耦合、父上下文刚建立”的相邻节点，不把它外推成所有任务都应继续当前页。换页阈值、长上下文与语义边界的普适策略仍由后续 R4 等 Reality 决定。

## 额外发现（开放回归，不计入 R1 性能样本）

发现当前 ChatGPT UI 的 composer 为 `DIV.ProseMirror[contenteditable=true][role=textbox]`；旧 runtime 的“可见 composer”判定在回答结束后可误报 `composer=false`，导致 safeCheckpoint/rotation 控制可能失效。

```ini
DEFECT=V070-R1-UI-COMPOSER-VISIBILITY-REGRESSION
STATUS=OPEN
R1_SAMPLE_IMPACT=EXCLUDED_INVALID_RUNS_ONLY
MUST_FIX_BEFORE_V070_FINAL_FREEZE=YES
```

证据：`evidence/V070-R1-CURRENT-VS-ROTATE-REALITY-20261004-R1.json`
