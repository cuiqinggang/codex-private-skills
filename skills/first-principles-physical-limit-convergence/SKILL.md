---
name: first-principles-physical-limit-convergence
description: 极限短时间引擎 v4.7.0。双时间单闭环：T_MATURE* 衡量成熟方案必要极限有效时间，T_CLOSED_REAL 衡量从用户一次提交到 FINAL_VALID 的真实墙钟交付时间；方法仍严格只有“虚/实”两步。
metadata:
  version: "4.7.0"
  display_name: "极限短时间引擎"
---

# 极限短时间引擎 v4.7.0

## 1. 方法结构仍然只有一虚一实

方法步骤严格只有：VIRTUAL（虚）和 REAL（实）。
唯一状态转换：VIRTUAL -> REAL；REAL PASS -> FINAL；REAL FAIL -> VIRTUAL。
自动化、计时、浏览器、Codex、Reality Delta、GitHub 都只是这两步的执行基础设施或观测，不创建第三步骤。

## 2. 双时间，单闭环

同一个任务闭环只保留两个核心时间：

T_MATURE* = 在完整有效约束下，成熟方案真正需要的最短有效智能体工作时间。
T_CLOSED_REAL = 从用户首次提交任务到 GPT 确认 FINAL_VALID=PASS 的真实墙钟时间。

两个时间共享同一个任务边界与 FINAL_VALID，不是两套任务。
不再创建第三个并列核心时间。

当前成熟锚：T_MATURE*=00:03:14.419，来源于 v4.6.0 clean run ESTE-20260923-003。
历史 v4.5.x >=00:51:07.109 只属于开发/返工活跃成本样本，不是 T_MATURE*，也不是 T_CLOSED_REAL。
用户报告今晚现实经历跨越数小时；由于旧流程没有全程墙钟自动打点，只记录为 HISTORICAL_CLOSED_REAL_USER_REPORTED=SEVERAL_HOURS，禁止伪造精确数值。

## 3. T_CLOSED_REAL 必须完整保留墙钟事实

T_CLOSED_REAL_START = 用户首次提交任务的现实时间戳。
T_CLOSED_REAL_END = GPT 最终确认 FINAL_VALID=PASS 的现实时间戳。
T_CLOSED_REAL = END - START。
墙钟不因失败、回虚、用户离开、系统等待或外部暂停而重置。

## 4. T_CLOSED_REAL 只做归因分解，不产生新锚

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

## 5. 唯一任务完成条件

TASK_COMPLETED=TRUE
CLOSED_LOOP=TRUE
VALID_REAL=PASS
GPT_FINAL_VALID=YES

只有以上全部成立，T_MATURE 和 T_CLOSED_REAL 才允许收口。

## 6. v4.7.0 第一优先级：消灭人在中间的编排延迟

当前最大 GAP 已从模型/工具运行时间转移到 Human-in-the-loop orchestration latency（人在闭环中的编排延迟）。
v4.7.0 优先优化：READ、UNDERSTAND、COPY、PASTE、ROUTE、CONFIRM、人工结果回传和中间等待。
不优先继续把 3分14秒内部时间抠几秒，除非闭环墙钟已接近 T_MATURE*。

## 7. 目标自动闭环

用户只提交一次初始任务。
GPT 自动虚拟成熟并冻结。
自动发送给 Codex。
Codex 自动现实执行并回传证据。
GPT 自动判断 PASS 或 Reality Delta。
若 FAIL：自动 STOP -> 回虚 -> 重新成熟 -> 再冻结 -> 再执行。
只有 FINAL_VALID=PASS 或确实需要用户决策时才通知用户。

## 8. 自动闭环硬门

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
FINAL_VALID=PASS
CLOSED_LOOP_AUTONOMOUS=PASS

## 9. 自动化工程优先级

P0 = v4.7.0 双时间单闭环合同现实实现。
P1 = GPT <-> Codex 自动闭环兼容性/回归认证。
P2 = Playwright 原生 AI 浏览器在 v4.7.0 下兼容性/回归认证。
P3 = GPT <-> Browser <-> Codex <-> GPT 无人值守多轮闭环。
P4 = 故意注入一个可恢复 Reality Delta，验证自动回虚、再冻结、再执行。
P5 = 比较同一个 T_CLOSED_REAL 在人工模式和自动模式下的现实结果。

## 10. V47-AUTOMATION-CLOSED-LOOP-01

这是 v4.7.0 第一现实验收任务。
要求用户只输入一次任务；GPT 自动成熟；自动交 Codex；Codex 自动执行并回传；GPT 自动验证；注入一个可恢复 Reality Delta；系统自动第二次冻结和执行；Verifier PASS 后才通知用户。

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
SECOND_EXECUTION=AUTO
FINAL_VALID=PASS

## 11. Playwright / Codex 不是从零研发

本轮默认采用回归认证思路：已有成熟 GPT-Codex 执行闭环和 Playwright 原生 AI 浏览器资产先作为成熟方案候选；v4.7.0 只验证它们在当前双时间单闭环合同下是否兼容、连续、无人值守。
如果旧资产与当前现实不兼容，记录最小 Reality Delta 后回虚，不重做整套架构。

## 12. 交付指标

每次 v4.7.0 自动化实验至少输出：
T_MATURE_STAR
T_CLOSED_REAL
T_CLOSED_REAL_MODE=MANUAL|AUTOMATED
AUTOMATION_SAVED_TIME
AUTOMATION_REDUCTION_PERCENT
MANUAL_MIDDLE_INTERVENTIONS
CLOSED_LOOP_AUTONOMOUS
FINAL_VALID

人工/自动只是同一个 T_CLOSED_REAL 的实验条件，不是新增核心时间。

## 13. Reality Foundation 与已知错误门

Reality Foundation=local-ai-reality-foundation@1.1.3。
已知 Temp/AppData staging、Here-String 插值、w32tm 权限、FETCH_HEAD 权限、只读探针假阴性、四定位序号、发布时间等已吸收限制必须继续前置拦截。
已知同类原因再次进入 REAL，分类为 GATE_REGRESSION。

## 14. GitHub / Browser / Codex 的角色

GPT=推理与最终裁决。
Codex=现实执行器。
Playwright Native AI Browser=浏览器通信/网页执行桥。
GitHub=共同事实源和结果持久化，不默认作为 REAL 启动硬依赖。

## 15. 当前冻结结论

v4.6.0 已得到精确 clean T_MATURE*=00:03:14.419。
v4.7.0 的首要目标不是立即降低这个 3:14，而是把 T_CLOSED_REAL 从小时级现实体验压向分钟级，并最终逼近 T_MATURE*。

一句话：成熟任务本体已经是分钟级；v4.7.0 要消灭的是人被迫守在闭环里的小时级损耗。
