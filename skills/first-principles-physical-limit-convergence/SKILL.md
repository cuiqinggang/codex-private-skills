---
name: first-principles-physical-limit-convergence
description: 极限短时间引擎 v4.7.1。双时间单闭环 + 虚→实原子发布门：虚拟成熟只有在同一轮完成下一序号分配并发布自包含 Codex 现实验收命令后才允许 VIRTUAL_COMPLETE=YES。
metadata:
  version: "4.7.1"
  display_name: "极限短时间引擎"
---

# 极限短时间引擎 v4.7.1

## 1. 方法结构仍然只有一虚一实

方法步骤严格只有：VIRTUAL（虚）和 REAL（实）。
唯一状态转换：VIRTUAL -> REAL；REAL PASS -> FINAL；REAL FAIL -> VIRTUAL。
自动化、计时、浏览器、Codex、Reality Delta、GitHub 都只是这两步的执行基础设施或观测，不创建第三步骤。

## 2. v4.7.1 虚→实原子发布门（不可绕过）

过去“HANDOFF_READY=PASS”仍可能停在口头汇报，导致虚已成熟却没有现实命令。v4.7.1 把状态转换改成原子事务。

固定状态机：

```text
VIRTUAL_ACTIVE
-> VIRTUAL_FREEZE_PASS
-> NEXT_SEQUENCE_ASSIGNED
-> REAL_HANDOFF_PREPARED
-> REAL_COMMAND_EMITTED
-> REAL
```

只有以下条件全部成立，才允许：

```text
VIRTUAL_COMPLETE=YES
CURRENT_PHASE=REAL
```

硬门：

```text
FREEZE_GATES_ALL_PASS=YES
NEXT_SEQUENCE_ASSIGNED=YES
REAL_HANDOFF_SELF_CONTAINED=YES
REAL_COMMAND_EMITTED=YES
TIME_LEDGER_CONTINUITY=PASS
```

其中任何一项缺失：

```text
VIRTUAL_COMPLETE=NO
TRANSITION_BLOCKED=HANDOFF_NOT_EMITTED
CURRENT_PHASE=VIRTUAL
```

### 同一轮原子性

一旦冻结门 PASS，同一条 GPT 回复必须连续完成：

1. 写出虚阶段冻结结果；
2. 分配同一 TASK_TIME_ID 下的 NEXT_SEQUENCE；
3. 生成【页面名｜任务名｜序号｜实】四定位标签；
4. 生成完整、自包含、可直接交给 Codex 的现实验收任务；
5. 明确现实阶段禁止重新设计；
6. 明确 PASS/FAIL 输出合同；
7. 发布该 Codex 命令；
8. 然后才允许宣布 VIRTUAL_COMPLETE=YES / CURRENT_PHASE=REAL。

禁止以“下一步我可以给你命令”“准备进入实”“HANDOFF_READY=PASS”作为虚阶段终点。

### 发布与自动发送

若当前环境存在已授权 GPT->Codex 自动桥：
- 同一轮必须自动发送；
- 记录 REAL_DISPATCHED=AUTO。

若当前环境没有可用自动桥：
- 同一轮必须至少发布完整可复制的 Codex 命令；
- 记录 REAL_COMMAND_EMITTED=YES；
- 记录 REAL_DISPATCH_MODE=MANUAL_BRIDGE_REQUIRED；
- 这不满足 v4.7 自动闭环验收中的 MANUAL_CODEX_INPUT=0，但不允许因此省略命令。

### REAL FAIL 回虚

REAL FAIL 时：
- 只记录最小 Reality Delta；
- STOP；
- 同一 TASK_TIME_ID 回 VIRTUAL；
- 时间不清零；
- 序号不清零；
- 重新成熟后 NEXT_SEQUENCE=LAST_VALID_EMITTED_SEQUENCE+1；
- 再次触发本原子发布门；
- 没有新现实命令，不得再次声明 VIRTUAL_COMPLETE=YES。

### 防遗忘不变量

```text
VIRTUAL_COMPLETE_IMPLIES_REAL_COMMAND_EMITTED=TRUE
REAL_PHASE_IMPLIES_REAL_COMMAND_EXISTS=TRUE
HANDOFF_READY_WITHOUT_COMMAND=INVALID
FREEZE_PASS_WITHOUT_SEQUENCE=INVALID
REAL_FAIL_DOES_NOT_RESET_TASK_TIME_ID=TRUE
REAL_FAIL_DOES_NOT_RESET_SEQUENCE=TRUE
```

## 3. 双时间，单闭环

同一个任务闭环只保留两个核心时间：

T_MATURE* = 在完整有效约束下，成熟方案真正需要的最短有效智能体工作时间。
T_CLOSED_REAL = 从用户首次提交任务到 GPT 确认 FINAL_VALID=PASS 的真实墙钟时间。

两个时间共享同一个任务边界与 FINAL_VALID，不是两套任务。
不再创建第三个并列核心时间。

当前成熟锚：T_MATURE*=00:03:14.419，来源于 v4.6.0 clean run ESTE-20260923-003。
历史 v4.5.x >=00:51:07.109 只属于开发/返工活跃成本样本，不是 T_MATURE*，也不是 T_CLOSED_REAL。
用户报告今晚现实经历跨越数小时；由于旧流程没有全程墙钟自动打点，只记录为 HISTORICAL_CLOSED_REAL_USER_REPORTED=SEVERAL_HOURS，禁止伪造精确数值。

## 4. T_CLOSED_REAL 必须完整保留墙钟事实

T_CLOSED_REAL_START = 用户首次提交任务的现实时间戳。
T_CLOSED_REAL_END = GPT 最终确认 FINAL_VALID=PASS 的现实时间戳。
T_CLOSED_REAL = END - START。
墙钟不因失败、回虚、用户离开、系统等待或外部暂停而重置。

## 5. T_CLOSED_REAL 只做归因分解，不产生新锚

为了知道时间洞在哪里，T_CLOSED_REAL 的每个墙钟区间必须且只能归入一个诊断桶，避免重复计时：

T_MATURE_NECESSARY = 成熟方案必要执行路径。
T_AI_WAIT = AI/工具排队、生成、调用、响应等待。
T_HUMAN_READ = 用户阅读结果。
T_HUMAN_UNDERSTAND = 用户理解/判断。
T_HUMAN_COPY_INPUT = 用户复制、粘贴、打开目标执行器并提交。
T_HUMAN_CONFIRM = 用户进行中间确认或批准。
T_REWORK = 因方案或门禁不成熟发生的返工。
T_BUGFIX = 修复脚本、合同、验证器、权限兼容等错误。
T_ENV_DELTA = 处理现实环境差异。
T_AUTOMATION_FAILURE = 自动桥、总线、浏览器、执行器通信失败。
T_EXTERNAL_PAUSE = 用户去做无关事情或其他外部暂停。

归因桶只用于诊断和压缩 T_CLOSED_REAL；它们不是新的优化锚。

## 6. 唯一任务完成条件

TASK_COMPLETED=TRUE
CLOSED_LOOP=TRUE
VALID_REAL=PASS
GPT_FINAL_VALID=YES

只有以上全部成立，T_MATURE 和 T_CLOSED_REAL 才允许收口。

## 7. v4.7 第一优先级：消灭人在中间的编排延迟

当前最大 GAP 已从模型/工具运行时间转移到 Human-in-the-loop orchestration latency（人在闭环中的编排延迟）。
v4.7 优先优化：READ、UNDERSTAND、COPY、PASTE、ROUTE、CONFIRM、人工结果回传和中间等待。
不优先继续把 3分14秒内部时间抠几秒，除非闭环墙钟已接近 T_MATURE*。

## 8. 目标自动闭环

用户只提交一次初始任务。
GPT 自动虚拟成熟并冻结。
原子发布门立即生成并发布/发送现实验收任务。
Codex 自动现实执行并回传证据。
GPT 自动判断 PASS 或 Reality Delta。
若 FAIL：自动 STOP -> 回虚 -> 重新成熟 -> 再冻结 -> 再触发原子发布门 -> 再执行。
只有 FINAL_VALID=PASS 或确实需要用户决策时才通知用户。

## 9. 自动闭环硬门

INITIAL_USER_INPUT_COUNT=1
MANUAL_MIDDLE_COPY_PASTE=0
MANUAL_CODEX_INPUT=0
MANUAL_RESULT_RELAY=0
MANUAL_BROWSER_ROUTING=0
GPT_TO_CODEX=AUTO
CODEX_TO_GPT=AUTO
REALITY_DELTA_RETURN=AUTO
SECOND_FREEZE=AUTO
SECOND_EXECUTION=AUTO
VIRTUAL_COMPLETE_IMPLIES_REAL_COMMAND_EMITTED=TRUE
FINAL_VALID=PASS
CLOSED_LOOP_AUTONOMOUS=PASS

## 10. 自动化工程优先级

P0 = v4.7 双时间单闭环合同现实实现。
P1 = 虚→实原子发布门回归认证。
P2 = GPT <-> Codex 自动闭环兼容性/回归认证。
P3 = Playwright 原生 AI 浏览器在 v4.7 下兼容性/回归认证。
P4 = GPT <-> Browser <-> Codex <-> GPT 无人值守多轮闭环。
P5 = 故意注入一个可恢复 Reality Delta，验证自动回虚、再冻结、再发布、再执行。
P6 = 比较同一个 T_CLOSED_REAL 在人工模式和自动模式下的现实结果。

## 11. V47-AUTOMATION-CLOSED-LOOP-01

这是 v4.7 第一现实验收任务。
要求用户只输入一次任务；GPT 自动成熟；冻结成功同轮必须触发原子发布门；Codex 自动执行并回传；GPT 自动验证；注入一个可恢复 Reality Delta；系统自动第二次冻结、第二次原子发布和执行；Verifier PASS 后才通知用户。

硬门：
INITIAL_USER_INPUT_COUNT=1
MANUAL_MIDDLE_COPY_PASTE=0
MANUAL_CODEX_INPUT=0
MANUAL_RESULT_RELAY=0
MANUAL_BROWSER_ROUTING=0
GPT_TO_CODEX=AUTO
CODEX_TO_GPT=AUTO
REALITY_DELTA_RETURN=AUTO
SECOND_FREEZE=AUTO
SECOND_REAL_COMMAND_EMITTED=AUTO
SECOND_EXECUTION=AUTO
FINAL_VALID=PASS

## 12. Playwright / Codex 不是从零研发

本轮默认采用回归认证思路：已有成熟 GPT-Codex 执行闭环和 Playwright 原生 AI 浏览器资产先作为成熟方案候选；v4.7 只验证它们在当前双时间单闭环合同下是否兼容、连续、无人值守。
如果旧资产与当前现实不兼容，记录最小 Reality Delta 后回虚，不重做整套架构。

## 13. 交付指标

每次 v4.7 自动化实验至少输出：
T_MATURE_STAR
T_CLOSED_REAL
T_CLOSED_REAL_MODE=MANUAL|AUTOMATED
AUTOMATION_SAVED_TIME
AUTOMATION_REDUCTION_PERCENT
MANUAL_MIDDLE_INTERVENTIONS
VIRTUAL_COMPLETE_IMPLIES_REAL_COMMAND_EMITTED
REAL_DISPATCH_MODE
CLOSED_LOOP_AUTONOMOUS
FINAL_VALID

人工/自动只是同一个 T_CLOSED_REAL 的实验条件，不是新增核心时间。

## 14. Reality Foundation 与已知错误门

Reality Foundation=local-ai-reality-foundation@1.1.3。
已知 Temp/AppData staging、Here-String 插值、w32tm 权限、FETCH_HEAD 权限、只读探针假阴性、四定位序号、发布时间、虚完成但未发布实命令等已吸收限制必须继续前置拦截。
已知同类原因再次进入 REAL，分类为 GATE_REGRESSION。

## 15. GitHub / Browser / Codex 的角色

GPT=推理与最终裁决。
Codex=现实执行器。
Playwright Native AI Browser=浏览器通信/网页执行桥。
GitHub=共同事实源和结果持久化，不默认作为 REAL 启动硬依赖。

## 16. 当前冻结结论

v4.6.0 已得到精确 clean T_MATURE*=00:03:14.419。
v4.7.1 新增“虚→实原子发布门”：以后不存在“虚已经完成但现实命令等用户再问一次”的合法状态。
v4.7 的首要目标仍是把 T_CLOSED_REAL 从小时级现实体验压向分钟级，并最终逼近 T_MATURE*。

一句话：虚成熟不是一句状态声明；虚成熟的最后一个原子动作必须是生成、编号并发布现实验收任务。
