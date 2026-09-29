# v5.6.4 Reality 最小认证

目标：只认证 v5.6.4 新增的 Reality 时间派发合同，不重新认证整个引擎。

## 必测

1. 正常 Reality 命令：定位行、状态机行、时间锚行三者齐全，允许派发。
2. 删除定位行：必须拒绝派发。
3. 删除状态机行：必须拒绝派发。
4. 删除时间锚行：必须拒绝派发。
5. GPT_DISPATCH_TIME 不得作为 TASK_ACCEPTED。
6. 执行器真实收件现场建立 TASK_ACCEPTED、accepted_clock、accepted_tick_ns。
7. 起点只冻结一次。
8. 同源 event_tick_ns 能机械产生 T_VALID。
9. 无合法起点时不得产生数值 T_VALID。
10. 不得因本测试现场修改 Freeze。

## 失败分类

- GPT_HOST_DISPATCH
- RECEIPT_PROTOCOL
- TIME_ORIGIN
- RUNTIME_CALCULATION
- TEST_HARNESS
- EXTERNAL

Reality 完成后保持状态40返回 GPT：
RETURN_TO_GPT=YES

不得自行宣布 FINAL_VALID 或 DONE。


## 新增最小必测：五状态时间锚

11. 分别观察 10、20、30、40、100 的正式状态输出；每个状态都必须同时有状态机行和时间锚行。
12. 状态20→30→40 全程 TASK_ACCEPTED 与冻结起点不得被重置。
13. 状态30必须区分 GPT_DISPATCH_TIME 与真实 TASK_ACCEPTED。
14. 状态100只有合法同源计时链存在时才允许数值 T_VALID；缺起点必须 fail-closed。
15. 输出：
STATE10_TIME_ANCHOR=
STATE20_TIME_ANCHOR=
STATE30_TIME_ANCHOR=
STATE40_TIME_ANCHOR=
STATE100_TIME_ANCHOR=
STATE_TIME_COUPLING=PASS/FAIL
