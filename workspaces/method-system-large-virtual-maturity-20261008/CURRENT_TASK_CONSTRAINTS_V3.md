# 《当前任务目标与正反约束 第3版》

任务ID：METHOD-SYSTEM-LARGE-VIRTUAL-MATURITY-20261008
合同版本：3
状态：CURRENT
升级来源：第2版
任务类型：双大型成熟母任务并行生产同构对抗式虚拟成熟

## 最终现实目标

在当前正式方法版本下，同时运行两个不同类型、现实已经完成、正确终局已知、证据充分的大型成熟母任务，从各自 TASK_ACCEPTED 开始做 Production-Equivalent Adversarial Replay（生产同构对抗式虚拟重放），重点验证跨任务并发时的任务隔离、CEO/Executor 隔离、Freeze 隔离、共享资源仲裁、页面生命周期、失败恢复与 FINAL_VALID 回收。

本合同升级只改变本次验收强度，不自动升级方法版本。

## 固定方法起点

- 《人工单页面极限短时间引擎》第22版
- 《极限短时间执行大脑》第18版（若本轮确认其为故障责任层，允许最小升级）
- 《新页面运行模板》第17版
- 初始方法固定版本：e64f7593a732a99c82c8d4e36b30e25f89d00aa7

## 大型成熟母任务 A

TASK_A_ID=DUAL-STRESS-A-LTMVH-PAGE-CONTROL-20261008

旧双页面控制恢复 / LTMVH 页面控制闭环。

必须完整覆盖：
- CEO / Executor；
- 多阶段；
- 串行与并行；
- Freeze；
- Reality；
- FAIL / Delta；
- 回虚；
- Repair；
- Reverify；
- True New Chat；
- exactly-once；
- 页面卡死恢复；
- 专用浏览器复用；
- 浏览器重复启动防护；
- Executor 完成后关闭；
- CEO 换页与关闭；
- Merge；
- FINAL_VALID。

权威 Oracle：
- skills/long-term-memory-super-virtual-human/REALITY_STATUS_2026-10-04_V0.4.5.md
- skills/long-term-memory-super-virtual-human/CHATGPT_SESSION_CONTINUITY_CONTROLLER.md
- skills/long-term-memory-super-virtual-human/evidence/SINGLE-BROWSER-LOOP-FIX-REALITY-20261003-R15.json
- skills/long-term-memory-super-virtual-human/evidence/STALL-DETECTION-FULL-E2E-REALITY-20261003-R10.json
- skills/long-term-memory-super-virtual-human/evidence/TRUE-NEW-CHAT-EXISTING-BROWSER-REALITY-20261003-R6.json
- skills/long-term-memory-super-virtual-human/evidence/CEO-CLEAN-LIFECYCLE-EXTREME-TIME-20261004-R18-R19.json
- workspaces/method-system-large-virtual-maturity-20261008/evidence/REPLAY1_FULL_TRACE.md

已知正确终局：
- 页面控制闭环 FINAL_VALID=YES；
- R18=51,454ms；
- R19 同构复验=54,246ms；
- 最终恰好 1 个空白 New chat 根页；
- 项目级 LTMVH FINAL_VALID 不因此改写为 YES。

## 大型成熟母任务 B

TASK_B_ID=DUAL-STRESS-B-H3P1-VIDEO-CONVERGENCE-20261008

H3-P1“首个有效图声对”完整视频极限时间收敛母任务，不得缩减为一次简单视频生成。

必须重放完整历史收敛链：
- 初始基线 T*=653,921.787ms；
- R1 阶段分解与编排空耗定位；
- R2 单本机闭环 runner、history/output publication race 修复、12-step、随机 seed 语义漂移、固定有效 seed；
- R3 warm path + lightweight verifier；
- R4 最佳阶段组合；
- 单 decode；
- 单次无目标提示 ASR；
- 独立 verifier 并行；
- FAIL/INVALID 候选不得冒充 T*；
- 最终 Reality-certified FINAL_VALID；
- 最终 T*=288,281.990ms。

权威 Oracle：
- skills/video-extreme-time-engine/SKILL.md
- skills/video-extreme-time-engine/FREEZE.md
- skills/video-extreme-time-engine/CASE-H3-P1.md
- skills/video-extreme-time-engine/CHANGELOG.md

VALID 规格保持：
成年女性正面对镜头挥手，清楚说中文“你好”，存在有效人声、音画基本同步、最低展示可用，且必要 verifier 全 PASS。

## 双任务隔离硬约束

1. TASK_A / TASK_B 各自独立 TASK_ID。
2. 各自独立 CONTRACT_VERSION。
3. 各自独立 FREEZE_VERSION 序列与 FREEZE_TAG。
4. 各自允许拥有自己的 ACTIVE_CEO；若当前方法对此存在歧义，必须通过实际控制流判定。
5. A 的 CEO 不得修改 B 的任务状态。
6. B 的 Executor 不得写入 A 的 Freeze。
7. 两任务可同时存在 Executor 并行。
8. Executor 返回顺序必须交错。
9. 两 CEO 的 Freeze / Merge 顺序必须交错。
10. A/B 任一触发 True New Chat 时，另一任务继续推进。
11. 任一 Reality FAIL / Delta 不得阻塞或回滚另一任务。
12. 任一 Repair / Reverify 只作用于本 TASK。
13. 任一卡死/恢复不得导致另一任务重复执行。
14. 关闭 Executor/CEO 必须按 TASK_ID + PAGE_ID 精确回收，不得误关另一任务。
15. 共享 persistent browser、GitHub main writer、Windows 执行通道或其他稀缺资源发生竞争时必须有明确仲裁。
16. 不允许第二套不必要 persistent browser。
17. 不允许两个 writer 同时控制同一共享可变资源。
18. 不允许旧 CEO / 新 CEO split-brain。
19. TASK_A / TASK_B 的 Freeze version、STATE_REF、证据路径不得串线。
20. 任一任务 FINAL_VALID 后只能回收自己的资源；若共享资源仍被另一任务使用，不得销毁。

## 重复压力

同一双任务母测试必须多次制造并验证：
- Executor 并行；
- 交错返回；
- CEO Merge；
- Freeze；
- CEO 换页；
- True New Chat；
- FAIL / Delta；
- Repair / Reverify；
- 页面关闭；
- 共享资源申请、等待、获取、释放。

禁止用单次偶然 PASS 代替重复压力。

## Fail Fast

一旦首次出现以下任一项：
- 两个合法解释导致不同控制结果；
- 状态污染；
- 双 writer；
- Freeze 串线；
- 错误 Merge；
- 错误关闭；
- 无法继续；
- 共享资源无确定仲裁；

立即：
Fail Fast → Stop → Root Cause → 只升级真正负责版本 → 最小修复 → 从 TASK_A/TASK_B 两个 TASK_ACCEPTED 全部重跑。

不得带病继续收集后续错误。

## 版本责任

- 具体判断 / 跨任务调度 / 共享资源仲裁：优先《极限短时间执行大脑》；
- 页面生命周期 / handoff / CEO 页规则：优先《新页面运行模板》；
- 只有整套总纲职责根本改变才升级《人工单页面极限短时间引擎》。

一次确认故障只升级真正责任层。

## DONE_WHEN

只有同时满足以下全部条件才允许 VIRTUAL_MATURE=YES：

- A、B 都从各自 TASK_ACCEPTED 到各自 FINAL_VALID；
- 存在真实并发交错；
- 多轮并行 / Freeze / Merge / 换页 / FAIL / Recovery 重复覆盖；
- 无 TASK_A / TASK_B 状态污染；
- 无 Freeze 串线；
- 无错误 Merge；
- 无重复执行；
- 无双 writer；
- 无错误页面关闭；
- 无重复 persistent browser 启动；
- 无共享资源失控；
- 无旧故障复现；
- 无新的结构性方法故障；
- 若发现方法故障，已完成最小修复并从两个 TASK_ACCEPTED 全部重跑通过。

最终：
VIRTUAL_MATURE=YES
REALITY_CERTIFIED=NO

本轮是生产同构虚拟成熟，不是新的现实 Reality 认证。
