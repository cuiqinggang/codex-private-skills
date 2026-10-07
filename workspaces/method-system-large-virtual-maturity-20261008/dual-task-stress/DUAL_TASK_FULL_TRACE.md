# 双大型任务并行生产同构对抗式虚拟重放 — Full Trace

META_TASK=METHOD-SYSTEM-LARGE-VIRTUAL-MATURITY-20261008
CONTRACT_VERSION=3
METHOD=ENGINE22 / BRAIN19 / TEMPLATE17
METHOD_REF=f468845df6a74e0842b75550c1072e90cb1784da
TASK_ACCEPTED=2026-10-08T00:45:00+08:00

TASK_A=DUAL-STRESS-A-LTMVH-PAGE-CONTROL-20261008
TASK_B=DUAL-STRESS-B-H3P1-VIDEO-CONVERGENCE-20261008

## 1. 首故障与重启

BRAIN18 在双任务起跑即暴露 ACTIVE_CEO / global writer 作用域歧义。
Fail Fast -> F14 -> 只升级 BRAIN18→19 -> F15 -> 两 TASK 从 TASK_ACCEPTED 全部重跑。
ENGINE22/TEMPLATE17 未升级。

## 2. 并行结构

两任务均 PAGE_TOPOLOGY=CEO_EXECUTOR。
ONE_ACTIVE_CEO=PER_TASK_ID：
- A 同时存在 A-CEO-n；
- B 同时存在 B-CEO-n；
- 同一 TASK 内旧/新 CEO handoff 后旧 CEO 不再写状态。

共用同一个 persistent ChatGPT browser；没有第二 browser launch。
GitHub main writer 通过 SYSTEM_RESOURCE_LEASE 在写操作粒度仲裁。

## 3. 交错执行

W1：A-N1/A-N2 与 B-N1/B-N2 同时运行；返回顺序 B-N2 -> A-N1 -> B-N1 -> A-N2。
W2：A R15 Repair/Reverify 与 B publication-race Repair/seed reverify 并发。
W3：A stall/hydration FAIL→Repair 与 B fixed-seed R2→R3 virtual 并发。
W4：A R6 existing-browser Reality 与 B R3 warm-path Reality 并发。
W5：A R18 virtual candidate convergence 与 B R4 fast-invalid/best-valid repair 并发。

A Freeze=13；B Freeze=13。
A True New Chat=4（F3/F6/F9/F12 后）。
B True New Chat=4（F3/F6/F9/F12 后）。
共享 writer contention group=13。
第二 persistent browser launch=0。

## 4. TASK_A

- baseline clean lifecycle + historical fault oracle parallel merge；
- R15 duplicate launch Reality FAIL；
- attach-only/watchdog Repair；
- R15 Reverify PASS；
- stall/hydration链 FAIL；
- R10-style abort/checkpoint/True New Chat/exactly-once Repair；
- Reverify submission=1 marker=1 ACK；
- R6 existing-browser continuity PASS；
- R8/R10/R13/R14/R15/R16/R17/R18 候选连续虚拟成熟；
- R18=51,454ms STOP_GATE；
- R18/R19 final oracle PASS；
- TASK_A FINAL_VALID=YES。

A 先于 B 完成。A cleanup 只关闭 A 所有权页；B CEO/Executor 页保持活动，系统浏览器没有被错误重置。

## 5. TASK_B

完整 H3-P1 收敛链：
- baseline 653,921.787ms；
- R1 五阶段剖面，识别编排空耗；
- publication race FAIL；
- bounded same-prompt polling Repair；
- random seed semantic drift INVALID；
- fixed seed=2026090201 + 12-step Repair；
- R2 Reality04 PASS，616,191.785ms；
- R3 warm path + lightweight verifier + single decode + single ASR + independent verifier parallel；
- R3 Reality05 PASS，358,618.442ms；
- ~263.164s fast candidate INVALID，明确拒绝提升 T*；
- best VALID stage combination Repair；
- R4 Reality06 PASS，288,281.990ms；
- TASK_B FINAL_VALID=YES。

B 完成后全部任务页回收，系统共享浏览器才恢复为 1 个空白 New chat 根页。

## 6. 对抗矩阵结果

X01-X20 全部 PASS。

特别结果：
- TASK_A/B Freeze version 完全独立；
- STATE_REF/Freeze-path cross injection 被 TASK_ID namespace 拒绝，状态未改变；
- A FAIL/回虚未回滚 B；
- B INVALID/回虚未改变 A；
- 页面关闭均按 TASK_ID+PAGE_ID；
- A FINAL_VALID 时未误关 B；
- shared repo writer 13 次竞争均 single owner；
- writer lease 只阻塞具体写节点，另一个 TASK 的无冲突工作继续；
- old/new CEO split-brain=0；
- duplicate execution=0；
- wrong Merge=0；
- Freeze cross-line=0；
- state pollution=0。

## 7. 重复压力计数

EXECUTOR_PARALLEL_WAVES=5
INTERLEAVED_RETURNS>=10
CEO_MERGES>=20
TASK_A_FREEZES=13
TASK_B_FREEZES=13
TASK_A_TRUE_NEW_CHAT=4
TASK_B_TRUE_NEW_CHAT=4
TASK_A_FAIL_DELTA=2
TASK_B_FAIL_DELTA_OR_INVALID=3
TASK_A_REPAIR_REVERIFY_CYCLES=2
TASK_B_REPAIR_REVERIFY_CYCLES=3
SHARED_WRITER_CONTENTIONS=13
PAGE_CLOSE_EVENTS>=12
PERSISTENT_BROWSER_INSTANCE_COUNT=1
SECOND_BROWSER_LAUNCH=0

## 8. 最终判定

TASK_A_FINAL_VALID=YES
TASK_B_FINAL_VALID=YES
REAL_CONCURRENT_INTERLEAVING=YES
TASK_STATE_POLLUTION=NO
FREEZE_CROSS_LINE=NO
WRONG_MERGE=NO
DUPLICATE_EXECUTION=NO
DOUBLE_WRITER=NO
WRONG_PAGE_CLOSE=NO
DUPLICATE_PERSISTENT_BROWSER=NO
SHARED_RESOURCE_CONTROL_LOST=NO
OLD_FAULT_RECURRED=NO
NEW_METHOD_FAULT_AFTER_BRAIN19=NO

VIRTUAL_MATURE=YES
REALITY_CERTIFIED=NO
