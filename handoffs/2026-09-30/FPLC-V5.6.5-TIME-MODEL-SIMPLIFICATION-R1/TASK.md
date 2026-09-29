# v5.6.5 时间模型简化 Reality

PAGE=极限短时间v5.6.5自动
ENGINE_VERSION=v5.6.5
FREEZE_ID=FPLC-v5.6.5-TIME-MODEL-SIMPLIFICATION-R1
ENGINE_PATH=skills/first-principles-physical-limit-convergence-v5.6.5/
REALITY_START_STATE=30

## 目标

只验证 v5.6.5 的时间模型简化是否在真实环境成立。
不要重做引擎，不要扩展规则。

## 实际收件即本轮起点

收到本任务时：
- 记录真实 FLOW_START_TIME；
- FLOW_START_STATE=30；
- 不补 STATE10_TIME / STATE20_TIME；
- 不把 GPT 派发时间冒充收件时间。

## 只读核验 + 运行测试

读取：
- skills/first-principles-physical-limit-convergence-v5.6.5/SKILL.md
- skills/first-principles-physical-limit-convergence-v5.6.5/FREEZE.md
- skills/first-principles-physical-limit-convergence-v5.6.5/ACCEPTANCE.md
- skills/first-principles-physical-limit-convergence-v5.6.5/runtime.py
- skills/first-principles-physical-limit-convergence-v5.6.5/display.py

验证：
1. 状态机仍为 10→20→30→40→100。
2. 当前 Reality 可从30直接开始。
3. 不要求补10/20历史时间。
4. 当前节点产生真实 STATE_TIME。
5. T_FLOW 从本轮实际起点计算。
6. 不依赖 Stopwatch.GetTimestamp 或任何特定单调时钟 API 才允许推进。
7. 时间不可比较时只令 T_FLOW=未知，不伪造时间，不因此改变业务状态。
8. T_VALID/T* 与 T_FLOW 分离；局部执行耗时不得冒充 T_VALID。
9. SHA256/业务 judge/TRANSITIONS 未因本次时间简化被改写。
10. Reality 阶段禁止修改 Freeze/Runtime 来取得 PASS。

## 返回格式

【极限短时间v5.6.5自动｜v5.6.5时间模型简化Reality｜01｜实】
【状态机｜v5.6.5｜40｜实：执行与审核中】
【时间｜本轮起点=30@<真实收件时间>｜当前节点=40@<真实返回时间>｜本轮已用(T_FLOW)=<机械计算>｜T_VALID=尚未产生｜T*=<已有则填，否则未知>】

VERSION=v5.6.5
FREEZE_ID=FPLC-v5.6.5-TIME-MODEL-SIMPLIFICATION-R1
REALITY_RESULT=PASS/FAIL
TEST_RESULTS=
FLOW_START_STATE=30
FLOW_START_TIME=
STATE40_TIME=
T_FLOW=
HISTORICAL_TIME_BACKFILLED=NO
SPECIFIC_TIMER_API_REQUIRED=NO
BUSINESS_STATE_BLOCKED_BY_TIMER_API=NO
T_VALID=尚未产生
LOCAL_TIME_USED_AS_T_VALID=NO
STATE_MACHINE_UNCHANGED=
BUSINESS_LOGIC_UNCHANGED=
SHA256_LOGIC_UNCHANGED=
RETURN_TO_GPT=YES

失败时只报告最小失败点，不现场修复。
不得自行宣布 FINAL_VALID、DONE 或状态100。
