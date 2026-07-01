# Loop Prompt Patterns

Source material: `C:\Users\A\.codex\manual-paste-attachments\codex-pasted-text-20260613-201102-c54ee1f3.txt`

## Core Difference

普通提示词追求一次生成结果。Loop 提示词要求先定义标准，再生成第一版，再按标准检查、评分、修复、复查，直到达标或诚实停止。

Core formula:

```text
目标定方向
样品定气质
标准定好坏
第一版打底
评分找差距
修复逼近目标
复查防自嗨
停止防乱跑
沉淀变技能
```

## Universal Loop Prompt Skeleton

Use this for complex tasks that should not end at the first draft.

```text
# 通用复杂 Loop 提示词模板

任务目标：
【填写你要完成什么】

任务性质：
这不是一次性生成任务，而是 loop 成熟化任务。
你不能第一版就结束，必须按标准一轮一轮检查和修复。

## 1. 先理解目标

请先说明：
1. 这个任务真正要解决什么问题；
2. 最终结果应该长什么样；
3. 它不应该变成什么；
4. 成功标准是什么；
5. 风险是什么。

## 2. 制定检查标准

请根据目标制定检查标准。

要求：
1. 每项标准必须可判断；
2. 每项标准必须能打分；
3. 不要写空泛标准；
4. 标准必须和最终用途相关。

## 3. 生成第一版

请按目标和标准生成第一版。
第一版不要求完美，但必须结构完整。

## 4. 自查第一版

请按检查标准逐项评分，0-10 分。

要求：
1. 低于 8 分必须说明问题；
2. 不得只写优点；
3. 必须指出具体缺陷；
4. 必须提出修复动作。

## 5. 修复第二版

请根据自查结果修复第二版。

要求：
1. 只针对问题修；
2. 不要乱改；
3. 保留第一版中好的部分；
4. 说明修改原因。

## 6. 再次自查

请再次评分。
如果仍有低于 8 分的项目，继续修复。
最多修复 3 轮。

## 7. 停止条件

满足以下条件才能输出最终版：
1. 核心标准全部 8 分以上；
2. 没有违反禁止项；
3. 结果符合最终用途；
4. 有明确验收记录；
5. 有可复用经验。

如果达不到，输出 PARTIAL 或 BLOCKED，不得假装完成。

## 8. 最终输出

最终输出：
1. 最终版；
2. 检查标准；
3. 各轮评分；
4. 修复记录；
5. 未解决问题；
6. 下次可复用模板。
```

## Pattern Catalog

Use these routes to adapt the universal skeleton.

| Scenario | Loop Focus | Required Evidence |
| --- | --- | --- |
| AI Company Knowledge OS dashboard | 样品分析 -> 成熟标准 -> 项目映射 -> 设计版本 -> 评分修复 | 样品分析报告、标准映射表、评分记录、修复记录、Codex 实现要点 |
| 8-hour Codex long task | 时间线 -> 阶段闸门 -> 阶段记录 -> 最终验收 | `STAGE_XX_REPORT.md`、`FINAL_ACCEPTANCE_REPORT.md`、文件清单、风险清单 |
| Video/tutorial to skill package | 内容理解 -> 用户适配 -> 方法拆解 -> 技能包结构 -> 最小实验 | 核心理解报告、方法拆解表、技能包草案、实验设计、Gate Review 检查表 |
| DeepSeek low-cost exploration | 多候选生成 -> 自评分 -> 淘汰 -> 融合 -> Gate Review | 5 个候选方案、评分表、淘汰理由、主方案、备选方案 |
| Image/video work | 原图分析 -> 目标定义 -> 第一版 -> 对比检查 -> 修复版 | 原图特征、保留项、禁止项、对比表、成熟版提示词 |
| Obsidian archive | 读取 -> 分类标准 -> 第一轮归档 -> 自查 -> 修复 -> 知识地图 | 归档报告、标签表、关系表、重复项、待处理清单、知识地图 |
| Software/page repair | 复现 -> 最小修复计划 -> 第一轮修复 -> 自测 -> 回归检查 | 复现报告、修改清单、测试结果、风险、回滚建议 |
| One-person AI company planning | 资源分析 -> 多路线 -> 评分 -> 淘汰 -> 融合 -> 30 天计划 | 资源分析、路线评分、淘汰表、主路线、每周检查表 |
| Skill-package rule integration | 允许/禁止边界 -> 目标技能包备份 -> 规则文件 -> 模板 -> 索引更新 -> 证据/manifest -> 验证/同步 | 备份路径、规则文件、模板文件、SKILL.md 更新说明、manifest、验证结果、未触碰禁区声明 |
| Loop Engineering video standard | 可观测目标 -> 小步执行 -> 外部验证器/Harness -> 决策 -> 继续/停止/回滚/人审 | 验证器清单、决策矩阵、真实信号、成本边界、不能 PASS 的条件 |

## Non-Negotiables

- Do not produce the final answer before defining acceptance criteria.
- Do not hide low scores; anything below 8 must become a repair item.
- Do not continue into the next stage when key acceptance criteria fail.
- Do not mark `PASS` without evidence.
- Use `PARTIAL` for usable but incomplete results.
- Use `BLOCKED` when key requirements still fail after 3 repair rounds or required access/input is missing.

## Trigger Keywords

Use this reference when the user mentions:

```text
Loop 提示词
成熟化 loop
样品驱动
第一版
评分
低于 8 分
修复第二版
最多 3 轮
停止条件
阶段闸门
证据回传
沉淀成技能
```

## Reuse Instruction

When a future task asks for a prompt, plan, dashboard, repair, archive, or skill conversion and quality matters, first decide whether it needs a Loop prompt. If yes, adapt the universal skeleton and the closest pattern from this file instead of inventing a one-off prompt.

For a concrete command-package example of integrating Loop rules into `obsidian-ai-company-os`, read `case-ai-company-os-loop-rule-integration.md`.

For validation-driven Loop Engineering rules from the video contact sheet and command package, read `case-loop-engineering-video-standard.md`.
