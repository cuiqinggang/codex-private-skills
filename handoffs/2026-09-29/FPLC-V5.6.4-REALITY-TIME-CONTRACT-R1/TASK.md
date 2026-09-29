# v5.6.4 Reality 时间派发合同最小认证

ENGINE_VERSION=v5.6.4
FREEZE_ID=FPLC-v5.6.4-REALITY-TIME-DISPATCH-CONTRACT-R1
ENGINE_COMMIT=6bf619fdbc4ab3f7ca2a336551c922ba2307da35
ENGINE_PATH=skills/first-principles-physical-limit-convergence-v5.6.4/

目标：只认证 v5.6.4 新增的 Reality 时间派发合同，不重新设计或扩大架构。

必须验证：
1. 正常命令三行齐全 → 允许派发。
2. 缺定位行 → 拒绝派发。
3. 缺状态机行 → 拒绝派发。
4. 缺时间锚行 → 拒绝派发。
5. GPT_DISPATCH_TIME 不得作为 TASK_ACCEPTED。
6. 执行器真实收件现场建立 TASK_ACCEPTED、accepted_clock、accepted_tick_ns。
7. 时间起点只冻结一次。
8. 同源 event_tick_ns 机械产生 T_VALID。
9. 无合法起点时不得产生数值 T_VALID。
10. Reality 阶段禁止修改 Freeze 来取得 PASS。

失败分类：
GPT_HOST_DISPATCH
RECEIPT_PROTOCOL
TIME_ORIGIN
RUNTIME_CALCULATION
TEST_HARNESS
EXTERNAL

完成后必须 RETURN_TO_GPT=YES。
不得自行宣布 FINAL_VALID 或 DONE。
