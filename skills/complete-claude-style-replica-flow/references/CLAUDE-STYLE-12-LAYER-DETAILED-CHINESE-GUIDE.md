# Claude-style 12 Layer 详细中文指南

状态码：`CLAUDE_STYLE_12_LAYER_EFFECTIVE_CORE_LOGIC_EXPANDED`

## 目录

1. 编写目标与来源边界
2. 官方支撑点
3. 0. 总原则：这不是普通 12 步，而是 12 个控制层
4. 1. 总体流程图
5. 2. Layer 1 — Control Plane / Orchestrator
6. 3. Layer 2 — Short Entry / Memory
7. 4. Layer 3 — Skills / Progressive Disclosure
8. 5. Layer 4 — Planning / Work Decomposition
9. 6. Layer 5 — Subagents / Context Isolation
10. 7. Layer 6 — Execution Plane
11. 8. Layer 7 — Hooks / Lifecycle Triggers
12. 9. Layer 8 — Scripts / Deterministic Checks
13. 10. Layer 9 — Verification Plane
14. 11. Layer 10 — Repair Loop
15. 12. Layer 11 — Compact / Handoff
16. 13. Layer 12 — Final Acceptance
17. 14. 12 层之间的因果关系
18. 15. 在 GPT-Codex 闭环中的正确应用
19. 16. 任务包必须强制包含的格式
20. 17. 一票否决规则
21. 18. 最终一句话

## 编写目标与来源边界

本指南用于把“完整 Claude-style 复刻流程”沉淀成可复用技能包的主体参考。目标不是把 12 层写得越长越好，而是把每一层的核心作用、边界条件、输入输出、与前后层的关系写准。这样以后 GPT / Codex 看到技能包时，才不会把它改造成另一套流程。

这里的“Claude-style 12 Layer”是用户定义的长任务控制系统，不是 Claude Code 官方文档中逐字定义的官方 12 层标准。Claude Code 官方文档提供的是底层能力支撑：agentic coding、上下文管理、subagent 隔离、skills 按需加载、hooks 生命周期检查、permissions 权限约束，以及先探索、再计划、再编码、再验证的实践方向。本指南把这些能力组合成固定 12 个控制层。

硬边界：

1. 保留 12 个原始英文层名。
2. 保留固定顺序。
3. 保留每层中文名、核心作用、输入、产物、边界、前后关系、失败条件。
4. 不把 12 Layer 改成普通 12 步。
5. 不改名、不压缩、不重解释。
6. 不让 Execution Plane 自验。
7. 不让 Verification Plane 缺席。
8. 不让 Repair Loop 缺席。
9. 不让 Final Acceptance 缺席。

## 官方支撑点

官方资料支撑的是“为什么这些控制层有必要”，不是替代本指南的 12 层定义。

- Claude Code 是 agentic coding 环境，能在终端里协助读代码、改文件、运行命令和处理软件工程任务。参考：`https://code.claude.com/docs/en/overview`
- Claude Code 的上下文会被指令、文件内容、命令输出、工具结果等填满，因此长任务必须做上下文入口控制、压缩和交接。参考：`https://code.claude.com/docs/en/context-window`
- Subagents 有独立上下文窗口，可配置工具权限，适合把研究、审计、验证等大量信息隔离出去，只把摘要返回主控。参考：`https://code.claude.com/docs/en/sub-agents`
- Skills 是按需加载的能力包，通常由 `SKILL.md` 和可选脚本、引用、资产组成，用于把专门流程交给模型在需要时读取。参考：`https://code.claude.com/docs/en/skills`
- Hooks 可在生命周期节点触发命令或检查，例如工具调用前后、通知、停止、子智能体停止等。参考：`https://code.claude.com/docs/en/hooks`
- Permissions / settings 可限制工具访问和工具行为，用于控制可读、可写、可执行范围。参考：`https://code.claude.com/docs/en/permission-modes` 和 `https://code.claude.com/docs/en/settings`
- Claude Code 常见工作流和最佳实践强调先探索、再计划、再编码，并给 Claude 一个可运行的验证信号。参考：`https://code.claude.com/docs/en/common-workflows` 和 `https://code.claude.com/docs/en/best-practices`

这些支撑点对应到本指南：

```text
agentic coding 能力      -> Layer 6 Execution Plane
context / compact        -> Layer 2 Short Entry + Layer 11 Compact / Handoff
subagents 独立上下文     -> Layer 5 Subagents / Context Isolation
skills 按需加载          -> Layer 3 Skills / Progressive Disclosure
hooks 生命周期触发       -> Layer 7 Hooks / Lifecycle Triggers
permissions 权限控制     -> Layer 1 边界 + Layer 5 子智能体权限 + Layer 7 forbidden path
可运行验证信号           -> Layer 8 Scripts / Deterministic Checks
独立判断与最终验收       -> Layer 9 Verification Plane + Layer 12 Final Acceptance
```

## 0. 总原则：这不是普通 12 步，而是 12 个控制层

Claude-style 12 Layer 不能理解成：

```text
第 1 步做 A
第 2 步做 B
第 3 步做 C
……
最后完成
```

它真正的性质是：

```text
一个长任务控制系统。
```

它把一个复杂 AI 编程任务拆成 12 个控制层：

```text
Layer 1  控制目标和边界
Layer 2  控制记忆入口
Layer 3  控制技能加载
Layer 4  控制任务拆解
Layer 5  控制上下文隔离
Layer 6  控制执行产物
Layer 7  控制生命周期风险
Layer 8  控制确定性检查
Layer 9  控制独立验证
Layer 10 控制失败返修
Layer 11 控制交接压缩
Layer 12 控制最终通过权
```

它的核心目的不是“让流程看起来完整”，而是防止 AI 长任务出现以下失败：

1. 一开始目标不清，越做越偏。
2. 上下文被旧报告、旧失败、长日志污染。
3. 技能包全量加载，互相冲突。
4. 任务没有拆 gate，边做边想。
5. 子任务全部塞进主上下文，最后主控失去判断力。
6. 执行者自己宣布成功，形成假 PASS。
7. 没有生命周期阻断，危险动作一直执行到底。
8. 没有脚本验证，只靠 AI 口头判断。
9. 执行和验收混在一起。
10. 失败被包装成 residual risk，而不是返修。
11. 长任务没有交接摘要，下一轮接不上。
12. 没有 final acceptance，却声称最终完成。

所以这 12 层必须保留原名、原顺序、原功能。不能改成普通的“目标确认、现状读取、风险识别、小步实现”那种 12 步。

## 1. 总体流程图

正确的整体逻辑是：

```text
Layer 1 — Control Plane / Orchestrator
先定目标、边界、停止条件和最终验收权
        ↓
Layer 2 — Short Entry / Memory
只读短入口和当前记忆，不把历史垃圾塞进上下文
        ↓
Layer 3 — Skills / Progressive Disclosure
按需加载技能，不全量加载，不让技能冲突
        ↓
Layer 4 — Planning / Work Decomposition
拆 gate、子任务、产物、验证点和返修路径
        ↓
Layer 5 — Subagents / Context Isolation
把搜索、审计、日志分析、验证等会污染上下文的任务隔离出去
        ↓
Layer 6 — Execution Plane
正式执行，但只能提交 execution claims，不能自我验收
        ↓
Layer 7 — Hooks / Lifecycle Triggers
在关键生命周期节点阻断风险动作、触发检查
        ↓
Layer 8 — Scripts / Deterministic Checks
用脚本、bad-case、字段检查做确定性验证
        ↓
Layer 9 — Verification Plane
独立读取 claims 和检查结果，接受或拒绝 claims
        ↓
Layer 10 — Repair Loop
被拒绝的 claims 回到对应层返修，不能包装成风险继续 PASS
        ↓
Layer 11 — Compact / Handoff
生成短交接、证据索引、当前状态，防止上下文污染
        ↓
Layer 12 — Final Acceptance
最终验收。没有 final-acceptance.md / json，就没有最终 PASS
```

可以进一步概括成：

```text
前 5 层：防止乱开始。
第 6 层：真正做事，但不能验收自己。
第 7-10 层：防止假完成。
第 11-12 层：保证长任务可交接、可验收、可关闭。
```

## 2. Layer 1 — Control Plane / Orchestrator

中文名：主控调度层

本层核心问题：谁来决定这次任务的目标、范围、边界、继续、停止、返修和最终验收？

为什么必须有这一层：

AI 长任务最大的风险不是不会做，而是一开始没有边界。如果没有 Layer 1，任务会变成：

```text
用户说一个目标
→ AI 自己猜范围
→ 中途不断扩大
→ 最后做了很多东西
→ 但不一定是用户真正要的东西
```

所以 Layer 1 是总指挥部。它不是执行层，也不是验证层。它负责决定：

1. 本任务要解决什么。
2. 本任务不解决什么。
3. 哪些目录可以动。
4. 哪些目录不能动。
5. 哪些动作必须先审批。
6. 什么情况下继续。
7. 什么情况下停止。
8. 什么情况下进入 repair。
9. 什么情况下允许 final acceptance。
10. 最终状态码如何定义。

本层输入：

1. 用户目标。
2. 任务背景。
3. 当前上下文。
4. 已有技能包。
5. 禁止事项。
6. 时间预算 / 任务等级。

本层产物：

1. `control-plane.md`
2. `task-boundary.md`
3. `stop-conditions.md`
4. `final-acceptance-gate.md`
5. `status-code-policy.md`

本层边界：

Layer 1 不能直接写代码，不能直接验收，不能把“任务目标”直接变成“执行完成”。它只能定义控制规则。

与下一层的关系：

Layer 1 定义边界以后，Layer 2 才知道：

1. 应该从哪些入口读取状态？
2. 哪些历史不要读？
3. 哪些报告是当前可信的？
4. 哪些旧结论已经废弃？

如果 Layer 1 不清楚，Layer 2 就会乱读，后面全部会偏。

失败条件：

1. 没有明确目标。
2. 没有明确禁止事项。
3. 没有 stop 条件。
4. 没有 repair 条件。
5. 没有 final acceptance 条件。
6. 没有状态码规则。

出现以上任意一条，不能进入 Layer 2。

## 3. Layer 2 — Short Entry / Memory

中文名：短入口 / 项目记忆层

本层核心问题：AI 从哪里读取当前状态，才能既掌握重点，又不被旧内容污染？

为什么必须有这一层：

长任务最容易出现的第二个问题是上下文污染。AI 一旦把旧报告、旧失败、旧路径、旧方案全部读进去，就会出现：

1. 旧结论和新结论混在一起。
2. 已废弃路线被重新当成当前路线。
3. 上下文越来越长。
4. 关键规则被淹没。
5. 后续生成的任务包越来越偏。

所以 Layer 2 要求：

1. 只读短入口。
2. 不全量读 reports。
3. 不一开始吞掉所有历史。

短入口应该像“当前地图”一样告诉 AI：

1. 当前任务是什么。
2. 当前阶段在哪里。
3. 可信 source-of-truth 是什么。
4. 最近状态码是什么。
5. 哪些文件必须读。
6. 哪些旧内容不要读。
7. 下一步从哪里开始。

本层输入：

1. Layer 1 的任务边界。
2. 项目短入口文件。
3. 当前状态文件。
4. source-of-truth map。
5. 最近 handoff。

本层产物：

1. `SHORT-ENTRY.md`
2. `PROJECT-MEMORY.md`
3. `CURRENT-STATE.md`
4. `SOURCE-OF-TRUTH-MAP.md`
5. `entry-read-log.md`

本层边界：

Layer 2 不是资料全量收集层。它不能做：

1. 全量读取 reports。
2. 全量读取所有历史工作区。
3. 把旧失败方案重新纳入当前任务。
4. 用旧状态覆盖新状态。

与下一层的关系：

Layer 2 的结果会告诉 Layer 3：

1. 本任务需要哪些技能？
2. 哪些技能已经过时？
3. 哪些技能不该加载？
4. 哪些模板是当前 source-of-truth？

如果 Layer 2 不干净，Layer 3 就会加载错技能。

失败条件：

1. 没有短入口。
2. 当前状态不明。
3. source-of-truth 不明。
4. 全量读取旧 reports。
5. 旧路线污染当前任务。

出现这些问题，必须回 Layer 2 修正。

## 4. Layer 3 — Skills / Progressive Disclosure

中文名：技能按需加载 / 渐进加载层

本层核心问题：本任务到底需要哪些技能？哪些技能不需要？如何避免技能包全量加载和冲突？

为什么必须有这一层：

技能包不是越多越好。技能全量加载会带来三个问题：

1. 上下文爆炸。
2. 技能之间互相冲突。
3. AI 被无关技能带偏。

正确方式是：

1. 任务需要什么技能，就加载什么技能。
2. 只加载当前任务相关的 `SKILL`、template、source-of-truth。
3. 无关技能不读。
4. 旧技能不读。
5. 冲突技能必须标记。

这就是 Progressive Disclosure：渐进加载、按需暴露。

本层输入：

1. Layer 2 的当前状态。
2. source-of-truth map。
3. 任务类型。
4. 候选技能路径。
5. 候选模板。

本层具体工作：

1. 判断任务类型。
2. 搜索或定位相关技能包。
3. 只读技能摘要和必须模板。
4. 判断技能版本是否适用。
5. 标记不使用的技能。
6. 标记冲突技能。
7. 形成技能加载清单。

本层产物：

1. `skill-load-plan.md`
2. `selected-skills.md`
3. `skill-source-map.md`
4. `unused-skills.md`
5. `skill-conflict-log.md`

本层边界：

Layer 3 不能替代计划层。它只负责选技能、加载技能、解释技能适用性。它不能直接拆任务，也不能直接执行。

与下一层的关系：

Layer 3 把正确技能交给 Layer 4。Layer 4 才能基于正确规则拆 gate、产物和验证点。如果 Layer 3 选错技能，Layer 4 拆出来的任务一定会错。

失败条件：

1. 没有技能加载清单。
2. 技能全量加载。
3. 关键技能缺失。
4. 技能版本不明。
5. 技能冲突未处理。
6. 无关技能污染任务。

出现这些问题，必须回 Layer 3。

## 5. Layer 4 — Planning / Work Decomposition

中文名：任务拆解层

本层核心问题：如何把目标拆成可执行、可验证、可返修的 gate？

为什么必须有这一层：

没有 Layer 4，AI 会直接进入执行：

```text
看起来知道目标
→ 直接改代码
→ 改到一半发现范围不清
→ 再补报告
→ 再补验证
→ 最后变成混乱产物
```

Layer 4 的作用是把任务拆清楚：

1. 分几关做？
2. 每一关做什么？
3. 每一关的产物是什么？
4. 每一关怎么验收？
5. 每一关失败后回哪一层？
6. 哪些是硬门槛？
7. 哪些只是优化项？

本层输入：

1. Layer 1 的任务边界。
2. Layer 2 的当前状态。
3. Layer 3 的技能加载结果。

本层产物：

1. `gate-plan.md`
2. `work-decomposition.md`
3. `artifact-plan.md`
4. `verification-plan.md`
5. `repair-path-map.md`
6. `bad-case-plan.md`

本层边界：

Layer 4 只做计划和拆解，不做真实执行。它不能：

1. 改代码。
2. 生成最终验收结论。
3. 用计划代替执行产物。
4. 用计划代替验证结果。

与下一层的关系：

Layer 4 拆完以后，必须判断：

1. 哪些子任务适合放进主上下文？
2. 哪些子任务会产生大量日志、搜索结果、代码读取？
3. 哪些需要交给 Layer 5 做上下文隔离？

所以 Layer 4 是 Layer 5 的输入来源。

失败条件：

1. 没有 gate。
2. 没有产物清单。
3. 没有验证点。
4. 没有 repair path。
5. 硬门槛和优化项混淆。
6. 任务大而散，无法执行。

出现这些问题，不能进入 Layer 5 / Layer 6。

## 6. Layer 5 — Subagents / Context Isolation

中文名：子智能体 / 上下文隔离层

本层核心问题：哪些任务必须隔离到独立上下文？如何定义子智能体的角色、权限、环境和输出契约？

为什么必须有这一层：

Layer 5 不是简单“分工”。它解决的是上下文污染和权限隔离。

很多子任务会产生大量信息：

1. 搜索资料。
2. 阅读源码。
3. 分析日志。
4. 审计技能包。
5. 检查失败原因。
6. 验证产物证据。
7. 对比多个方案。

这些内容如果全部进入主对话，会导致：

1. 主控上下文被噪声填满。
2. Layer 1 的边界被淹没。
3. Layer 4 的计划被长日志冲散。
4. 后面 GPT / Codex 忘记原始约束。

所以 Layer 5 的核心不是“多几个 agent 干活”，而是：

```text
让子任务在独立上下文里完成。
主上下文只接收摘要、结论和证据路径。
```

子智能体必须具备的条件：

1. `name`：名称。
2. `role`：角色。
3. `description`：何时使用。
4. `prompt`：专门系统提示。
5. `input packet`：委托输入包。
6. `allowed tools`：允许工具。
7. `disallowed tools`：禁止工具。
8. `permission mode`：权限模式。
9. `model / effort`：模型和推理强度。
10. `memory`：是否使用记忆。
11. `isolation`：是否需要 worktree 或独立工作区。
12. `source scope`：允许读取的范围。
13. `forbidden scope`：禁止读取的范围。
14. `output contract`：输出契约。
15. `stop condition`：停止条件。

默认权限原则：

1. research / audit / review / verification 类子智能体默认只读。
2. 默认不允许 Edit。
3. 默认不允许 Write。
4. 默认不允许删除。
5. 默认不允许读取 secret。
6. 默认不允许写 `H:\AI\skills`。
7. 默认不允许宣布 final PASS。

只有在 Layer 10 Repair Loop 明确授权后，才可以使用受限的 repair-worker。

子智能体类型矩阵：

| 类型 | 何时使用 | 默认权限 | 是否可写 | 输出 |
| --- | --- | --- | --- | --- |
| researcher | 查资料、读源码、找成熟路径 | Read / Grep / Glob | 否 | 摘要、来源、证据路径 |
| skill-auditor | 审技能包完整性 | Read / Grep / Glob | 否 | 缺口、冲突、建议 |
| code-reviewer | 审代码质量和风险 | Read / Grep / Bash 只读命令 | 否 | 问题列表、证据 |
| verifier | 检查 claims 是否有证据 | Read / Bash 验证命令 | 否 | accepted / rejected 建议 |
| failure-investigator | 分析失败日志 | Read / Grep / Bash 只读诊断 | 否 | root cause、复现证据 |
| repair-worker | Layer 10 授权后最小修复 | Read / Edit / Bash | 是，受限 | before / after、最小修复 |
| evidence-compiler | 汇总证据索引 | Read | 否 | evidence-index、handoff 摘要 |

本层输入：

1. Layer 4 的 gate plan。
2. 子任务清单。
3. 允许路径。
4. 禁止路径。
5. 技能加载结果。
6. 需要隔离的日志 / 搜索 / 审计任务。

本层产物：

1. `subagent-plan.md`
2. `subagent-delegation-packets.md`
3. `subagent-permission-matrix.md`
4. `context-isolation-map.md`
5. `subagent-summary.md`
6. `subagent-evidence-index.md`
7. `orchestrator-receipt-log.md`

本层边界：

Layer 5 不能代替：

1. Layer 6 Execution Plane。
2. Layer 9 Verification Plane。
3. Layer 12 Final Acceptance。

子智能体可以提供局部研究、审计、验证建议，但不能直接宣布最终通过。

与下一层的关系：

Layer 5 把隔离任务处理完以后，只把以下内容交回主控：

1. 摘要。
2. 结论。
3. 风险。
4. 证据路径。
5. 是否支持进入执行。

Layer 6 只能基于这些被主控接收的摘要进入执行。

失败条件：

1. 只写“让子智能体检查一下”，没有角色和权限。
2. 没有独立上下文说明。
3. 没有 input packet。
4. 没有 output contract。
5. 没有 allowed / disallowed tools。
6. 子智能体返回大量原始日志污染主上下文。
7. 子智能体越权写文件。
8. 子智能体宣布 final PASS。
9. 没有 orchestrator receipt log。
10. 没有证据路径。

出现这些问题，Layer 5 = FAIL，不能进入最终验收。

## 7. Layer 6 — Execution Plane

中文名：执行平面

本层核心问题：谁真正执行任务？执行后产物是什么？为什么执行者不能自己验收？

为什么必须有这一层：

Layer 6 是真正干活的地方：

1. 写代码。
2. 改文件。
3. 运行命令。
4. 生成脚本。
5. 生成报告。
6. 生成 artifact。

但是它有一条铁律：

```text
Execution Plane 只能 claim，不能 self-accept。
```

原因很简单：执行者天然会倾向于相信自己的执行结果。如果执行者同时做验收，就容易形成假 PASS。

所以 Layer 6 只能说：

1. 我做了什么。
2. 我改了哪些文件。
3. 我运行了哪些命令。
4. 我生成了哪些证据。
5. 我提出哪些 execution claims。

不能说：

```text
所以最终 PASS。
```

本层输入：

1. Layer 4 gate plan。
2. Layer 5 摘要和证据路径。
3. 授权的执行范围。
4. 禁止事项。

本层产物：

1. `execution-claims.md`
2. `modified-files.md`
3. `command-log.md`
4. `artifact-manifest.md`
5. `implementation-report.md`

本层边界：

Layer 6 不能：

1. 自己验收自己。
2. 跳过 Layer 8 脚本检查。
3. 跳过 Layer 9 独立验证。
4. 声称 final PASS。
5. 把外部 demo 冒充本地成果。

与下一层的关系：

Layer 6 的 claims 会进入：

1. Layer 7 生命周期检查。
2. Layer 8 脚本确定性检查。
3. Layer 9 独立验证。

也就是说，Layer 6 是被检查对象，不是验收官。

失败条件：

1. 没有 execution claims。
2. 没有 command log。
3. 没有 artifact manifest。
4. 没有 modified-files 清单。
5. 执行层自称 final PASS。

这些情况必须回 Layer 6 修复。

## 8. Layer 7 — Hooks / Lifecycle Triggers

中文名：生命周期钩子层

本层核心问题：如何在关键节点提前阻断风险，而不是最后才发现问题？

为什么必须有这一层：

长任务不能只在最后检查。很多错误必须在过程中拦截：

1. 写入禁止目录。
2. 删除不该删的文件。
3. 读取 secret。
4. 跳过证据归档。
5. 工具调用失败却继续。
6. compact 前没有交接摘要。

Layer 7 就是过程中的刹车和触发器。

本层具体工作：

1. 执行前做 preflight check。
2. 写文件前检查 forbidden path。
3. 工具调用后检查是否产出证据。
4. 验证失败时触发 repair。
5. compact 前生成 handoff。
6. stop 前检查 final acceptance 是否存在。

本层产物：

1. `lifecycle-hooks.md`
2. `hook-check-log.md`
3. `blocked-action-log.md`
4. `preflight-check.md`
5. `post-action-check.md`
6. `stop-gate-check.md`

本层边界：

Layer 7 是触发和阻断层，不是最终验证层。它不能替代 Layer 8 / 9 / 12。

与下一层的关系：

Layer 7 触发或要求 Layer 8 运行确定性检查。例如：

1. 写文件后 -> 触发文件存在性检查。
2. 生成 JSON 后 -> 触发 JSON parse 检查。
3. 任务停止前 -> 触发 final acceptance 检查。

失败条件：

1. 没有 preflight。
2. 没有 forbidden path 检查。
3. 工具失败后继续。
4. compact 前没有交接。
5. stop 前没有 final acceptance gate。

出现这些问题，必须回 Layer 7 或相关上游层修正。

## 9. Layer 8 — Scripts / Deterministic Checks

中文名：脚本确定性检查层

本层核心问题：如何让“是否通过”不靠 AI 口头判断，而靠可复验脚本？

为什么必须有这一层：

AI 说“看起来完成了”不可靠。必须有机器可检查的信号：

1. 测试是否通过。
2. 构建是否通过。
3. JSON 是否可解析。
4. 文件是否存在。
5. 字段是否完整。
6. 状态码是否正确。
7. bad-case 是否覆盖。
8. 截图是否符合视觉标准。

Layer 8 的核心是：

```text
AI 说了不算，脚本检查结果才是可复验证据。
```

本层输入：

1. Layer 6 execution claims。
2. artifact manifest。
3. 预设验收字段。
4. bad-case plan。

本层产物：

1. `verify-*.mjs`
2. `verify-*.py`
3. `verification-result.json`
4. `bad-case-test-result.md`
5. `deterministic-check-log.md`
6. `field-check-result.json`

本层边界：

Layer 8 不是独立验收层。它只产生机器检查结果。它不能直接说最终 PASS。它只能说检查结果 PASS / FAIL。

与下一层的关系：

Layer 8 的结果进入 Layer 9。Layer 9 决定是否接受 Layer 6 的 claims。

失败条件：

1. 没有验证脚本。
2. 脚本只检查文件存在，不检查关键字段。
3. 脚本失败但继续。
4. 没有 bad-case。
5. verification-result 不可解析。

这些情况必须修复。

## 10. Layer 9 — Verification Plane

中文名：独立验证平面

本层核心问题：谁独立判断 Execution Plane 的 claims 是否成立？

为什么必须有这一层：

Layer 9 是防止假 PASS 的核心。它和 Layer 6 必须分离：

```text
Layer 6：我做了什么。
Layer 9：我是否接受你做成了。
```

Layer 9 只读产物，不负责写代码，不负责补报告，不负责美化结果。

硬规则：Verification Plane 负责 acceptance / rejection。

本层输入：

1. `execution-claims.md`
2. `artifact-manifest.md`
3. Layer 8 `verification-result`
4. `bad-case-test-result`
5. evidence paths

本层具体工作：

1. 读取 execution claims。
2. 读取脚本检查结果。
3. 对每个 claim 做 accepted / rejected 判断。
4. 标记证据不足的 claim。
5. 生成独立验证结论。

本层产物：

1. `independent-verification.md`
2. `claim-acceptance-matrix.md`
3. `verification-result.json`
4. `accepted-claims.md`
5. `rejected-claims.md`

本层边界：

Layer 9 不能替代 Layer 12。它只能 acceptance / rejection claims。最终 PASS 仍然属于 Layer 12。

与下一层的关系：

如果 Layer 9 有 rejected claims，必须进入 Layer 10 Repair Loop。如果全部关键 claims accepted，才可以进入 Layer 11 / Layer 12。

失败条件：

1. 没有独立验证。
2. 验证平面和执行平面混同。
3. 没有 claim acceptance matrix。
4. rejected claims 被忽略。
5. 脚本失败但验证仍然接受。

这些情况直接 FAIL。

## 11. Layer 10 — Repair Loop

中文名：返修循环层

本层核心问题：验证失败后，如何回到正确层修复，而不是包装成风险继续通过？

为什么必须有这一层：

很多 AI 长任务失败，不是因为没有发现问题，而是因为发现以后：

1. 把问题写成 residual risk。
2. 把失败写成 known limitation。
3. 把未完成写成后续优化。
4. 最后仍然 PASS。

Layer 10 的规则是：

```text
rejected claim 必须返修。
不能包装。
不能跳过。
不能直接 final PASS。
```

本层输入：

1. Layer 9 rejected-claims。
2. failure reason。
3. claim-acceptance-matrix。
4. bad-case result。

本层具体工作：

1. 读取 rejected claims。
2. 判断失败属于哪一层：
   - 目标问题 -> 回 Layer 1。
   - 入口问题 -> 回 Layer 2。
   - 技能问题 -> 回 Layer 3。
   - 规划问题 -> 回 Layer 4。
   - 隔离问题 -> 回 Layer 5。
   - 执行问题 -> 回 Layer 6。
   - 钩子问题 -> 回 Layer 7。
   - 脚本问题 -> 回 Layer 8。
   - 验证标准问题 -> 回 Layer 9。
3. 执行最小修复。
4. 记录 before / after。
5. 重新跑 Layer 8 / Layer 9。

本层产物：

1. `repair-loop-log.md`
2. `rejection-to-repair-map.md`
3. `before-after-evidence.md`
4. `rerun-verification-result.json`

本层边界：

Layer 10 不能为了通过而降低标准。它只能修问题，不能改验收线来迎合结果。

与下一层的关系：

只有 repair 后重新通过 Layer 8 / 9，才可以进入 Layer 11。

失败条件：

1. rejected claims 没处理。
2. 把失败包装成 residual risk。
3. 没有 before / after。
4. 没有 rerun verification。
5. 为了 PASS 降低标准。

出现这些，不能 final PASS。

## 12. Layer 11 — Compact / Handoff

中文名：压缩交接层

本层核心问题：长任务阶段结束后，如何让下一轮接得上，又不把上下文塞爆？

为什么必须有这一层：

长任务一定会产生大量材料：

1. 日志。
2. 报告。
3. 脚本输出。
4. 截图。
5. 路径。
6. 失败记录。
7. 修复记录。
8. 验证记录。

如果不压缩交接，下一轮 GPT / Codex 会面对一堆文件路径，无法判断：

1. 哪个是最终结论？
2. 哪个是旧失败？
3. 哪个是最新证据？
4. 下一步从哪里开始？

Layer 11 的作用是：

```text
把阶段成果压缩成短摘要 + 证据索引。
```

本层输入：

1. accepted claims。
2. verification-result。
3. repair-loop-log。
4. artifact-manifest。
5. final candidate evidence。

本层产物：

1. `compact-handoff.md`
2. `handoff-summary.md`
3. `artifact-index.md`
4. `evidence-index.md`
5. `next-step.md`

本层边界：

Layer 11 不是最终验收。它只是交接整理。不能用 handoff 代替 final acceptance。

与下一层的关系：

Layer 11 把被验证接受的结果整理给 Layer 12，Layer 12 才能最终判断 PASS / PARTIAL / BLOCKED。

失败条件：

1. 没有 handoff。
2. 没有 evidence index。
3. 新旧结果混在一起。
4. 下一步不清楚。
5. 只给文件夹路径。

这些情况会导致下一轮无法准确继续。

## 13. Layer 12 — Final Acceptance

中文名：最终验收层

本层核心问题：谁最终盖章？什么条件下才允许最终 PASS？

为什么必须有这一层：

很多任务会把以下内容误认为最终验收：

1. `final-report.md`
2. execution summary
3. verification-result
4. 文件夹路径
5. “我已经完成”

这些都不是最终验收。

Final Acceptance 必须明确：

1. `final_pass = true / false`
2. 哪些硬门槛通过。
3. 哪些 claims 被接受。
4. 哪些证据支持。
5. 是否还有 blocker。
6. 最终状态码是什么。

本层输入：

1. Layer 9 accepted claims。
2. Layer 10 repair result。
3. Layer 11 handoff。
4. artifact manifest。
5. verification-result。
6. hard gate checklist。

本层产物：

1. `final-acceptance.md`
2. `final-acceptance.json`
3. `final-report.md`
4. `final-status-code.txt`

本层边界：

Layer 12 是最终通过权。没有它，不能 PASS。

硬规则：

1. 没有 `final-acceptance.md`，没有 final PASS。
2. 没有 `final-acceptance.json`，没有 final PASS。
3. `final-report` 不是 final-acceptance。
4. Execution claim 不是 final-acceptance。

失败条件：

1. 没有 `final-acceptance.md`。
2. 没有 `final-acceptance.json`。
3. `final_acceptance.json` 不可解析。
4. `final_pass` 不是 true 却声称 PASS。
5. 硬门槛未全部通过。
6. 仍有 blocker。

出现这些，最终状态只能是 PARTIAL / BLOCKED / FAIL，不能 PASS。

## 14. 12 层之间的因果关系

这 12 层的逻辑不是并列清单，而是因果链：

```text
Layer 1 不清楚 -> Layer 2 不知道读什么。
Layer 2 不干净 -> Layer 3 会加载错技能。
Layer 3 错了 -> Layer 4 会拆错任务。
Layer 4 不完整 -> Layer 5 不知道隔离什么。
Layer 5 不隔离 -> Layer 6 执行时上下文被污染。
Layer 6 只执行 -> 必须由 Layer 7-9 检查和验证。
Layer 7 缺失 -> 危险动作不会被过程阻断。
Layer 8 缺失 -> 没有机器可复验证据。
Layer 9 缺失 -> 执行者自己验收自己。
Layer 10 缺失 -> 失败会被包装成风险继续通过。
Layer 11 缺失 -> 长任务下一轮无法接续。
Layer 12 缺失 -> 没有最终通过权。
```

所以，任何任务包都必须显式包含 12 层。不能只在开头说一句“遵守 12 层”，然后正文里看不见 12 层。

## 15. 在 GPT-Codex 闭环中的正确应用

当前推荐流程是：

```text
用户把任务发布到 Codex 桌面端
→ Codex 收集任务、技能包、环境信息
→ Codex 把这些发给 GPT
→ GPT 按 Claude-style 12 Layer 原顺序生成完整可执行命令包
→ Codex 桌面端执行命令包
→ Codex 收集每层证据
→ Codex 把执行回传包发给 GPT
→ GPT 基于 Layer 9 和 Layer 12 做最终验收
→ Codex 按 GPT 的验收结论归档、修复或停止
```

这里的分工是：

1. 用户：发布任务，看最终结论。
2. GPT：制定 12 Layer 命令包，做最终验收。
3. Codex 桌面端：操作电脑、执行命令、收集证据、回传给 GPT。

关键边界：

1. Codex 可以执行，但不能自己 final PASS。
2. GPT 可以验收，但必须基于 Codex 回传的证据。
3. 用户不需要逐个文件判断，但用户保留最终业务决定权。

## 16. 任务包必须强制包含的格式

以后 GPT 生成任务包时，每一层必须按以下格式写：

```text
Layer X — 原始英文名
中文名：

本层目的：
本层输入：
本层动作：
本层产物：
本层验证：
失败返回：
证据路径：
是否允许跳过：
本任务中的具体应用：
```

如果某一层本任务不启用，也必须写：

```text
本任务不启用本层的某项机制，原因：
1.
2.
3.

替代保障：
1.
2.
3.

Verification Plane 是否接受 no-op / exception：
YES / NO
```

不能空着。

## 17. 一票否决规则

出现以下任意情况，任务包或执行结果直接 FAIL：

1. 把 12 Layer 改成普通 12 步。
2. 改名、压缩、重解释 12 层。
3. 只写英文层名，不写中文作用。
4. 没有写层与层的连接关系。
5. Layer 5 没有独立上下文、角色、权限、输出契约。
6. Execution Plane 自己宣布 final PASS。
7. Verification Plane 缺失。
8. Repair Loop 缺失。
9. Final Acceptance 缺失。
10. 只返回文件夹路径。
11. 没有 `final-acceptance.md`。
12. 没有 `final-acceptance.json`。

## 18. 最终一句话

Claude-style 12 Layer 的真正核心是：

```text
用 12 个控制层，把 AI 长任务从“模型觉得完成”变成“有边界、有证据、有验证、有返修、有最终验收”的工程闭环。
```

它不是为了复杂而复杂，而是为了保证长任务不跑偏、不污染、不假 PASS、不失控。

这版的重点是把每一层的作用、输入、产物、边界、失败条件、前后关系都写出来。后续让 Codex 更新技能包时，可以把这版作为 `CLAUDE-STYLE-12-LAYER-DETAILED-CHINESE-GUIDE.md` 的主体内容。
