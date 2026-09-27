# v5.3.3 超级冒烟任务 R1

## 任务定位

这是一个“形式上极简、流程上完整”的端到端自动化任务。

它不用于证明复杂业务能力；唯一目的，是用最短有效时间证明整条生产闭环能够自动走通：

任务发布 → GPT虚拟成熟 → Freeze → 自动完整Reality Dispatch → Codex真实执行 → 结果回传GPT → GPT最终收口。

本任务使用整体闭环极限短时间引擎 v5.3.3。
成熟技能包只作为执行工具，不改变任务的唯一目标。

## 唯一优化目标

T* = min(T_VALID)

T_VALID 边界：

TASK_ACCEPTED → FINAL_VALID

只有以下 VALID 条件全部满足，样本才进入时间比较：

1. 整条链无需用户人工提醒；
2. GPT不得停在Freeze；
3. Reality Dispatch必须完整；
4. Codex必须真实执行任务；
5. 业务结果必须正确；
6. 结果必须真实回传GPT；
7. GPT必须完成最终收口；
8. 不得通过隐藏测试入口、直接状态注入或现场修复伪造PASS。

## 极简业务任务

目标路径：

C:\Users\A\Documents\Codex\2026-09-27\este-super-smoke-v533\result.txt

目标内容必须精确为：

V5.3.3_SMOKE_OK

允许：
- 若目标目录不存在，创建该目录；
- 创建/覆盖目标 result.txt。

禁止：
- 修改目标目录之外的任何文件；
- 改动历史Freeze；
- 修改系统代理/FlClash/Windows网络设置；
- 为了通过验收临时修改产品。

## 自动化拓扑

1. v5.3.0 FSM：唯一状态权威；
2. v5.3.3 Acceptance Supervisor：失败分类、最多6次派发、传输恢复/切路；
3. GPT-Codex Orchestrator v1.5.2：只复用 A/B/C 传输与一次简单恢复；
4. Codex：真实执行器；
5. playwright-native-ai-browser：JEV-native Playwright 极限浏览器自动化 R3 编译热态版，负责真实界面操作；
6. GPT：虚拟成熟、Freeze、重新成熟、新Freeze、最终裁决。

## 自动化路径

S0 TASK_ACCEPTED
→ S10 VIRTUAL
→ S20 VIRTUAL_MATURE
→ S30 FROZEN_TRANSIENT
→ S40 REAL_DISPATCHED
→ Codex真实执行
→ 返回GPT
→ PASS: S100 FINAL_VALID

若 PRODUCT FAIL：
S40 → S10
→ GPT重新虚拟成熟
→ 新Freeze
→ 再派发

若 TEST_HARNESS / TRANSPORT FAIL：
产品Freeze不动
→ Orchestrator同路径恢复一次
→ 仍失败则 A→B→C
→ 重做同一任务

若 EXTERNAL BLOCKED：
先恢复/切路
→ A/B/C均不可用才进入BLOCKED

同一连续任务最多6次Reality派发。

## 用户模拟方式

最高级验收不由用户手工执行。

Codex/Orchestrator 必须调用 playwright-native-ai-browser，通过真实GPT页面模拟普通用户提交本任务，并观察/读取屏幕输出。

禁止：
- Codex自己写新的Playwright脚本；
- GPT提前手工准备最终Reality命令；
- 直接调用隐藏Python函数替代真实UI；
- 用户中途提醒“继续”“发命令”。

## 成功标准

最终必须同时证明：

AUTO_USER_PROMPT_SUBMITTED=PASS
VISIBLE_VIRTUAL_MATURITY=PASS
AUTO_FREEZE_TO_REAL=PASS
COMPLETE_REALITY_DISPATCH=PASS
CODEX_REAL_EXECUTION=PASS
TARGET_FILE_EXISTS=PASS
TARGET_FILE_CONTENT_EXACT=PASS
NO_OUT_OF_SCOPE_FILE_CHANGE=PASS
RESULT_RETURNED_TO_GPT=PASS
GPT_FINAL_CLOSEOUT=PASS
USER_INTERVENTION_COUNT=0

最终才允许：

FINAL_VALID=YES
DONE=YES

## 性能目标

最终只以真实有效闭环时间为准：

REAL_T* = min(REAL_VALID_T)

本任务不人为增加复杂业务步骤；设计目标是把控制开销压到最低。
虚拟阶段先以 60 秒作为“快速冒烟任务”的工程目标带，不作为VALID硬门。
真实完成后用实际 T_VALID 替代该目标带。

## 当前边界

本文件只定义任务与自动化闭环。

本轮不发布Codex执行命令。
