---
name: yesterday-replay-controlled-coding
description: "Use first when starting a substantial Codex task. CODEX_FIRST_YESTERDAY_REPLAY_MULTI_MODEL_90_GATE_V2.2: Codex接任务 → 简单直接做 → 复杂任务进入昨日重现 → 查本地成熟方案+网络成熟方案+官方文档+成熟组件细节 → 本地适配执行方案 → 多模型低成本极限回答技能包审核 → ≥90分才执行 → 证据验收 → ZIP交付。"
version: 2.2.0
---

# Yesterday Replay Controlled Coding

## Purpose

This skill is the first, lightweight routing gate for the user's workflow. It
must classify the task before any other skill, browser path, shell workflow, GPT
planning route, or implementation process is selected.

Keep this file cheap to load. Do not read the detailed workflow reference unless
the classification below says it is needed.

## Canonical Flow Name

```text
CODEX_FIRST_YESTERDAY_REPLAY_MULTI_MODEL_90_GATE_V2.2
```

## Initial Task Read Gate (初始任务必读门禁)

This skill must be read at the start of a new user task when the task is
substantial enough to need routing, planning, code changes, installation,
automation, repair, multi-step verification, browser operation, document
production, packaging, or long-running execution.

Do not repeatedly reload this skill for every message inside the same active
task. Mid-task user additions, corrections, clarifications, or problem reports
should be absorbed into the current route unless they clearly start a separate
new complex task.

Load discipline:

- New complex task from the user: read this skill first, then classify.
- Simple one-off request: answer directly or run the smallest useful check.
- Mid-task supplement or correction: continue the active route; do not restart
  the skill loading ceremony.
- New task after the prior task is complete: read this skill again if the new
  task is complex.
- Heavy references such as `references/controlled-workflow.md` are loaded only
  after G00 classification says the task is Complex.

## 完整工作流总览

```
Codex接到任务
  │
  ├─ G00 轻量分类
  │   ├─ Simple → 直接做 → 完成
  │   ├─ Complex → 进入昨日重现流程 ↓
  │   └─ Stop Gate → 停下来问用户
  │
  ├─ 昨日重现（搜索本地 + 网络成熟方案）
  │   ├─ 本地历史成功方案 / 本地技能包 / 旧命令包 / 旧报告
  │   ├─ 官方文档 / GitHub开源项目 / 成熟教程 / 社区验证方案
  │   ├─ 同类工具最佳实践 / 可复用组件细节
  │   └─ 组合成：本地执行方案 + 路径/依赖/权限/测试/回滚/验收适配
  │
  ├─ 多模型低成本极限回答技能包审核闭环
  │   ├─ 低成本模型先筛 → 强模型补充判断 → GLM-5.2等高价值模型参与
  │   ├─ 输出评分、风险、失败概率、改进建议
  │   ├─ ≥90分 → 正式执行
  │   └─ <90分 → Loop回修订 → 再提交审核 → 直到≥90分
  │
  ├─ 执行 + 证据验收
  │   └─ 产出PASS/FAIL证据
  │
  └─ ZIP交付
      └─ 三位数字ZIP打包到桌面
```

## G00 Lightweight Classification

Classify the request into exactly one route:

| Route | Use when | Action |
| --- | --- | --- |
| Simple | The task is deterministic, low-risk, one-step, or answerable from current context with no meaningful route judgment. | Do it directly. Do not load the detailed workflow reference. Use the narrowest meaningful check if a check is useful. |
| Complex | The task involves coding, debugging, configuration, installation, automation, repair, multi-step analysis, route judgment, external/current facts, browser work, documents, or non-trivial verification. | Load `references/controlled-workflow.md`, then run yesterday replay across local history, skills, old reports/commands, official docs, GitHub/open-source projects, mature tutorials, community-verified solutions, and reusable component details. Produce a local-adapted execution plan before review. |
| Stop Gate | The task may delete data, batch-modify broad areas, change system/account/payment/security state, expose secrets, run unknown high-impact commands, or has an explicit safety blocker. | Stop before execution and ask the user for the narrowest missing decision or permission. |

## Simple Route

For simple requests:

- Answer or run the minimal read-only/local command directly.
- Do not invoke GPT web planning.
- Do not load heavy reference files or extra process skills unless the request
  itself names them.
- Preserve normal safety boundaries.
- If claiming a local fact, use a narrow check when cheap.

Examples: explain a concept, answer a short question from already-loaded
context, list a directory, check whether a file exists, run an explicit harmless
command, or inspect one small file.

## Complex Route

Before complex execution, read:

```text
C:\Users\A\.codex\skills\yesterday-replay-controlled-coding\references\controlled-workflow.md
```

Then follow the detailed rules there for:

- risk levels and Level 0-3 execution
- backup, diff, logs, and verification discipline
- Superpowers-style planning, debugging, TDD, and completion checks
- yesterday-replay mature-path reuse from local and network sources
- local adaptation for paths, dependencies, permissions, tests, rollback, and acceptance
- 多模型低成本极限回答技能包审核闭环 (score gate ≥90)
- ChatGPT screenshot bridge boundaries
- evidence verification and ZIP delivery

GPT web planning is optional, not mandatory. Use it only when it materially helps
and the allowed screenshot bridge route is available. If a local skill,
official doc, browser/accessibility path, or test path is sufficient, use that
instead.

## Yesterday Replay Scope (本地 + 网络成熟方案)

Yesterday replay is not local-only. Its job is to find mature, already-tested
paths before Codex invents anything.

Search sources:

```text
本地历史成功方案
本地技能包
旧命令包
旧报告
官方文档
GitHub/开源项目
成熟教程
社区验证方案
同类工具最佳实践
可复用组件细节
```

Codex must not copy these blindly. It must combine and adapt them into:

```text
本地执行方案
本地路径适配
依赖适配
权限适配
测试适配
回滚适配
验收适配
```

## Score Gate (≥90分门槛)

复杂任务方案在执行前必须进入「多模型低成本极限回答」技能包审核。
GLM-5.2 只是审核系统中的高价值判断模型之一，不是唯一裁判。

审核流程：

```text
本地执行方案
→ 进入「多模型低成本极限回答」技能包
→ 多个模型分层审核
→ 低成本模型先筛
→ 强模型补充判断
→ GLM-5.2 作为其中一个高价值判断模型参与
→ 汇总评分、风险、失败概率、改进建议
→ ≥90 分才执行
```

| 分数段 | 结论 | 动作 |
|--------|------|------|
| ≥90 | 通过 | 正式执行 |
| 80-89 | 接近但不足 | Loop回修改，重点补缺项 |
| 70-79 | 明显不足 | Loop回大改 |
| <70 | 方案不可用 | 推翻重来或回到昨日重现重新找方案 |

打分维度（每项0-100，总分=加权平均）：

| 维度 | 权重 | 评估内容 |
|------|------|---------|
| 方案完整性 | 25% | 目标/范围/步骤/验证/停止条件/完成标准是否齐全 |
| 成熟度 | 20% | 是否复用了已验证的成熟方案，而非从零开始 |
| 本地适配性 | 20% | 方案是否已适配本地环境（路径/依赖/权限/编码） |
| 风险控制 | 20% | 备份/回滚/日志/验证是否到位 |
| 证据可验收 | 15% | 产出是否有明确的PASS/FAIL判据 |

**Codex负责总入口、本地执行、本地适配、证据验收。**
**多模型低成本极限回答技能包负责统一审核。**
审核不通过 → Loop循环修订 → 再提交 → 直到≥90分才执行。

## Model Role Positioning

| 角色 | 定位 |
| --- | --- |
| Codex | 总入口、本地执行、本地适配、证据验收 |
| 昨日重现 | 查找本地和网络成熟方案，不重新造轮子 |
| GPT | 复杂规划/修订/外援思考，不是入口 |
| 多模型低成本极限回答技能包 | 统一审核系统 |
| GLM-5.2 | 审核系统中的高价值模型之一 |
| DeepSeek/GPT/其他模型 | 审核系统中的其他对照模型 |
| 90分 Gate | 是否允许执行的最终门槛 |

## ZIP Delivery (三位数字ZIP交付)

复杂任务完成后，必须打包交付：

```text
1. 扫描桌面已有 NNN.zip（001-999）
2. 选择未使用的最小三位数字
3. 打包内容：更新后的技能/代码 + 报告 + 备份说明 + 变更清单
4. ZIP命名：NNN.zip（如 003.zip）
5. 不得覆盖已有ZIP
```

ZIP内至少包含：

```text
updated_skill/ 或 updated_code/
TASK_REPORT.md
backup_path.txt
changed_files_manifest.txt
```

## On-Demand Skill References (按需调用技能包)

以下技能包**不合并进本文件**，仅在需要时按流程调用。保持本技能包轻量。

### 1. 连接GPT/DeepSeek智能体时 → 调用「AI自执行坐标知识系统」

当需要通过浏览器连接GPT网页版或DeepSeek网页版（发送提示词、获取回答、复制结果）时，
调用此技能包进行坐标法操作。

```text
技能包路径: C:\Users\A\.hermes\skills\productivity\one-step-one-screenshot
技能包名称: AI自执行坐标知识系统 (one-step-one-screenshot v3.0)
```

调用流程：

```text
1. 从 coordinate_knowledge/coordinate_registry.jsonl 加载目标网站的已验证坐标
2. 从 coordinate_knowledge/screen_profiles.json 加载对应的 screen_profile
3. 验证 State Contract（分辨率/缩放/窗口状态/页面状态是否匹配）
4. 匹配 → 直接按坐标执行（click input → paste → click send → wait → click copy）
5. 不匹配 → 进入截图标定流程（一步一截图法 fallback）
6. 执行后运行 coordinate_update_finalizer（成功/失败都沉淀到知识库）
```

**何时调用**：多模型审核需要发送方案给GPT网页、需要从GPT/DeepSeek获取回答时。
**何时不调用**：本地能解决的任务（文件操作、脚本执行、终端命令）不需要连接网页智能体。

### 2. 审核本地执行方案时 → 调用「多模型低成本极限回答技能包」

当复杂任务已经形成本地执行方案，需要统一审核、交叉验证、评分、风险识别、
失败概率判断和改进建议时，调用多模型低成本极限回答技能包。该技能包是统一审核
系统；GLM-5.2 只是其中一个高价值判断模型节点，不是唯一审核者。

```text
技能包路径: C:\Users\A\.codex\skills\ultrafusion-low-cost-multi-model-extreme-fusion
技能包定位: 多模型低成本极限回答 / 极限融合 / 统一审核系统
模型阵容:   由技能包按低成本分层策略调度；GLM-5.2 只是高价值模型之一
```

调用流程：

```text
1. 读取本地执行方案
2. 进入多模型低成本极限回答技能包
3. 低成本模型先筛
4. 强模型补充判断
5. GLM-5.2 作为其中一个高价值判断模型参与
6. 汇总评分、风险、失败概率、改进建议
7. 评分结果反馈到 Score Gate 的打分维度中
```

**何时调用**：复杂任务本地执行方案进入Score Gate审核时。
**何时不调用**：简单任务、低风险任务、单一模型回答已足够时。

**注意**：不要把审核写成“GLM-5.2审核”。GLM-5.2 是审核系统中的高价值模型之一，
不是唯一裁判。

### 调用关系图

```
yesterday-replay-controlled-coding (本技能包，路由+执行框架)
  │
  ├─ 需要连接GPT/DeepSeek网页？
  │   └─ 调用 → AI自执行坐标知识系统 (坐标法操作浏览器)
  │
  ├─ 本地执行方案需要审核？
  │   └─ 调用 → 多模型低成本极限回答技能包 (分层审核+评分+风险+失败概率+改进建议)
  │
  └─ 两者关系：
      坐标知识系统负责"怎么连"（传输层）
      多模型低成本极限回答技能包负责"如何审核"（质量层）
      本技能包负责"什么时候连、连了怎么用"（编排层）
```

## Browser And Screenshot Routing

- For ChatGPT web send/copy planning, use `chatgpt-screenshot-bridge` only when
  the detailed workflow permits it and the visible page is safe. The current
  accepted implementation is
  `C:\Users\A\.codex\skills\chatgpt-screenshot-bridge`, with full-window
  screenshot state classification, browser visual fallback, stop-button
  disappearance wait, small-crop copy-button targeting, and sentinel clipboard
  verification.
- For ordinary browser work that depends on visible pixels, use
  `screenshot-recognize-operate-browser` after this router classifies the task.
- Do not use real Windows mouse or keyboard input outside the narrow
  pre-authorized ChatGPT text-only bridge unless the user explicitly allows it
  for that task.

## Reporting

For complex work, report:

- route classification
- score gate result (score + dimensions)
- files changed
- commands/checks run
- PASS/FAIL evidence
- ZIP delivery path
- skipped checks and residual risk

For simple work, keep the response short and do not include process ceremony
unless the user asks for it.
