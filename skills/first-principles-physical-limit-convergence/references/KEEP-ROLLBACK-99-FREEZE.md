# KEEP / ROLLBACK / 99 / FREEZE

KEEP 默认要求：

```text
TASK_CONTRACT_IDENTICAL=YES
HARD_CONSTRAINTS_PASS=YES
AUTHORITATIVE_TIMING_VALID=YES
T_NEW < T_OLD
```

差值小于测量噪声时不得把随机抖动声明为 KEEP。

更慢、错误、质量/稳定性/安全失败、合同改变、计时不可比、收益未高于噪声或引入更大关键路径成本时 ROLLBACK。

`T_MACHINE_STAR` 允许版本化修订，但必须 `NEW_EVIDENCE=YES / ASSUMPTION_INVALIDATED=YES / REVISION_REASON=DOCUMENTED`。禁止 `CURRENT_TOO_SLOW -> MOVE_TARGET_UP`。

99 必须同时满足：task completed、hard constraints PASS、measurement valid、稳定重复、结果进入或贴近高置信本机极限区间、剩余高置信可实施机制的绝对收益 <= 噪声 + 工程/切换成本门槛、无明显大块重甲、target 未被人为放宽、shared repo closure PASS。

FREEZE 至少保存任务合同、硬件/软件身份、权威 timers、T_PHY/T_MACHINE_STAR 版本、final timings、iteration history、KEEP/ROLLBACK、remaining gaps、SHA/source identity、reproduction entry、shared repository commit。
