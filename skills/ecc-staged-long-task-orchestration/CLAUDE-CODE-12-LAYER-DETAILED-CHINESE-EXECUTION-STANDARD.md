# Claude Code / Claude-style 12 Layer 中文详细执行标准

## 0. 文件定位

本文是 `ecc-staged-long-task-orchestration` 的 12 Layer 中文详细操作标准。

所有复杂长任务、2H endurance validation、8H endurance validation、SkillOpt 长任务、Run Guard、T8H official run，都必须围绕 Claude Code / Claude-style 12 Layer 展开。

本文不是普通 12 步流程。不得改写为：

```text
目标确认
现状读取
风险识别
方案设计
小步实现
回归验证
```

必须保留原始英文层名和固定顺序：

```text
Layer 1 - Control Plane / Orchestrator
Layer 2 - Short Entry / Memory
Layer 3 - Skills / Progressive Disclosure
Layer 4 - Planning / Work Decomposition
Layer 5 - Subagents / Context Isolation
Layer 6 - Execution Plane
Layer 7 - Hooks / Lifecycle Triggers
Layer 8 - Scripts / Deterministic Checks
Layer 9 - Verification Plane
Layer 10 - Repair Loop
Layer 11 - Compact / Handoff
Layer 12 - Final Acceptance
```

## 1. 全局硬规则

### 1.1 12 Layer 是主轴，不是附录

所有任务包必须以 12 Layer 为主轴展开。每个文件、checkpoint、claim、验证脚本、bad-case、final acceptance 都必须能映射到某个 Layer。

如果任务包只列出 12 个标题，但实际执行按其他流程推进，判定为：

```text
ECC_12_LAYER_REWRITTEN_AS_ORDINARY_STEPS_REJECTED
```

### 1.2 每层必须包含固定字段

每个 Layer 必须包含：

```text
Layer X - 原始英文名
中文名：
一、本层定位
二、本层目的
三、本层输入
四、本层动作
五、本层产物
六、本层文件要求
七、本层内容要求
八、本层禁止事项
九、本层时间门槛关联
十、本层多智能体 / 上下文隔离要求
十一、本层验证方法
十二、失败返回
十三、证据路径
十四、连接到下一层的条件
十五、本任务中的具体应用
```

缺少上述关键字段，不得视为该 Layer 完成。

### 1.3 时间门槛不能替代真实流程

必须区分：

```text
Time Gate：是否满足最低时长。
Runtime Driver：是否持续推进到目标时长或 BLOCK。
Real Workload：是否有真实工作产物。
```

2H endurance validation 必须声明：

```text
minimum_elapsed_minutes >= 120
checkpoint_interval_minutes = 15 or 30
required_checkpoint_count_minimum >= 5
final checkpoint must exist
CONTINUOUS_RUNTIME_UNTIL_TARGET_OR_BLOCKED = true
PARTIAL_STARTED_IS_NOT_VALID_STOP_STATE = true
```

8H / T8H endurance validation 必须声明：

```text
minimum_elapsed_minutes >= 480
required_checkpoint_count_minimum >= 8
checkpoint-008h-final must exist
CONTINUOUS_RUNTIME_UNTIL_TARGET_OR_BLOCKED = true
PARTIAL_STARTED_IS_NOT_VALID_STOP_STATE = true
```

### 1.4 多智能体 / 子智能体证据模式必须显式声明

Layer 5 必须声明 evidence mode：

```text
REAL_SUBAGENT_EXECUTION
LOGICAL_CONTEXT_ISOLATION_ONLY
NO_SUBAGENT_EXCEPTION
```

如果任务要求真实子智能体：

```text
REAL_SUBAGENT_EXECUTION_REQUIRED = true
LOGICAL_CONTEXT_ISOLATION_ONLY_NOT_ACCEPTED = true
```

如果只允许逻辑隔离，必须写清楚：

```text
LOGICAL_CONTEXT_ISOLATION_ONLY
```

并提供替代证据：

```text
独立 input
独立 output
files_read
files_written
independent_conclusion
orchestrator_receipt
Verification Plane acceptance
```

不得把逻辑隔离说成真实子智能体执行。

## 2. Layer 1 - Control Plane / Orchestrator

中文名：主控调度层

一、本层定位：定义任务目标、边界、禁止事项、继续条件、停止条件、返修条件和最终验收条件。本层不写代码、不执行命令、不做最终验收。

二、本层目的：回答本次做什么、不做什么、为什么做、什么时候允许开始、什么时候必须停止、什么时候进入下一层、什么时候进入 Final Acceptance。

三、本层输入：用户任务、P1 control spec、P2 preparation packet、P3 final executable package、source-of-truth、历史成功证据、历史失败证据、禁止事项、验收要求、time gate policy、checkpoint policy。

四、本层动作：明确 `task_id`、`task_mode`、`task_level`、`workspace`、`scope`、`out_of_scope`、`forbidden_actions`、`time_gate`、`checkpoint_gate`、`subagent_mode`、`execution_claim_self_accept_allowed=false`、`verification_plane_required=true`、`repair_loop_required=true`、`final_acceptance_required=true`。

五、本层产物：`01-control-plane.md`、`00-run-config.json`、`source-of-truth-confirmation.md`、`forbidden-actions.md`、`acceptance-gates.md`。

六、本层文件要求：`00-run-config.json` 至少包含 task id、minimum elapsed minutes、checkpoint interval、required checkpoint count、continuous runtime、self-accept 禁止、verification、repair、final acceptance 字段。

七、本层内容要求：写清目标、边界、禁止事项、hard gate、soft gate、blocker、failure status code、success status code。

八、本层禁止事项：目标不清就执行；没有 source-of-truth 就启动；没有 time gate 就启动 endurance；没有 P1/P2/P3 就进入 P4。

九、本层时间门槛关联：必须说明是否需要 `minimum_elapsed_minutes`、是否需要 continuous runtime driver、checkpoint 间隔、未满足时长是否允许 PASS。

十、本层多智能体 / 上下文隔离要求：声明 `subagent_required` 与 `subagent_mode`。

十一、本层验证方法：检查 run config、source-of-truth、禁止事项、时间门槛、final acceptance 条件是否完整。

十二、失败返回：返回 Layer 1，状态码 `CONTROL_PLANE_INCOMPLETE_REJECTED`、`SOURCE_OF_TRUTH_MISSING_REJECTED`、`TIME_GATE_MISSING_REJECTED`。

十三、证据路径：列出本层所有配置和确认文件。

十四、连接到下一层的条件：目标、边界、source-of-truth、time gate、forbidden actions 全部明确。

十五、本任务中的具体应用：SkillOpt 2H 任务必须先锁定 shadow-only、candidate-only、no-auto-merge、120 分钟门槛和 final acceptance 要求。

## 3. Layer 2 - Short Entry / Memory

中文名：短入口 / 项目记忆层

一、本层定位：只读取当前任务需要的短入口和可信项目记忆，防止旧报告、旧失败路线、旧结论污染当前任务。
二、本层目的：确定当前任务从哪里接续，哪些材料可信，哪些是反例，哪些旧产物不能复用。
三、本层输入：P2/P3 上下文包、source-of-truth map、历史成功 run 摘要、历史失败 run 摘要、negative evidence。
四、本层动作：建立 `short-entry-index.md`、`trusted-source-index.md`、`negative-evidence-index.md`、`do-not-reuse-index.md`。
五、本层产物：`02-short-entry-memory.md` 与上述索引。
六、本层文件要求：每个 source 标注 path、role、trusted/historical/negative/do-not-reuse、reason、allowed_usage、forbidden_usage。
七、本层内容要求：写清可信入口、旧失败如何处理、旧成功如何参考、不能复用哪些 start timestamp / checkpoint / final acceptance。
八、本层禁止事项：全量吞 reports；把旧失败 run 当正式 run；把旧 PASS 复制成新 PASS；复用旧 start timestamp 或 checkpoint。
九、本层时间门槛关联：确认当前 run 是 fresh start，禁止复用旧 elapsed 和旧 checkpoint。
十、本层多智能体 / 上下文隔离要求：可指定 memory-audit-subagent 或 negative-evidence-audit-subagent；逻辑隔离必须有 input/output/receipt。
十一、本层验证方法：检查 trusted source 与 negative evidence 是否区分，do-not-reuse 是否记录，旧材料是否未污染当前任务。
十二、失败返回：返回 Layer 2，状态码 `SHORT_ENTRY_MEMORY_CONTAMINATED_REJECTED`、`OLD_RUN_REUSE_REJECTED`。
十三、证据路径：列出 source index 路径。
十四、连接到下一层的条件：短入口和可信记忆清晰。
十五、本任务中的具体应用：快速 V2 只能作为 draft evidence，不能作为 2H final acceptance。

## 4. Layer 3 - Skills / Progressive Disclosure

中文名：技能按需加载 / 渐进加载层

一、本层定位：只加载当前任务真正需要的技能、模板和规则。
二、本层目的：防止技能冲突、上下文爆炸、无关技能带偏任务。
三、本层输入：source-of-truth map、skill package paths、templates、P2 skill candidate index、mature path index。
四、本层动作：建立 `skill-load-map.md`、`rule-conflict-resolution.md`、`skill-role-map.md`。
五、本层产物：`03-skills-progressive-disclosure.md` 和上述映射文件。
六、本层文件要求：每个 skill 写明 skill_path、role、loaded_files、used_for_layer、used_for_gate、conflict_risk、resolution。
七、本层内容要求：区分任务本体 source-of-truth、编排层、历史参考、工具补充和不能覆盖主规则的内容。
八、本层禁止事项：不搜索已有技能就自研；误用编排技能为任务本体；忽略 endurance ladder/domain skill。
九、本层时间门槛关联：endurance 任务必须加载 time gate、checkpoint、continuous runtime policy。
十、本层多智能体 / 上下文隔离要求：可设置 skill-search、mature-path-audit、rule-conflict 审查；记录搜索范围和 missing root。
十一、本层验证方法：检查 source-of-truth 是否正确、技能是否按需加载、是否有冲突解决、是否误用技能。
十二、失败返回：返回 Layer 3，状态码 `SKILL_SELECTION_MISSING_REJECTED`、`SOURCE_OF_TRUTH_CONFLICT_REJECTED`。
十三、证据路径：列出 skill-load-map、search logs、conflict resolution。
十四、连接到下一层的条件：技能和规则明确。
十五、本任务中的具体应用：主控使用 `ecc-staged-long-task-orchestration`，领域辅助使用 `skillopt-sample-optimizer`。

## 5. Layer 4 - Planning / Work Decomposition

中文名：任务拆解层

一、本层定位：把任务拆成 gate、checkpoint、子任务、产物、验证点和返修路径。
二、本层目的：回答分几关、每关做什么、每关产物是什么、如何验证、失败回哪一层。
三、本层输入：Layer 1 control plane、Layer 2 memory、Layer 3 skill map、time gate、checkpoint policy、subagent requirements。
四、本层动作：生成 work-breakdown、gate-matrix、checkpoint-plan、artifact-plan、repair-routing-map、bad-case-plan。
五、本层产物：`04-planning-work-decomposition.md`、`work-breakdown.md`、`gate-matrix.md`、`checkpoint-plan.md`、`artifact-plan.md`、`repair-routing-map.md`、`bad-case-plan.md`。
六、本层文件要求：checkpoint-plan 必须包含 checkpoint_name、target_elapsed_minutes、allowed_creation_condition、associated_layer、required_evidence、forbidden_shortcut。
七、本层内容要求：明确每个时间段对应的 Layer、产物、验证、风险；2H 至少 T+0、T+30、T+60、T+90、T+120 final。
八、本层禁止事项：没有计划就执行；只写大纲不写 gate；没有 checkpoint plan；没有 repair route；把等待时间包装成工作。
九、本层时间门槛关联：写清每个 checkpoint 的真实 elapsed 条件、late checkpoint 记录方式、forged checkpoint 直接 FAIL。
十、本层多智能体 / 上下文隔离要求：规划 policy-audit、testcase-design、checkpoint-evidence、verifier-review、final-acceptance-audit。
十一、本层验证方法：检查 gate matrix、checkpoint plan、artifact plan、repair map、每段时间是否有真实工作。
十二、失败返回：返回 Layer 4，状态码 `PLANNING_GATE_MATRIX_MISSING_REJECTED`、`CHECKPOINT_PLAN_MISSING_REJECTED`、`REAL_WORKLOAD_PLAN_MISSING_REJECTED`。
十三、证据路径：列出规划文件路径。
十四、连接到下一层的条件：规划文件齐全且每个 gate 可验证。
十五、本任务中的具体应用：SkillOpt 2H 必须把样本扩展、候选 patch、风险审查、HTML 验收、最终证据拆成时间绑定 gate。

## 6. Layer 5 - Subagents / Context Isolation

中文名：子智能体 / 上下文隔离层

一、本层定位：隔离会污染主上下文的搜索、审计、日志分析、失败调查和验证辅助任务。
二、本层目的：提供独立角色、独立输入、独立输出、权限边界和 evidence receipt。
三、本层输入：Layer 4 子任务计划、source scope、forbidden scope、allowed tools、disallowed tools。
四、本层动作：生成 subagent assignment plan 或 logical context isolation packets。
五、本层产物：`05-subagents-context-isolation.md`、`subagent-assignment-plan.md`、`orchestrator-receipt-log.md`、各 subagent input/output。
六、本层文件要求：每个子智能体必须定义 name、role、description、prompt、input packet、allowed tools、disallowed tools、source scope、forbidden scope、output contract、stop condition。
七、本层内容要求：明确 `REAL_SUBAGENT_EXECUTION` 或 `LOGICAL_CONTEXT_ISOLATION_ONLY`；不得混淆。
八、本层禁止事项：只写“让子智能体检查一下”；子智能体越权写文件；子智能体宣布 final PASS；把逻辑隔离伪装成真实子智能体。
九、本层时间门槛关联：长期任务 checkpoint 必须记录 Layer 5 evidence mode 和 receipt 状态。
十、本层多智能体 / 上下文隔离要求：本层即为该要求的主控层；所有隔离输出必须被 orchestrator 接收。
十一、本层验证方法：Verification Plane 检查每个子智能体或逻辑隔离 packet 的输入、输出、权限、receipt。
十二、失败返回：返回 Layer 5，状态码 `SUBAGENT_EVIDENCE_MISSING_REJECTED`、`LOGICAL_CONTEXT_ISOLATION_MISREPORTED_REJECTED`。
十三、证据路径：列出 subagent input/output、receipt、verification。
十四、连接到下一层的条件：上下文隔离证据被主控接收。
十五、本任务中的具体应用：SkillOpt 可使用逻辑隔离分别审查样本选择、风险控制、候选 patch、最终验收。

## 7. Layer 6 - Execution Plane

中文名：执行平面

一、本层定位：真正执行任务并提交 claims。
二、本层目的：生成实际产物、记录命令、提交执行声明，但不能自我验收。
三、本层输入：Layer 1-5 产物、P3 final executable package、workspace。
四、本层动作：复制 shadow skills、分析样本、生成候选 patch、生成 dashboards、记录 command log。
五、本层产物：`06-execution-plane.md`、`execution-claims.md`、`command-log.md`、`artifact-manifest.md`。
六、本层文件要求：execution claims 必须列 claim_id、claim_text、evidence_paths、risk、expected verification。
七、本层内容要求：只描述做了什么、生成了什么、证据在哪里；不得写 final PASS。
八、本层禁止事项：self-accept；把文件存在当验收；自动合并正式技能；隐藏失败。
九、本层时间门槛关联：2H 任务必须持续推进到 120 分钟或 BLOCK，不能用快速脚本冒充。
十、本层多智能体 / 上下文隔离要求：引用 Layer 5 receipt，不得越权替代。
十一、本层验证方法：Layer 8/9 检查 claims 与 evidence。
十二、失败返回：返回 Layer 6 或 Repair Loop，状态码 `EXECUTION_CLAIMS_MISSING_REJECTED`、`EXECUTION_SELF_ACCEPT_REJECTED`。
十三、证据路径：列出 claims、command log、artifact manifest。
十四、连接到下一层的条件：执行 claims 和 artifacts 完整。
十五、本任务中的具体应用：只在 shadow workspace 模拟 SkillOpt 优化。

## 8. Layer 7 - Hooks / Lifecycle Triggers

中文名：生命周期钩子层

一、本层定位：在关键生命周期节点提前检查、阻断、触发复验。
二、本层目的：防止忘记 preflight、forbidden path、checkpoint、handoff。
三、本层输入：run config、checkpoint plan、forbidden actions、workspace status。
四、本层动作：记录 start hook、checkpoint hook、pre-compact hook、final hook。
五、本层产物：`07-hooks-lifecycle-triggers.md`、`checkpoint-log.md`、hook result files。
六、本层文件要求：每个 hook 包含 timestamp、elapsed_minutes、current_layer、required_evidence、continue_allowed。
七、本层内容要求：覆盖 start、checkpoint、verification、handoff、final acceptance。
八、本层禁止事项：没有 preflight 继续；工具失败后继续；compact 前无 handoff；forged timestamp。
九、本层时间门槛关联：检查 start timestamp 不刷新、checkpoint elapsed 达标、late checkpoint 诚实记录。
十、本层多智能体 / 上下文隔离要求：checkpoint-evidence 审计可辅助，但接受权仍在 Layer 9。
十一、本层验证方法：检查 hook log 是否覆盖关键节点。
十二、失败返回：返回 Layer 7，状态码 `LIFECYCLE_HOOK_MISSING_REJECTED`、`CHECKPOINT_HOOK_FAILED_REJECTED`、`FORGED_TIMESTAMP_REJECTED`。
十三、证据路径：列出 hooks 日志。
十四、连接到下一层的条件：hooks 安全后进入 Layer 8。
十五、本任务中的具体应用：2H SkillOpt 每个 checkpoint 必须绑定当前 12 Layer 状态。

## 9. Layer 8 - Scripts / Deterministic Checks

中文名：脚本确定性检查层

一、本层定位：用脚本和确定性检查替代 AI 口头判断。
二、本层目的：检查文件存在、JSON 可解析、字段完整、时间达标、checkpoint 足够、bad-case 正确失败、valid case 通过。
三、本层输入：artifact manifest、checkpoint log、run config、test cases、execution claims、subagent evidence、final acceptance draft。
四、本层动作：生成并运行 verifier。
五、本层产物：`08-scripts-deterministic-checks.md`、`script-verification-result.md`、`script-verification-result.json`、bad-case test result。
六、本层文件要求：verification JSON 至少包含 final_pass、elapsed_minutes、checkpoint_count、failures、status_code。
七、本层内容要求：检查 elapsed、checkpoint、12 Layer、self-accept、Layer 5 evidence、Verification Plane、Repair Loop、Final Acceptance、bad-case、path-only return。
八、本层禁止事项：脚本 PASS 等于 final PASS；只检查文件存在；脚本失败包装成 residual risk；删除 bad-case 换 PASS。
九、本层时间门槛关联：检查 elapsed_minutes >= minimum_elapsed_minutes、checkpoint_count >= required、timestamp 未伪造。
十、本层多智能体 / 上下文隔离要求：verifier-review 可审计脚本覆盖项。
十一、本层验证方法：Layer 9 读取脚本结果并判断 claims。
十二、失败返回：返回 Layer 8 或 Layer 10，状态码 `DETERMINISTIC_CHECK_FAILED`、`BAD_CASE_TEST_FAILED`、`ELAPSED_TIME_GATE_FAILED`、`CHECKPOINT_GATE_FAILED`。
十三、证据路径：列出 verifier 和结果 JSON。
十四、连接到下一层的条件：Layer 8 结果进入 Layer 9；脚本 PASS 不等于 final PASS。
十五、本任务中的具体应用：验证 SkillOpt 输出、三分类 patch、HTML、manifest、时间门槛。

## 10. Layer 9 - Verification Plane

中文名：独立验证平面

一、本层定位：只读验证，不写代码，不补报告，不美化结论。
二、本层目的：判断 Execution Plane claims 是否 accepted / rejected。
三、本层输入：execution-claims.md、artifact-manifest.md、script-verification-result.json、subagent evidence、checkpoint-log、bad-case result。
四、本层动作：生成 claim acceptance matrix。
五、本层产物：`09-verification-plane.md`、`independent-verification.md`、`claim-acceptance-matrix.md`、`verification-result.md`、`verification-result.json`。
六、本层文件要求：claim matrix 包含 claim_id、claim_text、evidence_paths、script_result、accepted、rejection_reason、repair_required、repair_target_layer。
七、本层内容要求：逐条检查 execution claims、Layer 5 evidence、time evidence、checkpoint evidence、bad-case evidence、final acceptance 前置条件。
八、本层禁止事项：执行层自己验收；所有 claims 一句话全接受；忽略 rejected claims；为了 PASS 降低标准。
九、本层时间门槛关联：接受或拒绝 elapsed、checkpoint、late checkpoint、forged checkpoint。
十、本层多智能体 / 上下文隔离要求：明确 Layer 5 evidence accepted / rejected。
十一、本层验证方法：本层自身是验证层，但仍要被 Layer 12 读取。
十二、失败返回：有 rejected claims 必须进入 Layer 10，状态码 `ECC_VERIFICATION_PLANE_MISSING_REJECTED`、`CLAIM_REJECTED_REPAIR_REQUIRED`。
十三、证据路径：列出 verification result 和 claim matrix。
十四、连接到下一层的条件：rejected claims 被处理。
十五、本任务中的具体应用：决定快速 V2 草稿、候选 patch、risk report 是否可接受。

## 11. Layer 10 - Repair Loop

中文名：返修循环层

一、本层定位：处理被 Layer 9 拒绝的 claims。
二、本层目的：确保失败不被包装成 residual risk。
三、本层输入：rejected claims、claim acceptance matrix、script failures、verification result。
四、本层动作：按失败类型返回对应层修复。
五、本层产物：`10-repair-loop.md`、`repair-loop-log.md`、`rejected-claims-before-repair.md`、`repair-actions.md`、`post-repair-verification-rerun.md`。
六、本层文件要求：每个 repair item 包含 rejected_claim、reason、target_layer、repair_action、before、after、rerun_verification、final_status。
七、本层内容要求：如果没有 rejected claims，必须写 `no open rejection` 并引用 Layer 9 matrix。
八、本层禁止事项：忽略 rejected claims；把 blocker 改成后续优化；降低检查标准；删除坏例；跳过复验。
九、本层时间门槛关联：elapsed/checkpoint 未达标时不能 repair 成 PASS，只能继续 runtime 或 BLOCK。
十、本层多智能体 / 上下文隔离要求：verifier-review / final-acceptance-audit 可复核 repair，但不能替代 Layer 9。
十一、本层验证方法：必须重新跑 Layer 8，并回到 Layer 9。
十二、失败返回：open rejection > 0 时 Layer 12 final_pass 必须 false。
十三、证据路径：列出 repair log 和 rerun verification。
十四、连接到下一层的条件：no open rejection。
十五、本任务中的具体应用：如果发现“2 分钟冒充 2H”，必须返回 Layer 1/4/7/8，而不是 PASS。

## 12. Layer 11 - Compact / Handoff

中文名：压缩交接层

一、本层定位：整理交接，不是最终验收。
二、本层目的：把长任务结果整理成可读、可复查、可接续的证据包。
三、本层输入：all layer files、artifact manifest、verification result、repair loop log、checkpoint log。
四、本层动作：生成 evidence packet。
五、本层产物：`11-compact-handoff.md`、`compact-handoff.md`、`evidence-index.md`、`artifact-index.md`、`next-step-recommendation.md`、`codex-evidence-return-packet.md`。
六、本层文件要求：return packet 包含 TASK_ID、Workspace、Skills used、12 Layer status、Execution claims、Deterministic checks、Verification Plane result、Repair Loop、Handoff、Final acceptance summary、Final status codes、Open issues、Request GPT final acceptance。
七、本层内容要求：不能 path-only。
八、本层禁止事项：只返回路径；只写已完成；handoff 冒充 final acceptance；隐藏 open rejection。
九、本层时间门槛关联：摘要 elapsed_minutes、checkpoint_count、late checkpoint、recovery event。
十、本层多智能体 / 上下文隔离要求：摘要 Layer 5 evidence mode 和 acceptance。
十一、本层验证方法：Layer 12 读取 handoff 并判断 final pass。
十二、失败返回：状态码 `ECC_CODEX_PATH_ONLY_RETURN_REJECTED`、`HANDOFF_MISSING_REJECTED`。
十三、证据路径：列出 handoff 和 evidence index。
十四、连接到下一层的条件：证据包完整。
十五、本任务中的具体应用：Codex 给 GPT 的回传不能只给 outputs 路径，必须列核心证据摘要。

## 13. Layer 12 - Final Acceptance

中文名：最终验收层

一、本层定位：最终通过权。final-report、verification-result、execution summary、文件夹路径都不是 final acceptance。
二、本层目的：判断最终 PASS / PARTIAL / BLOCKED / REJECTED。
三、本层输入：Layer 1-11、script verification、claim acceptance matrix、repair loop、checkpoint log、final evidence packet。
四、本层动作：生成 final acceptance。
五、本层产物：`12-final-acceptance.md`、`final-acceptance.md`、`final-acceptance.json`、`final-report.md`。
六、本层文件要求：final-acceptance.json 必须包含 task_id、task_mode、final_pass、status_code、elapsed_minutes、checkpoint_count、minimum_elapsed_minutes、required_checkpoint_count_minimum、source_of_truth_confirmed、execution_plane_self_accept_detected、verification_plane_accepted、repair_loop_open_rejections、subagent_evidence_required、subagent_evidence_mode、subagent_evidence_accepted、bad_case_tests_passed、valid_case_passed、open_blockers。
七、本层内容要求：final_pass=true 只能在 elapsed 达标、checkpoint 达标、source-of-truth 正确、P1/P2/P3/P4 成立、Execution Plane 没有 self-accept、Layer 5 evidence accepted、Layer 8 verifier PASS、Layer 9 accepted、Layer 10 no open rejection、bad-case tests passed、final acceptance files 存在、Codex return not path-only、open_blockers=[] 时出现。
八、本层禁止事项：final-report 冒充 final-acceptance；elapsed 不足却 PASS；checkpoint 不足却 PASS；Verification Plane 缺失却 PASS；open blockers 不为空却 PASS；Codex 自己替 GPT 做最终验收。
九、本层时间门槛关联：明确 minimum_elapsed_minutes、actual_elapsed_minutes、checkpoint_count、checkpoint policy、late checkpoint、forged checkpoint。
十、本层多智能体 / 上下文隔离要求：明确 subagent_evidence_required、subagent_evidence_mode、subagent_evidence_accepted。
十一、本层验证方法：GPT 最终审计必须读取 final-acceptance.json、verification-result.json、claim matrix、checkpoint log、subagent evidence。
十二、失败返回：状态码 `ECC_FINAL_ACCEPTANCE_MISSING_REJECTED`、`FINAL_ACCEPTANCE_FIELDS_MISSING_REJECTED`、`FINAL_PASS_WITH_OPEN_BLOCKERS_REJECTED`、`FINAL_PASS_WITHOUT_LAYER5_ACCEPTANCE_REJECTED`、`FINAL_PASS_WITHOUT_VERIFICATION_PLANE_REJECTED`。
十三、证据路径：列出 final acceptance 文件路径。
十四、关闭条件：只有 GPT final acceptance 或明确自动验收规则接受，任务才可关闭。
十五、本任务中的具体应用：2H SkillOpt 必须由 Final Acceptance 决定 PASS，不能由脚本或 Execution Plane 决定。

## 14. Checkpoint 必须绑定 12 Layer

每个 checkpoint 必须写：

```text
checkpoint_name:
timestamp:
elapsed_minutes:
current_layer:
completed_layers:
active_layer:
layer_evidence_paths:
checkpoint_specific_work:
open_risks:
open_rejected_claims:
repair_loop_status:
continue_allowed:
next_layer_target:
interruption_or_recovery_note:
```

checkpoint 不是 Layer 的替代品。checkpoint 只是时间证据。所有 checkpoint 必须证明当前 12 Layer 推进到哪里。

## 15. 状态码补充

```text
CLAUDE_12_LAYER_DETAIL_STANDARD_INSTALLED
CLAUDE_12_LAYER_DETAIL_STANDARD_MISSING_REJECTED
TIME_GATE_IS_NOT_RUNTIME_DRIVER
CONTINUOUS_RUNTIME_DRIVER_REQUIRED
PARTIAL_STARTED_IS_NOT_VALID_STOP_STATE
REAL_SUBAGENT_EXECUTION_REQUIRED
LOGICAL_CONTEXT_ISOLATION_ONLY_ACCEPTED
LOGICAL_CONTEXT_ISOLATION_ONLY_NOT_ACCEPTED
FORGED_CHECKPOINT_TIMESTAMP_REJECTED
LATE_RECOVERY_CHECKPOINT_ACCEPTED
CODEX_RETURN_MUST_REQUEST_GPT_FINAL_ACCEPTANCE
FINAL_EVIDENCE_AUDIT_REQUIRED
```

## 16. 最短使用口令

```text
请使用 CLAUDE-CODE-12-LAYER-DETAILED-CHINESE-EXECUTION-STANDARD.md。

本任务必须严格围绕 Claude Code / Claude-style 12 Layer 展开。
每层必须有中文详细操作、文件要求、内容要求、禁止项、时间门槛关联、多智能体验证要求、Verification Plane 接受条件和失败返回。
不得只列 12 个标题。
不得改写成普通 12 步。
不得跳过 Layer 5。
不得让 Execution Plane self-accept。
不得用 final-report 替代 final-acceptance。
```
