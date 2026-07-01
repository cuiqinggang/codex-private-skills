# Claude-style 12 Layer Compact Core

## 0. 总理解

Claude-style 12 Layer 不是普通 12 步。

它不是：

```text
目标确认 -> 现状读取 -> 风险识别 -> 小步实现 -> 回归验证
```

这种自创流程。

它是一个长任务控制系统：

```text
前 5 层：防止任务乱开始；
第 6 层：真正执行，但不能自我验收；
第 7-10 层：防止假完成；
第 11-12 层：保证交接清楚、最终验收成立。
```

核心作用：

```text
让 AI 长任务有边界、有证据、有验证、有返修、有最终验收。
```

硬规则：

- 必须保留 12 个原始英文层名。
- 必须保留固定顺序。
- 每层必须有中文名和核心作用。
- 每层必须说明边界、连接下一层、失败条件。
- 不能改成普通 12 步。
- 不能改名、不能压缩、不能重解释。

## Layer 1 — Control Plane / Orchestrator

中文名：主控调度层

核心作用：定义任务目标、边界、禁止事项、继续条件、停止条件、返修条件和最终验收条件。

边界：本层不写代码、不执行命令、不做最终验收。它只负责定规则和任务边界。

连接下一层：Layer 1 定清楚边界后，Layer 2 才知道应该读哪些入口文件，不应该读哪些旧材料。

失败条件：目标不清、范围不清、禁止事项不清、停止条件不清、最终验收条件不清，则不能进入 Layer 2。

## Layer 2 — Short Entry / Memory

中文名：短入口 / 项目记忆层

核心作用：只读取短入口和当前项目记忆，避免一开始就吞掉全部历史、旧报告和旧失败路线。

边界：不能全量读取 reports。不能把旧结论、旧路线、旧失败方案当成当前规则。

连接下一层：Layer 2 给出当前状态和可信 source-of-truth，Layer 3 才能按需加载正确技能。

失败条件：没有短入口、当前状态不清、source-of-truth 不清、旧材料污染当前任务，则必须返回 Layer 2。

## Layer 3 — Skills / Progressive Disclosure

中文名：技能按需加载 / 渐进加载层

核心作用：只加载当前任务真正需要的技能、模板和 source-of-truth。

边界：本层只负责选技能和加载技能，不负责拆任务、不负责执行。

连接下一层：Layer 3 把正确技能交给 Layer 4，Layer 4 才能基于正确规则拆任务。

失败条件：技能选错、关键技能遗漏、技能版本不明、技能冲突未处理，则必须返回 Layer 3。

## Layer 4 — Planning / Work Decomposition

中文名：任务拆解层

核心作用：把任务拆成 gate、子任务、产物、验证点和返修路径。

边界：本层只做计划和拆解，不写代码、不替代执行、不替代验收。

连接下一层：Layer 4 判断哪些子任务会产生大量日志、搜索、审计或验证内容，需要交给 Layer 5 做上下文隔离。

失败条件：没有 gate、没有产物清单、没有验证点、没有返修路径，不能进入执行。

## Layer 5 — Subagents / Context Isolation

中文名：子智能体 / 上下文隔离层

核心作用：把会污染主上下文的搜索、审计、日志分析、代码阅读、失败调查、验证辅助等任务隔离到独立上下文中。

它不是简单分工，而是上下文隔离、角色隔离、权限隔离、环境输入隔离、输出摘要隔离。

每个子智能体必须定义：

```text
name
role
description
prompt
input packet
allowed tools
disallowed tools
source scope
forbidden scope
output contract
stop condition
```

默认权限：

```text
research / audit / review / verification 类子智能体默认只读。
默认不允许写文件。
默认不允许删除。
默认不允许读取 secret。
默认不允许写 H:\AI\skills。
默认不允许宣布最终 PASS。
```

边界：Layer 5 不能替代 Execution Plane。Layer 5 不能替代 Verification Plane。Layer 5 不能替代 Final Acceptance。

连接下一层：Layer 5 只把摘要、结论、风险和证据路径交回主控。Layer 6 基于这些被主控接收的摘要进入执行。

失败条件：只写“让子智能体检查一下”但没有角色、权限、输入、输出契约，直接 FAIL。子智能体返回大量原始日志污染主上下文，FAIL。子智能体越权写文件，FAIL。子智能体宣布最终 PASS，FAIL。

## Layer 6 — Execution Plane

中文名：执行平面

核心作用：真正执行任务：改文件、写代码、运行命令、生成产物、记录日志。

硬规则：Execution Plane 只能 claim，不能 self-accept。

边界：它只能提交 execution claims，不能说“所以最终 PASS”。

连接下一层：Layer 6 的 claims 必须交给 Layer 7、Layer 8、Layer 9 检查和验证。

失败条件：没有 execution-claims、没有 command-log、没有 artifact-manifest、执行层自称 final PASS，则必须返回 Layer 6 修复。

## Layer 7 — Hooks / Lifecycle Triggers

中文名：生命周期钩子层

核心作用：在关键生命周期节点提前检查、阻断、触发复验。

边界：Layer 7 是过程中的刹车，不能替代脚本检查、独立验证或最终验收。

连接下一层：Layer 7 触发或要求 Layer 8 运行确定性检查。

失败条件：没有 preflight、没有 forbidden path 检查、工具失败后继续、compact 前没有 handoff，则必须修正。

## Layer 8 — Scripts / Deterministic Checks

中文名：脚本确定性检查层

核心作用：用脚本和可复验检查代替 AI 口头判断。

边界：Layer 8 只输出机器检查结果，不能宣布最终 PASS。

连接下一层：Layer 8 的检查结果进入 Layer 9，由独立验证平面接受或拒绝 claims。

失败条件：没有验证脚本、脚本失败但继续、只检查文件存在不检查关键字段、verification-result 不可解析，则必须修复。

## Layer 9 — Verification Plane

中文名：独立验证平面

核心作用：只读执行产物和脚本结果，独立判断 Execution Plane 的 claims 是否被接受。

硬规则：Verification Plane 负责 acceptance / rejection。

边界：Layer 9 不写代码、不补报告、不美化结论。它只做 acceptance / rejection。

连接下一层：如果有 rejected claims，必须进入 Layer 10 Repair Loop。如果关键 claims 全部 accepted，才可以进入 Layer 11 / Layer 12。

失败条件：没有独立验证、验证平面和执行平面混同、没有 claim acceptance matrix、rejected claims 被忽略，直接 FAIL。

## Layer 10 — Repair Loop

中文名：返修循环层

核心作用：处理被 Verification Plane 拒绝的 claims，回到对应层做最小返修。

硬规则：Repair Loop 处理 rejected claims。失败不能包装成 residual risk。rejected claim 不能写成“后续优化”然后继续 PASS。

连接下一层：修复后必须重新跑 Layer 8 / Layer 9。重新被接受后，才能进入 Layer 11。

失败条件：rejected claims 没处理、失败被包装成 residual risk、没有 before / after、没有 rerun verification、为了 PASS 降低标准，直接 FAIL。

## Layer 11 — Compact / Handoff

中文名：压缩交接层

核心作用：把长任务阶段成果压缩成短摘要、产物索引、证据索引和下一步建议。

边界：Layer 11 不是最终验收。handoff 不能替代 final acceptance。

连接下一层：Layer 11 把被验证接受的结果整理给 Layer 12，Layer 12 才能最终判断 PASS / PARTIAL / BLOCKED。

失败条件：没有 handoff、没有 evidence index、新旧结果混在一起、下一步不清楚、只给文件夹路径，则不能最终关闭任务。

## Layer 12 — Final Acceptance

中文名：最终验收层

核心作用：最终通过权。

硬规则：final-report 不是 final acceptance。execution summary 不是 final acceptance。verification-result 不是 final acceptance。文件夹路径不是 final acceptance。没有 final acceptance，没有 final PASS。

必须有：

```text
final-acceptance.md
final-acceptance.json
```

边界：Final Acceptance 才是最终 PASS 权威。

失败条件：没有 final-acceptance.md，没有 final PASS。没有 final-acceptance.json，没有 final PASS。final_pass 不是 true 却声称 PASS，直接 FAIL。仍有 blocker 却声称 PASS，直接 FAIL。
