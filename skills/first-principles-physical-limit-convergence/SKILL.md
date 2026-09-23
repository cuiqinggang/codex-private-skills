---
name: first-principles-physical-limit-convergence
description: 极限短时间引擎 v4.6.2。只有“虚/实”两步；以完整 GPT→Codex→现实证据→GPT 收口的整体闭环有效工作时间为唯一优化锚定物。
metadata:
  version: "4.6.2"
  display_name: "极限短时间引擎"
---

# 极限短时间引擎 v4.6.2

## 唯一目标

TASK_COMPLETED=TRUE
CLOSED_LOOP=TRUE
T_VALID_RUN=measure(UNION(REQUIRED_LOOP_ACTIVE_INTERVALS))
T*=min(T_VALID_RUN)

在任务真正完成、闭环完整的前提下，让“问题进入 → GPT 虚拟成熟 → Codex 现实执行 → 现实证据返回 → GPT 最终确认”所消耗的有效智能体工作时间最短。
局部更快但破坏完整闭环的方案，不是有效候选。

## 方法永远只有两步

1. 虚 VIRTUAL
2. 实 REAL

唯一状态转换：VIRTUAL -> REAL；REAL PASS -> FINAL；REAL FAIL -> VIRTUAL。
检索、组合、冻结、预检、检查点、Reality Delta、日志都只是两步内部动作，不得再编号成 V1/V2/R1/R2。

## 现实底座

Reality Foundation=local-ai-reality-foundation@1.1.6
虚开始前必须读取与任务相关的最小充分现实约束。
已知 Codex 现实限制必须在虚阶段规避：Temp/AppData 可执行脚本 staging 风险；PowerShell 双引号 Here-String 变量提前展开风险；w32tm 非管理员 Access Denied；workspace-write 下 .git/FETCH_HEAD 写权限失败；只读 nvidia-smi 可能出现“有效 stdout + 非零 exit status”冲突。
已知同类错误再次穿过“虚”进入“实”，视为 Gate Regression。

## 虚：一次完成成熟与交付

虚的目标：冻结预测整体 T_VALID_RUN 最短的完整有效方案。
冻结前必须同时满足：REALITY_FOUNDATION_SUFFICIENT、FINAL_VALID_CONDITION_DEFINED、EXECUTION_CHAIN_CLOSED、EXTERNAL_DEPENDENCIES_CLOSED、CODEX_POLICY_COMPATIBILITY、KNOWN_FAILURE_GATES、POSITION_AND_SEQUENCE_GATE、TIMING_CONTRACT_READY、FROZEN_SOLUTION、HANDOFF_READY 全部 PASS。
虚完成时必须在同一轮直接交付“实”的 Codex 自包含任务，不允许留下“再问一次怎么执行 / 再下载 / 再生成命令”的无价值往返。

## v4.6.1：虚内现实预跑证据门

“虚拟成熟”不得只等于“推理认为可行”。

凡 GPT 在当前会话里已经具备现实执行/访问能力、并且能够低成本复现冻结方案的关键公开子路径，冻结前必须先真实执行该子路径并形成证据。

固定规则：

```text
CAN_GPT_REAL_PREEXECUTE=YES
-> MUST_REAL_PREEXECUTE_BEFORE_FREEZE=YES
-> EVIDENCE_REQUIRED=YES
-> PREEXEC_RESULT=PASS 才允许该子路径进入 FROZEN_SOLUTION

CAN_GPT_REAL_PREEXECUTE=NO
-> 明确标记 UNEXECUTABLE_BY_GPT
-> 只把环境专属剩余差异交给 REAL
```

预跑仍属于 VIRTUAL 内部动作，不新增第三步。

预跑证据至少证明与当前冻结主张直接相关的事实，例如：
- 公共资源/URL真实存在并能取得；
- 文件内容、大小、哈希或 revision 与冻结目标一致；
- 可由 GPT 当前工具实际完成的 API / GitHub / Web / 文件动作已经成功；
- 若预跑失败，必须在“虚”中修正、换成熟路径或 BLOCK，不得把未经预跑的同一路径直接发布给 Codex 试错。

只有本机专属、账号专属、GPU专属、浏览器登录态专属、Windows执行上下文专属等 GPT 无法等价复现的剩余差异，才允许进入 REAL。

这条门的目的不是增加测试数量，而是减少“理论方案 -> Codex失败 -> 回虚”的返工时间；若某项预跑不能降低完整 T_VALID_RUN，则不增加无价值测试。

## v4.6.2：发布时间账本 + REAL 单次发布纪律

规则存在但未执行，等于规则无效。v4.6.2 把以下两项升级为不可绕过发布门。

### A. 时间账本门

在任何 VIRTUAL -> REAL 发布前，必须已经存在：

```text
TASK_TIME_ID
PROBLEM_ENTRY_TIMESTAMP
ACTIVE_TOTAL_BEFORE_DISPATCH
GPT_DISPATCH_TIMESTAMP
TIME_LEDGER_READY=PASS
```

REAL 回来后必须补齐：

```text
CODEX_ACTIVE_START_TIMESTAMP
CODEX_ACTIVE_END_TIMESTAMP
CODEX_PROCESS_ACTIVE_MS
GPT_POST_RETURN_ACTIVE_MS
TIME_ACCOUNTING_COMPLETE=PASS
```

若缺任一关键字段：

```text
FINAL_VALID=BLOCK
T*=NOT_ELIGIBLE
```

允许保留功能性 PASS，但不得把该样本用于 T* 或成熟时间基线。

### B. REAL 单次发布纪律

同一冻结方案只允许一次正式 REAL 认证。

```text
FREEZE_ID=S*
-> REAL_RELEASE_COUNT=1
```

如果 REAL FAIL：

```text
STOP
-> RETURN_TO_VIRTUAL
-> 吸收 Reality Delta
-> 重新预跑
-> 生成 NEW_FREEZE_ID
-> 只有新冻结完成后才允许下一次 REAL
```

禁止：

```text
REAL FAIL
-> 不回虚成熟
-> 直接改一点命令
-> 再发下一条 REAL
```

连续 Codex 试错不属于现实认证，而属于未完成的虚拟成熟返工。

### C. 发布序号不是方法步骤

TASK_SEQUENCE 仅是审计发布序号，不是“第 N 步”。

```text
METHOD_STEP_COUNT=2
TASK_SEQUENCE_ROLE=AUDIT_ONLY
```

用户可见表述不得把 08、09 等发布序号描述成“第八步/第九步”。
真正的方法永远只有：

```text
VIRTUAL
REAL
```

## 实：Codex 是默认执行器

完整闭环：GPT -> Codex -> PowerShell/Browser/Local Tools -> 本机现实证据 -> Codex 正式结果 -> GPT -> FINAL_VALID。
固定角色：REASONING_BRAIN=GPT；EXECUTOR=CODEX；DETERMINISTIC_TOOLS=PowerShell/Browser/Local Tools；FINAL_JUDGE=GPT。
PowerShell 是 Codex 内部工具，不替代 Codex 执行器。
实阶段禁止现场重新设计或修复。失败只允许：最小 Reality Delta -> STOP -> 回虚；累计时间不重置。

## 四定位 + 单调序号

每个 GPT -> Codex 执行任务必须使用：【页面名｜任务名｜序号｜虚/实】。
第三字段 SEQUENCE 是同一 TASK_TIME_ID 下的单调递增发布序号。
INITIAL_SEQUENCE=01；NEXT_SEQUENCE=LAST_VALID_EMITTED_SEQUENCE+1。
REAL FAIL、返回虚、方法版本升级都不重置序号；只有新 TASK_TIME_ID 才从 01 开始。
Codex 开头与最后一行必须原样回显同一四定位标签。

## 时间接力

每个整体问题建立 TASK_TIME_ID 与 PROBLEM_ENTRY_TIMESTAMP。
每次 GPT 发布 Codex 任务记录：TASK_TIME_ID、TASK_SEQUENCE、GPT_DISPATCH_TIMESTAMP、ACTIVE_TOTAL_BEFORE_DISPATCH。
Codex 接手记录：CODEX_ACTIVE_START_TIMESTAMP、CODEX_START_TICK、CODEX_STOPWATCH_FREQUENCY。
Codex 结束记录：CODEX_ACTIVE_END_TIMESTAMP、CODEX_END_TICK、CODEX_PROCESS_ACTIVE_MS。
持续时间以 System.Diagnostics.Stopwatch 为权威；绝对时间戳只作审计坐标。
GPT 收到结果后的读取、判断、最终收口继续计入同一 TASK_TIME_ID。用户离开、休息、现实事务造成的空档不计入主动智能体工作时间。

## 整体时间与局部时间

唯一优化指标：T_VALID_RUN=完整闭环的有效工作时间。
T_GPT、T_CODEX、T_REAL、T_VERIFY、T_REWORK、T_HANDOFF 等局部时间只用于找瓶颈，LOCAL_TIMER_ROLE=DIAGNOSTIC_ONLY。
任何新增规则/门禁，只在预期能降低完整任务 T_VALID_RUN 时保留。

## 只读探针语义规则

对冻结的只读、无副作用、结构化探针：SEMANTIC_EVIDENCE_COMPLETE=YES 且 SEMANTIC_GATE=PASS 且 OUTPUT_CONTRADICTION=NO，则 PROBE_VALID=PASS。
若 exit status 非零，只作为诊断信息，不得单独推翻已经成立的完整语义证据。该规则不得推广到写操作或有副作用的命令。

## GitHub 共同事实源

GitHub=SHARED_FACT_SOURCE；GitHub!=DEFAULT_REAL_BOOTSTRAP_TRANSPORT。
现实启动默认不依赖 git fetch / FETCH_HEAD 写入。
产生可复用新事实时：GPT 分析 -> Codex 执行 -> 本机证据 -> GPT 正式结果包 -> GitHub 共同事实源 -> 远端验证 -> GPT 重新读取。
只读解释、未执行方案草拟、读取已有事实或不改变 CURRENT 的查询，不强制制造 Git commit。

## 交付原则

每轮只交付一个明确高价值动作。
虚结束时必须同时给：四定位标签 + 正确 NEXT_SEQUENCE + 发布时间 + 发布前累计有效时间 + 自包含 Codex 实任务。
不默认增加外层 PowerShell 包装、桌面下载、手工搬运或第二次询问。

## 错误吸收原则

现实失败后，不只修当前错误，还必须问：为什么“虚”没有提前挡住它？
若可复用且能减少未来返工时间，则 Reality Foundation 吸收现实限制，和/或虚增加前置门禁。
已知同类原因原则上不得第二次以相同方式进入“实”。

## 计时样本分类

历史 v4.5.x 首次开发过程包含方法设计、返工和多次 Reality Delta。
HISTORICAL_DEVELOPMENT_RUN >= 00:51:07.109。
它是开发/返工成本样本，不是 v4.6.1 成熟运行的 T*，也不是物理下界。
v4.6.1 成熟性能必须重新用干净任务测量：T_VALID_RUN_CLEAN=新 TASK_TIME_ID 下完整一虚一实闭环的真实有效时间；T*=min(VALID CLEAN RUNS)。

## 收口

只有 VALID_REAL=PASS、GPT_FINAL_VALID=YES、TIME_ACCOUNTING_COMPLETE=YES 才允许任务结束。

一句话：不是让某一步最快，而是在完整闭环真正解决问题的前提下，让整个任务最快。
