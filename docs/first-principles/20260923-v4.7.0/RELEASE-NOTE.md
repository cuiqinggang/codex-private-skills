# 极限短时间引擎 v4.7.0 冻结说明

## 版本核心

v4.7.0 = 双时间单闭环。

- T_MATURE*：成熟方案必要极限有效时间。当前精确锚为 00:03:14.419。
- T_CLOSED_REAL：用户首次提交到 GPT FINAL_VALID 的完整现实墙钟时间。
- 方法仍只有 VIRTUAL / REAL 两步。
- T_CLOSED_REAL 的归因桶只做诊断，不创建第三个核心时间。

## 为什么升级

v4.6.0 已经证明任务本体可在约 3 分钟完整闭环；现实用户体验却可能跨越数小时。v4.7.0 优先消除人在 READ / UNDERSTAND / COPY / PASTE / ROUTE / CONFIRM / RESULT RELAY 中的编排延迟。

## 自动化顺序

P0 双时间单闭环合同；P1 GPT↔Codex 回归认证；P2 Playwright 回归认证；P3 合并无人值守多轮闭环；P4 注入可恢复 Reality Delta；P5 精确 manual vs automated T_CLOSED_REAL 对照。

## 当前证据边界

GPT↔Codex v1.5.2：A PASS、B PASS_CONTROLLED、C PASS_CONTROLLED、USER_MIDDLE_COPY_PASTE=0；自然 A→B / B→C failover 仍未验证。

Playwright：冻结 R3 runner / Artifact Virtual-99 可远端定位。最新 30/30、min 272.98ms 的现实结果来自用户本轮提供的近期真实输出；本次仓库检查没有定位到独立远端最终结果文件，因此保留来源标记，不冒充远端复核证据。

## 下一现实任务

`V47-AUTOMATION-CLOSED-LOOP-01`，TASK_TIME_ID=`ESTE-20260923-005`。

用户只提交一次；中间人工复制粘贴、Codex 输入、结果回传、浏览器路由全部目标为 0。使用无副作用 Reality Delta 注入，验证自动回虚、第二次冻结和第二次执行。

第一轮先测精确 `T_CLOSED_REAL_AUTOMATED`。由于今晚人工过程只有“数小时”的用户报告而没有完整墙钟自动打点，不计算虚假节省百分比。后续用同任务精确人工基线做 paired comparison。
