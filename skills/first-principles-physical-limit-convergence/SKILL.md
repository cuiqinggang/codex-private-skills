---
name: first-principles-physical-limit-convergence
description: 极限短时间引擎 v4.7.2。最终确定性版：一虚一实、双时间单闭环、唯一 E00→E90 状态序列、机器状态转换门、虚内现实预跑、单 Freeze 单 REAL、虚→实原子发布。
metadata:
  version: "4.7.2"
  display_name: "极限短时间引擎"
---

# 极限短时间引擎 v4.7.2

## 0. 永久核心

METHOD_STEPS=2
STEP_1=VIRTUAL
STEP_2=REAL
THIRD_STEP=NONE

T_MATURE_STAR = 成熟方案在完整有效约束下的最短必要有效时间。
T_CLOSED_REAL = 用户首次提交到 GPT FINAL_VALID=PASS 的真实墙钟时间。
第三个核心时间禁止建立。

当前成熟锚：T_MATURE_STAR=00:03:14.419，来源 ESTE-20260923-003。

## 1. 唯一执行状态序列

执行状态不是方法步骤。方法仍只有 VIRTUAL / REAL；状态仅用于机械约束执行。

E00 TASK_BIND
E10 TIME_BIND
E20 REALITY_BIND
E30 VIRTUAL_MATURE
E40 GPT_PREEXEC
E50 FREEZE
E60 ATOMIC_DISPATCH
E70 REAL_EXEC
E80 REAL_JUDGE
E90 FINAL_CLOSE

唯一正常路径：
E00 -> E10 -> E20 -> E30 -> E40 -> E50 -> E60 -> E70 -> E80 -> E90

唯一失败回路：
E80.FAIL -> E20

回路规则：同一 TASK_TIME_ID；CYCLE_ID+1；时间不重置；TASK_SEQUENCE 不重置；必须产生 NEW_FREEZE_ID；不得直接从 E80 回 E70。

任何未列出的跳转一律 INVALID_TRANSITION=BLOCK。

## 2. 每个状态都必须显式携带核心时间

每个状态输出都必须包含：
ENGINE_VERSION=4.7.2
TASK_TIME_ID=<id>
CYCLE_ID=<Cnn>
STATE_ID=<Exx>
PHASE=VIRTUAL|REAL|FINAL
T_MATURE_STAR=00:03:14.419
T_CLOSED_REAL_START=<timestamp>
T_CLOSED_REAL_NOW=<elapsed wall clock or exact timestamps>
NEXT_STATE=<Exx|FINAL|BLOCK>
TIME_CORE_VISIBLE=PASS

缺少上述任一核心字段，STATE_OUTPUT_VALID=NO。
因此任何讨论都不能把最核心的时间忘掉。

## 3. E00 TASK_BIND

建立唯一 TASK_TIME_ID、页面名、任务名、CYCLE_ID=C01。
记录用户首次提交时间，作为 T_CLOSED_REAL_START。
新任务 TASK_SEQUENCE 从 01 开始。

## 4. E10 TIME_BIND

绑定 T_MATURE_STAR 参考值、墙钟起点、活动时间账本。
TIME_LEDGER_READY=PASS 才能进入 E20。

## 5. E20 REALITY_BIND

加载 Reality Foundation=local-ai-reality-foundation@1.1.3。
加载所有已知失败门：Temp/AppData executable staging、Here-String 插值、w32tm 权限、FETCH_HEAD 权限、只读 probe 假阴性、四定位/序号/发布时间、原子发布。
已知同类错误再次进入 REAL = GATE_REGRESSION。

## 6. E30 VIRTUAL_MATURE

只做虚拟成熟：现实约束下寻找最短完整有效方案。
不得创建第三步骤，不得把日志/检查点包装成 V1/V2/R1/R2。

## 7. E40 GPT_PREEXEC

继承 v4.6.1：凡 GPT 当前工具能低成本真实预跑的关键公开子路径，冻结前必须先实际跑成功并留证据。
CAN_GPT_REAL_PREEXECUTE=YES -> PREEXEC_RESULT=PASS 才能继续。
无法等价预跑的本机/GPU/登录态/Windows 专属差异明确标记 UNEXECUTABLE_BY_GPT，留给 REAL。
预跑只在预期减少整体闭环返工时执行。

## 8. E50 FREEZE

冻结前必须全部 PASS：
FINAL_VALID_CONDITION_DEFINED
EXECUTION_CHAIN_CLOSED
EXTERNAL_DEPENDENCIES_CLOSED
CODEX_POLICY_COMPATIBILITY
KNOWN_FAILURE_GATES
POSITION_AND_SEQUENCE_GATE
TIME_LEDGER_READY
PREEXEC_EVIDENCE_READY

生成唯一 FREEZE_ID。
同一 FREEZE_ID 的 REAL_RELEASE_COUNT 初始必须为 0。

## 9. E60 ATOMIC_DISPATCH

继承 v4.7.1：VIRTUAL 完成与 REAL 命令发布是一个原子事务。
同一轮必须依次完成：
NEXT_SEQUENCE_ASSIGNED
FOUR_LOCATOR_REAL_LABEL_CREATED
REAL_HANDOFF_SELF_CONTAINED
PASS_FAIL_CONTRACT_DEFINED
GPT_DISPATCH_TIMESTAMP_RECORDED
ACTIVE_TOTAL_BEFORE_DISPATCH_RECORDED
REAL_COMMAND_EMITTED_OR_AUTO_DISPATCHED

只有全部 PASS 才允许：VIRTUAL_COMPLETE=YES 且 CURRENT_PHASE=REAL。
HANDOFF_READY 但没有现实命令 = INVALID。

四定位唯一格式：【页面名｜任务名｜序号｜虚/实】。
序号只作审计，不是方法步骤。

## 10. E70 REAL_EXEC

Codex 是默认现实执行器；PowerShell/Browser/Local Tools 是内部确定性工具。
继承 v4.6.2：同一 FREEZE_ID 只允许一次正式 REAL 发布。
REAL_RELEASE_COUNT 必须从 0 变 1；若已为 1，再次发布同一 FREEZE_ID = BLOCK。
REAL 禁止重新设计、补方案、现场修复。

## 11. E80 REAL_JUDGE

PASS：验证真实结果与冻结 VALID 条件；进入 E90。
FAIL：只记录最小 Reality Delta；STOP；不得直接重试；回 E20；CYCLE_ID+1；吸收必要现实事实；重新预跑；生成 NEW_FREEZE_ID；NEXT_SEQUENCE=LAST_VALID_SEQUENCE+1。

## 12. E90 FINAL_CLOSE

只有 VALID_REAL=PASS、GPT_FINAL_VALID=YES、TIME_ACCOUNTING_COMPLETE=YES 才能结束。
记录 T_MATURE 样本、T_CLOSED_REAL_END、T_CLOSED_REAL。
执行 Foundation absorb check。
可复用事实写入 GitHub 共同事实源并回读验证。

## 13. 双时间单闭环

T_MATURE_STAR 负责回答：成熟方案本体最短需要多少有效工作时间。
T_CLOSED_REAL 负责回答：用户现实从提交到最终交付到底等了多久。

T_CLOSED_REAL 的诊断桶只能用于归因，不创建第三核心：
T_MATURE_NECESSARY, T_AI_WAIT, T_HUMAN_READ, T_HUMAN_UNDERSTAND, T_HUMAN_COPY_INPUT, T_HUMAN_CONFIRM, T_REWORK, T_BUGFIX, T_ENV_DELTA, T_AUTOMATION_FAILURE, T_EXTERNAL_PAUSE。

## 14. 自动闭环目标

用户只提交一次；GPT 自动虚；自动发送给 Codex；Codex 自动实并回传；GPT 自动判定；若 Reality Delta 则自动回虚、重新冻结、再次发布和执行；FINAL_VALID 后才通知用户。

自动验收硬门：INITIAL_USER_INPUT_COUNT=1；MANUAL_MIDDLE_COPY_PASTE=0；MANUAL_CODEX_INPUT=0；MANUAL_RESULT_RELAY=0；MANUAL_BROWSER_ROUTING=0；GPT_TO_CODEX=AUTO；CODEX_TO_GPT=AUTO；REALITY_DELTA_RETURN=AUTO；SECOND_FREEZE=AUTO；SECOND_EXECUTION=AUTO；FINAL_VALID=PASS；CLOSED_LOOP_AUTONOMOUS=PASS。

## 15. GitHub / Browser / Codex

GPT=推理与最终裁决。
Codex=现实执行器。
Playwright Native AI Browser=浏览器通信/执行桥。
GitHub=共同事实源，不是默认 REAL 启动硬依赖。

## 16. 机器执行门

任何状态转换在执行前必须通过 deterministic state validator。
validator 只接受合同允许的 from_state -> to_state、必需字段、时间核心、序号、FREEZE_ID、REAL_RELEASE_COUNT。
validator FAIL -> EXECUTION=BLOCK；AI 不得用自然语言解释绕过。

## 17. 最终不变量

METHOD_STEP_COUNT=2
TIME_CORE_VISIBLE_ALWAYS=TRUE
STATE_SEQUENCE_REQUIRED=TRUE
ILLEGAL_TRANSITION_BLOCKED=TRUE
VIRTUAL_COMPLETE_IMPLIES_REAL_COMMAND_EMITTED=TRUE
ONE_REAL_PER_FREEZE_ID=TRUE
REAL_FAIL_REQUIRES_NEW_FREEZE_ID=TRUE
REAL_FAIL_DOES_NOT_RESET_TASK_TIME_ID=TRUE
REAL_FAIL_DOES_NOT_RESET_SEQUENCE=TRUE
FINAL_REQUIRES_TIME_ACCOUNTING_COMPLETE=TRUE

一句话：规则不是建议；进入本技能后只能沿 E00→E90 状态机执行，机器门不通过就不能继续。
