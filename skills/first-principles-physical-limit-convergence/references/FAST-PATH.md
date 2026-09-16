# FAST PATH — 两步物理极限收敛最短路径

## STEP 1 — CALCULATE

1. 冻结 `TASK_CONTRACT`、`TASK_COMPLETED` 和 hard constraints。
2. 继承所有与新任务兼容的既有冻结 99；禁止故意退回 stock。
3. 复用已有真实事实，只补关键缺口；禁止为了“完整感”全盘重扫。
4. 建立物理因果 DAG 与 critical path。
5. 推导 `T_PHY=[LOW,HIGH]`：不可避免计算、数据移动、同步、等待与物理资源下界。
6. 推导 `T_MACHINE_STAR=[LOW,HIGH]`：加入当前机器的实际算力、带宽、容量、软件栈、可持续利用率与资源互斥约束。
7. 建立 `ASSUMPTION_LEDGER`：未知量用区间 + 置信度，不因为缺一次新实测而停止推导。
8. 计算分块理论目标与 `ATTACK_ORDER`。
9. 判断多智能体模式：`OFF / SUPPORT_PARALLEL / RESOURCE_PARTITIONED`；排他资源 benchmark 必须串行。
10. 可选查成熟方案，只用于 sanity check / implementation reuse / 漏项检查，不作为终点。

## STEP 2 — CONVERGE

11. 对第一步已证明属于重甲的路径先做安全去重，建立 `V1`。
12. 审核 V1 命令包：合同、计时边界、资源状态、可逆性、看门狗、证据、Git closure。
13. 真正运行 V1，得到权威 `T_CURRENT` 与各自然时间块。
14. 计算 `DELTA_T_REDUCIBLE_i = T_CURRENT_i - T_MACHINE_TARGET_i`。
15. 选择最大绝对 Gap，实施一个可解释机制；真实运行。
16. 更快且 hard constraints PASS => KEEP；否则 ROLLBACK。
17. 重新测量、重排 Gap；循环，不预设固定阶段数量。
18. 满足 99 gate 后 FREEZE。
19. 形成正式报告和结构化事实。
20. 精确 stage -> commit -> push -> remote verify。
21. 只有 shared-repo closure PASS 后，99 / FREEZE / FINAL PASS 才正式成立。

```text
先算终点，再做 V1；以后永远攻击离本机物理目标最远、且绝对可节省时间最大的块。
```
