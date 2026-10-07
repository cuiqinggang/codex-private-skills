# 《当前任务目标与正反约束 第2版》

任务ID：METHOD-SYSTEM-LARGE-VIRTUAL-MATURITY-20261008
合同版本：2
状态：CURRENT

## 最终现实目标

以已经现实完成、正确终局已知的“旧双页面控制恢复 / LTMVH 页面控制闭环”为唯一大型成熟母任务，
按《人工单页面极限短时间引擎》第22版、《极限短时间执行大脑》第18版、
《当前任务目标与正反约束》第2版、《新页面运行模板》第17版，
从 TASK_ACCEPTED 开始做 Production-Equivalent Adversarial Replay（生产同构对抗式虚拟重放）。

## 正向约束

- 从 TASK_ACCEPTED 真正从头开始。
- 必须覆盖多阶段、CEO/Executor、串并行、Freeze、Reality、FAIL/Delta、重新虚拟成熟、True New Chat、跨页恢复、Merge、FINAL_VALID。
- Fail Fast → Repair → Restart。
- 第一个确认方法故障出现即停止，不带病继续。
- 只升级真正负责故障的版本，并做最小修复。
- 修复后从 TASK_ACCEPTED 全部重跑。
- 第一次完整到 FINAL_VALID 后，再做一次完整 clean replay。
- 两遍大型完整重放均无旧故障复现、无新结构故障，才允许 VIRTUAL_MATURE=YES。
- 本阶段仅为虚拟成熟，不得写成 Reality 实测认证。
- 页面长时间停在思考/恢复/寻找路径而无推进时，优先判定是否为控制流故障，不允许无限等待。

## 反向约束

- 不把历史母任务的业务故障误判成当前方法故障。
- 不在 Reality 内现场修改 Freeze。
- 不跳过 FAIL/Delta 后的回虚与 Reverify。
- 不用 Branch 代替 True New Chat。
- 不让并行 Executor 直接写全局 Freeze。
- 不让旧 CEO 与新 CEO 同时成为全局 writer。
- 不把 LTMVH 整体项目 FINAL_VALID 与“页面控制闭环”子任务 FINAL_VALID 混为一谈。
- 不因已有小样本通过而提前宣布大型 VIRTUAL_MATURE=YES。

## 母任务 Oracle

权威历史证据：
- skills/long-term-memory-super-virtual-human/REALITY_STATUS_2026-10-04_V0.4.5.md
- skills/long-term-memory-super-virtual-human/CHATGPT_SESSION_CONTINUITY_CONTROLLER.md
- skills/long-term-memory-super-virtual-human/evidence/SINGLE-BROWSER-LOOP-FIX-REALITY-20261003-R15.json
- skills/long-term-memory-super-virtual-human/evidence/STALL-DETECTION-FULL-E2E-REALITY-20261003-R10.json
- skills/long-term-memory-super-virtual-human/evidence/TRUE-NEW-CHAT-EXISTING-BROWSER-REALITY-20261003-R6.json
- skills/long-term-memory-super-virtual-human/evidence/CEO-CLEAN-LIFECYCLE-EXTREME-TIME-20261004-R18-R19.json

已知正确终局（仅页面控制闭环子任务）：
- clean baseline = 恰好 1 个空白 New chat 根页；
- CEO-1 拆分 / DONE_WHEN；
- 最少必要 Executor；
- checkpoint 后 True New Chat CEO-2 接管；
- exactly-once，不重做已接受子任务；
- 完成 Executor 立即关闭；
- FINAL_VALID 后恢复恰好 1 个空白 New chat 根页；
- 历史最佳有效结果 R18 = 51,454 ms，R19 同构复验 PASS；
- LTMVH 整体项目级 FINAL_VALID 仍不得因此改写为 YES。

## DONE_WHEN

1. 第一遍完整大型对抗式 replay 从 TASK_ACCEPTED 到页面控制子任务 FINAL_VALID；
2. 历史 R15、R10/R6 等故障链被正确作为母任务 Reality/恢复事件处理；
3. 当前方法若有结构故障，首个故障即 Fail Fast；
4. 第一遍 PASS 后仍保持 VIRTUAL_MATURE=NO，进入第二遍 clean replay；
5. 第二遍也完整 PASS 后才允许 VIRTUAL_MATURE=YES；
6. REALITY_CERTIFIED 始终保持 NO，除非另行进行新的 Reality。
