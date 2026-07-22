# Claude-style 12 Layer（Claude 风格 12 层）失败教训整合补丁

用途：把近期 SuperTool（超级工具）部署中出现的真实错误，嵌入 Claude-style 12 Layer（Claude 风格 12 层）技能包，防止第二次重复犯错。

## 零、中文可审计输出硬规则

这条规则必须高于普通写作风格规则。以后所有计划、命令包、错误、修复、验收、报告，必须让用户能够直接看懂、直接审计。

```text
CHINESE_AUDITABLE_OUTPUT（中文可审计输出）= 必须开启。
NO_ENGLISH_ONLY_PLAN（禁止纯英文计划）= 必须开启。
CHINESE_EXPLANATION_REQUIRED（英文术语必须中文解释）= 必须开启。
```

硬要求：

- 中文优先。面向用户的计划、错误、修复、验收结论必须先写中文。
- 如果必须保留英文层名、英文错误码、英文状态码、英文文件名，必须在同一行或下一行写中文解释。
- 不能只写 `TIME_ONLY_LOOP detected`，必须写 `TIME_ONLY_LOOP（纯耗时间型假执行）已检测到`。
- 不能只写 `claim acceptance matrix missing`，必须写 `claim acceptance matrix（声明验收矩阵）缺失`。
- 用户看不懂的纠错计划，默认判定为不可审计，不能进入最终验收。

错误示例：

```text
TIME_ONLY_LOOP detected.
Repair Loop required.
```

正确示例：

```text
TIME_ONLY_LOOP（纯耗时间型假执行）已检测到：
系统只在等待时间、打印 heartbeat（心跳日志），没有进入真实任务，也没有产生有效产物。

Repair Loop（返修循环）必须启动：
把“等时间”改成“执行真实任务”，并重新跑 Scripts / Deterministic Checks（脚本确定性检查）和 Verification Plane（独立验证平面）。
```

## 一、必须吸收的错误清单

1. 提前结束：要求 2 小时或 4 小时，实际十几分钟就宣布完成。
2. 单点死循环：一个子任务卡住反复重试，拖死全局。
3. 只看总时间：机械等时间，不进入真实任务。
4. 时间巡检假执行：每隔几分钟只写一次时间总结、heartbeat（心跳日志）、进度口号，不产生实际产物。
5. 后台不可见：验证只在日志或报告里，Cursor/Kilo/Codex 真实界面看不到。
6. 多智能体口头化：说用了多智能体，但没有独立上下文、独立文件、独立证据。
7. 验收器只会判失败：只看异常，不看成功信号。
8. 模型路由漂移：原定 OpenRouter DeepSeek V4 Pro，后来回退到 deepseek-v3.2。
9. 证据不足：只给文件夹、总结或报告，没有 action-level evidence（动作级证据）。
10. 总时间结束即停止：时间到了就关闭任务，但目标未完成、未说明未完成项。
11. 英文纠错不可审计：错误码、计划、修复项只写英文，用户看不懂，无法判断错误是否真正修复。

核心修正规则：

```text
长任务必须同时防止两种假执行：
1. 提前结束型假完成。
2. 纯耗时间型假执行。
```

## 二、全局硬参数

所有 12 Layer 长任务命令包必须显式包含：

```text
MIN_RUNTIME
最低运行时间：未达到该时间，不能最终通过。

MAX_RUNTIME
最高运行时间：达到后进入收敛总结，不能机械停掉。

PHASE_TIMEBOX
阶段时间盒：每个阶段有最大可用时间。

SUBTASK_MAX_TIME
单个子任务最大时间：防止卡死在一个任务。

SUBTASK_MAX_RETRY
单个子任务最大重试次数：防止无限返修。

NO_EARLY_EXIT
禁止提前结束：不能十几分钟就宣布长任务完成。

NO_TIME_ONLY_LOOP
禁止纯耗时间型假执行：不能只等时间、不干活。

NO_INFINITE_LOOP
禁止无限循环：卡住必须跳转下一任务。

FAILOVER_TO_NEXT_TASK
失败跳转下一任务：局部失败不能拖死全局。

REAL_WORK_EVIDENCE_REQUIRED
必须有真实工作证据：必须产生动作级证据和产物变化。

VISUAL_STREAM_REQUIRED
必须有可视化执行流：用户要能在 Cursor/Kilo/Codex 看到过程。

MULTI_AGENT_EVIDENCE_REQUIRED
必须有多智能体证据：每个 agent（智能体）要有独立产物。

CHECKPOINT_INTERVAL
检查点间隔：定期保存 checkpoint（断点）。

FINAL_TARGET_ALIGNMENT_REQUIRED
必须最终目标对齐：逐项对齐成熟态目标。

CHINESE_AUDITABLE_OUTPUT
中文可审计输出：英文术语必须配中文解释。

NO_ENGLISH_ONLY_PLAN
禁止纯英文计划：计划、错误、修复、验收不能只有英文。

CHINESE_EXPLANATION_REQUIRED
英文解释必需：英文码、英文层名、英文状态必须中文备注。
```

判定原则：

```text
没有达到最低运行时间 = 不能 Final PASS（最终通过）。
没有真实产物增长 = 不能用耗时抵扣任务。
单个子任务超时 = 记录失败并跳转下一任务。
总时间到达但目标未完成 = 进入 Final Consolidation（最终收敛总结），不得假装完成。
英文纠错计划没有中文解释 = 用户不可审计，不能进入最终验收。
```

## 三、嵌入 12 Layer 的修正规则

### Layer 1 — Control Plane / Orchestrator（主控调度层）

新增控制规则：

- 必须定义最低运行时间、最高运行时间、阶段时间盒、单任务最大时间。
- 必须定义“真实工作量”标准，禁止只跑时间。
- 必须定义什么叫实际进入任务，例如读取配置、修改文件、生成报告、执行验证、保存 checkpoint。
- 必须定义提前结束失败条件和纯耗时间失败条件。
- 必须定义中文可审计输出规则：所有计划、错误、修复、验收必须中文优先，英文必须中文备注。

新增失败条件：

```text
只定义总时长，没有阶段时间盒 = FAIL。
只定义时间目标，没有产物目标 = FAIL。
运行过程中只有 heartbeat（心跳日志）/时间总结，没有真实工作证据 = FAIL（失败）。
只写英文错误码，没有中文解释 = FAIL（失败）。
```

### Layer 2 — Short Entry / Memory（短入口 / 项目记忆层）

新增控制规则：

- 必须读取短入口中的当前真实目标，不允许被旧失败路线污染。
- 必须读取上轮失败清单，包括提前结束、死循环、耗时间假执行、多智能体无证据、模型路由漂移。
- 必须把“本轮不能重复的错误”写入 run constraints（运行约束）。
- 必须读取并执行 CHINESE_AUDITABLE_OUTPUT（中文可审计输出）规则。

新增失败条件：

```text
没有载入上轮失败教训 = FAIL。
继续沿用旧命令包的宽松时间逻辑 = FAIL。
```

### Layer 3 — Skills / Progressive Disclosure（技能按需加载 / 渐进加载层）

新增控制规则：

- 必须加载 12 Layer 原版技能，不允许改写成普通 12 步。
- 必须加载长任务控制补丁：最低运行时间、阶段时间盒、死循环跳转、真实工作证据。
- 必须加载模型路由约束：当前阶段全部走 OpenRouter（统一模型代理），禁止 legacy fallback（旧模型回退）。
- 必须加载中文可审计输出补丁，防止计划、修复和验收变成纯英文。

新增失败条件：

```text
没有加载 12 Layer 原始英文层名和固定顺序 = FAIL。
没有加载反提前结束/反耗时间规则 = FAIL。
```

### Layer 4 — Planning / Work Decomposition（任务拆解层）

新增控制规则：

- 每个子任务必须有：目标、动作、产物、证据、最大时间、最大重试、失败跳转。
- 计划必须把总任务拆成可推进的阶段，而不是一个大循环。
- 必须加入 progress-by-artifact（按产物推进）检查：每个阶段都要产生或更新具体文件。
- 每个英文阶段名、英文错误码、英文状态码都必须有中文备注。

新增失败条件：

```text
只有时间安排，没有产物安排 = FAIL。
一个阶段没有最大耗时限制 = FAIL。
没有“失败后跳到下一任务”规则 = FAIL。
计划只有英文，用户无法审计 = FAIL。
```

### Layer 5 — Subagents / Context Isolation（子智能体 / 上下文隔离层）

新增控制规则：

- 多智能体必须真实落地，不允许只写“让子智能体检查一下”。
- 每个 agent（智能体）必须有独立上下文、独立输入、独立输出、独立证据。
- 每个 agent（智能体）必须生成自己的 report（报告）、evidence（证据）、error log（错误日志）、contribution summary（贡献总结）。
- 每个 agent（智能体）的输出必须中文优先，英文字段后必须写中文解释。

每个 agent 最低字段：

```text
agent_id
智能体编号。

role
角色。

input_context
输入上下文。

working_scope
工作范围。

allowed_tools
允许使用的工具。

forbidden_scope
禁止触碰的范围。

output_file
输出文件。

evidence_file
证据文件。

error_log
错误日志。

contribution_summary
贡献总结。
```

新增失败条件：

```text
没有 agent（智能体）独立文件 = 多智能体 FAIL（失败）。
没有 agent（智能体）证据 = 多智能体 FAIL（失败）。
agent（智能体）自称 final PASS（最终通过） = FAIL（失败）。
agent（智能体）输出只有英文、没有中文解释 = FAIL（失败）。
```

### Layer 6 — Execution Plane（执行平面）

新增控制规则：

- 执行层必须真实执行，不允许只做时间巡检。
- 每个时间窗口必须产生 action-level evidence（动作级证据）。
- 允许 claim（声明）完成，但不能 self-accept（自我验收）。
- 必须记录 command-log（命令日志）、artifact-manifest（产物清单）、execution-claims（执行声明）。
- 实时输出必须中文可读，不能只打印英文状态。

反耗时间检查：

```text
如果连续两个 checkpoint 只有时间总结，没有新增/更新产物：
标记 TIME_ONLY_LOOP（纯耗时间型假执行）。
立即切换到实际任务动作或进入 Repair Loop（返修循环）。
```

新增失败条件：

```text
只打印 elapsed time（已耗时）/ heartbeat（心跳日志）/ waiting（等待中）= FAIL（失败）。
没有修改、检查、生成、验证任何具体对象 = FAIL。
执行层自称 Final PASS（最终通过） = FAIL（失败）。
执行日志只有英文，用户无法判断动作含义 = FAIL（失败）。
```

### Layer 7 — Hooks / Lifecycle Triggers（生命周期钩子层）

新增控制规则：

- preflight 必须检查是否存在纯耗时间风险。
- 每个 checkpoint hook（检查点钩子）必须检查 artifact delta（产物变化）。
- compact（压缩上下文）前必须保存 handoff（交接文件）。
- 子任务超时时必须触发 failover hook（失败跳转钩子）。
- 每个钩子输出必须写中文说明，英文函数名只能作为标识。

新增钩子：

```text
on_checkpoint:
  检查点触发：
  verify artifact_delta > 0 or meaningful_validation_done == true
  验证产物有变化，或者确实完成了有意义的验证。

on_subtask_timeout:
  子任务超时触发：
  stop retry
  停止继续重试。
  mark PARTIAL/BLOCKED
  标记为 PARTIAL（部分完成）或 BLOCKED（被阻塞）。
  jump next task
  跳到下一个任务。

on_time_only_loop_detected:
  检测到纯耗时间型假执行时触发：
  reject cycle
  拒绝本轮 cycle（循环）。
  enter Repair Loop
  进入 Repair Loop（返修循环）。
```

新增失败条件：

```text
checkpoint 只看时间不看产物 = FAIL。
子任务超时仍继续循环 = FAIL。
```

### Layer 8 — Scripts / Deterministic Checks（脚本确定性检查层）

新增控制规则：

- 脚本检查不能只看文件存在，必须检查关键字段和内容。
- 必须检查时间与产物是否匹配。
- 必须检查是否出现 time-only loop（纯耗时间型假执行）。
- 必须检查 OpenRouter 模型路由是否被 legacy 模型覆盖。
- 脚本输出必须有中文解释字段，不能只输出英文布尔值。

建议检查项：

```text
min_runtime_reached
最低运行时间已达到。

max_runtime_not_exceeded
没有超过最高运行时间。

phase_timebox_respected
阶段时间盒被遵守。

artifact_delta_count
产物变化数量。

checkpoint_count
检查点数量。

agent_evidence_count
智能体证据数量。

openrouter_only
只使用 OpenRouter（统一模型代理）。

legacy_model_absent
没有发现旧模型。

time_only_loop_absent
没有发现纯耗时间型假执行。

chinese_auditable_output_present
中文可审计输出存在。
```

新增失败条件：

```text
脚本只检查“文件存在” = FAIL。
没有检查 time-only loop（纯耗时间型假执行）= FAIL（失败）。
没有检查 agent evidence（智能体证据）= FAIL（失败）。
没有检查中文可审计输出 = FAIL（失败）。
```

### Layer 9 — Verification Plane（独立验证平面）

新增控制规则：

- Verification Plane（独立验证平面）必须独立验收 Execution Plane（执行平面）的 claims（声明）。
- 必须同时看成功信号和失败信号。
- 不能“有异常就全失败”，也不能“时间够了就通过”。
- claim acceptance matrix（声明验收矩阵）必须有中文解释列。

成功信号：

```text
real_execution_done
真实执行已完成。

model_route_verified
模型路由已验证。

tool_invoked
工具已调用。

artifact_generated
产物已生成。

checkpoint_saved
检查点已保存。

agent_evidence_present
智能体证据存在。

visual_stream_present
可视化执行流存在。

chinese_auditable_output_present
中文可审计输出存在。
```

失败信号：

```text
early_exit
提前结束。

time_only_loop
纯耗时间型假执行。

infinite_loop
无限循环。

silent_execution
静默执行，用户看不到。

missing_agent_evidence
缺少智能体证据。

legacy_model_detected
检测到旧模型路由。

missing_checkpoint
缺少检查点。

english_only_plan_detected
检测到纯英文计划或纯英文纠错项。
```

新增失败条件：

```text
只按耗时判 PASS = FAIL。
只按日志自述判 PASS = FAIL。
没有 claim acceptance matrix（声明验收矩阵）= FAIL（失败）。
验收结论只有英文、没有中文解释 = FAIL（失败）。
```

### Layer 10 — Repair Loop（返修循环层）

新增控制规则：

- 修复 rejected claims（被拒绝的声明），但不能无限修。
- 每个修复项必须有最大重试次数。
- 修复后必须重新跑 Layer 8 和 Layer 9。
- 对 time-only loop（纯耗时间型假执行）的修复必须从“等时间”切换为“做实际任务”。
- 每个修复项必须中文说明：错误是什么、为什么错、怎么修、复测结果是什么。

新增失败条件：

```text
同一错误重复超过最大重试仍不跳转 = FAIL。
把 rejected claim（被拒绝的声明）写成 residual risk（残余风险）继续 PASS（通过） = FAIL（失败）。
修复后没有 rerun verification（重新验证） = FAIL（失败）。
修复计划只有英文，用户无法审计 = FAIL（失败）。
```

### Layer 11 — Compact / Handoff（压缩交接层）

新增控制规则：

- handoff（交接文件）必须记录哪些任务完成、哪些失败、哪些跳过、为什么跳过。
- 必须记录时间使用情况与产物对应关系。
- 必须记录多智能体证据索引。
- 必须记录下一轮从哪里继续。
- 必须记录本轮英文术语/错误码的中文解释索引，方便用户接着审。

新增失败条件：

```text
只给文件夹路径 = FAIL。
只写“运行了 X 分钟”没有成果索引 = FAIL。
没有 unresolved claims（未解决声明）= FAIL（失败）。
handoff（交接文件）只有英文 = FAIL（失败）。
```

### Layer 12 — Final Acceptance（最终验收层）

新增控制规则：

- Final Acceptance（最终验收）才能宣布最终 PASS（最终通过）。
- 必须逐项对齐用户原始目标。
- 必须明确是否达到成熟态 AI Coding SuperTool 生态站要求。
- 如果未达到，必须给出 PARTIAL（部分完成）/BLOCKED（被阻塞）和下一轮修复入口。
- 最终验收必须中文优先，英文只作为辅助标识。

最终验收必须包含：

```text
final-acceptance.md
最终验收 Markdown 报告。

final-acceptance.json
最终验收 JSON 结构化结果。

target-alignment-matrix.md
目标对齐矩阵。

evidence-index.md
证据索引。

agent-evidence-index.md
智能体证据索引。

routing-integrity-report.json
模型路由完整性报告。

runtime-control-report.json
运行控制报告。

chinese-auditability-report.md
中文可审计性报告。
```

新增失败条件：

```text
没有 final-acceptance.md = 不能 PASS。
没有 final-acceptance.json = 不能 PASS。
时间够但目标未完成 = 不能 PASS。
存在 time-only loop（纯耗时间型假执行）且未修复 = 不能 PASS（通过）。
存在 legacy model routing（旧模型路由）且未修复 = 不能 PASS（通过）。
存在纯英文计划/纯英文纠错项且未补中文解释 = 不能 PASS（通过）。
```

## 四、成熟态目标必须逐项验收

最终必须对齐：

```text
成熟规则
成熟技能索引
成熟工具/插件生态资料
成熟自动化流程
成熟轻入口
成熟重资料库
成熟 Gate Review
成熟 Repair Loop
成熟多智能体分工
成熟多模态流程
长任务承载能力
断点续跑 / checkpoint / handoff 能力
```

每一项只能给：

```text
PASS（通过） / PARTIAL（部分完成） / FAIL（失败） / BLOCKED（被阻塞）
```

每一项必须绑定证据路径。没有证据路径，默认 FAIL。

## 五、最关键的新增反错误规则

```text
Rule A: No Early Exit（禁止提前结束）
未达到 MIN_RUNTIME，不得 Final PASS。

Rule B: No Time-Only Loop（禁止纯耗时间型假执行）
只消耗时间、只写 heartbeat（心跳日志）、只做时间总结，不算执行。

Rule C: No Infinite Subtask Loop（禁止单子任务无限循环）
单个任务超过时间盒或重试次数，必须记录并跳转。

Rule D: Evidence Before Acceptance（先有证据，再谈验收）
没有文件级、命令级、agent（智能体）级证据，不能验收。

Rule E: Visual Runtime Truth（可视化运行真实）
用户在 Cursor/Kilo/Codex 可见执行流里看不到，不算真实验收完成。

Rule F: Execution Claims Are Not Acceptance（执行声明不是最终验收）
Execution Plane（执行平面）只能 claim（声明），Final Acceptance（最终验收）才能 PASS（通过）。

Rule G: Chinese Auditable Output（中文可审计输出）
所有计划、错误、修复、验收必须中文优先；英文术语必须有中文解释。用户看不懂，就不能算纠错完成。
```
