---
name: task-selection-priority-engine
description: 任务选择排序引擎 v0.2.0。运行链之外的项目准入、继续性复审与项目组合优先级治理工具；不进入具体任务 Runtime，不污染 RUNTIME_T_VALID。
metadata:
  version: "0.2.0"
  display_name: "任务选择排序引擎"
---

# 任务选择排序引擎 v0.2.0
Task Selection & Priority Engine v0.2.0

## 1. 架构定位

本技能不是“整体闭环极限短时间引擎”的运行时前置节点。

它位于具体任务执行链之外，只负责：
1. ADMISSION（项目准入）：这个候选任务是否值得正式立项；
2. CONTINUATION REVIEW（继续性复审）：出现重大新事实后是否继续、暂停、改用现成方案或终止；
3. PORTFOLIO PRIORITY（项目组合优先级）：多个已通过准入的项目当前先做哪个。

一旦项目已准入并进入正式 Runtime，普通循环、重试、Reality Delta、Virtual→Real 均不得重新经过本技能。

## 2. 触发条件

允许调用：
- 新候选任务/项目首次立项；
- 重大范围、价值、投入、资源或架构变化导致原立项依据失效；
- 人工要求重新排序或复审；
- 自治调度器从尚未启动的候选池选择下一项目。

禁止因以下情况重复调用：
- 普通执行失败；
- 普通重试；
- Reality Delta；
- 任务内部循环；
- 已批准任务的常规节点切换。

## 3. 决策顺序

先硬准入，后排序：

1. FALSIFICATION / REVERSE ATTACK：最强反方、致命约束；
2. STRATEGIC FIT：整体目标一致性；
3. ARCHITECTURE FIT：整体自动化架构一致性；
4. EXISTING SOLUTION SUBSTITUTE：成熟现成方案是否足以替代自建；
5. CONFIDENCE / MINIMUM KILL TEST：证据不足时是否值得做最低成本 Kill Test；
6. VALUE / TOTAL BURDEN：置信度修正后的整体价值是否覆盖总投入；
7. 只有通过准入的项目进入 Portfolio Priority。

输出：
- KILL
- USE_EXISTING
- PILOT
- ADMIT

## 4. 排序原则

排序只对 ADMIT / CONTINUE 项目生效。

核心顺序：
- 关键依赖优先；
- 再按置信度修正后的整体价值密度 × 紧迫性 / 总负担；
- 同分时总负担更低者优先；
- 再同分按进入候选池顺序稳定排序。

“有用”不等于“值得单独立项”；违反整体架构的候选在排序前直接淘汰。

## 5. 审计时间

每次决策必须保存：
- DECISION_TIMESTAMP（决策时间）
- EVIDENCE_AS_OF（证据截止时间）
- SCOPE_HASH（范围哈希）
- REASON_CODE（决策原因）
- ADMISSION / CONTINUATION / PRIORITY

失败复盘必须按“当时可获得的证据”审查，禁止用事后信息倒推当时决策必然错误。

## 6. 时间原则

本技能自身优化仍只认：
`T* = min(T_VALID)`

冻结测功任务：
`TSPE-1000-STRUCTURED-E2E-01`

T_VALID 包含：
- 1000 个结构化候选进入冻结接口；
- schema 验证；
- 准入与继续性决策；
- 项目组合排序；
- 决策/证据时间写入；
- SHA-256 范围凭证；
- 独立结果验证。

但本技能的 T_VALID 与被准入项目的运行时间完全隔离：

`TSPE_T_VALID ∉ PROJECT_RUNTIME_T_VALID`

`TSPE_T_VALID ∉ PROJECT_T_STAR`

## 7. v0.2.0 冻结结果

FREEZE_ID=`TSPE-v0.2.0-E-INLINE-ONEPASS`

VIRTUAL_MATURITY=PASS
SEMANTIC_EQUIVALENCE_10000=PASS
GPT_REAL_PRECHECK=PASS
USER_WINDOWS_CODEX_REALITY_CERTIFICATION=PENDING

虚拟成熟当前锚：
`VIRTUAL_T_VALID_STAR_MS=6.414963`

GPT 执行宿主冻结验证器预跑：
- 30/30 VALID
- MIN=6.448333 ms
- P50=7.051018 ms
- P95=9.680503 ms
- MAX=10.030460 ms

完整冻结包：
`skills/task-selection-priority-engine/frozen/TSPE-v0.2.0.zip`

ZIP SHA-256：
`dbf26948390bd64f723c75843593a5410e0f9fd4d9c1b526a1d9cce9c47f27b9`

## 8. 现实阶段纪律

最终 Windows/Codex Reality Certification（现实认证）只允许执行冻结验证器，不允许现场重新设计、补规则或调参。

REAL FAIL：
`minimal Reality Delta -> STOP -> return to Virtual`

现实阶段不得把本技能插入被评估项目的 Runtime 节点链。

