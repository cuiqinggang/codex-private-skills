# LTMVH v0.7.0｜Reality Backlog

状态：SAVED_NOT_FROZEN

## P0 必做
- R1：同构任务 Current Page vs Frozen Node + True New Chat，比较完整 T_VALID。
- R2：同一独立任务集 Serial vs Parallel-2 vs Parallel-4/可承受并行度。
- R3：页面数量/资源占用 Benchmark；冻结后关闭无价值页。
- R4：语义边界触发 vs 固定字数/轮数阈值。
- R5：Frozen Node 合并 Gate：并行结果分别验收后合并。

## P1 恢复与自动化
- R6：真实 GPT/网页故障→Goal Loop 自动发现→恢复→继续→业务验收。
- R7：CDP/Chrome 主进程失效故障注入→第一性原理定位→局部修复→继续。
- R8：自动节点冻结→true New chat→minimal handoff→exactly-once。
- R9：自动页面价值判断→关闭无价值页面→最终单空白页。
- R10：动态 continue/rotate/serial/parallel scheduler 的恢复、去重、故障注入。

## P2 工具组合
- R11：Frozen Node + ECC V3.1 长流程对比。
- R12：GPT direct / Codex / Runner / Reasonix 按任务类型的 T_VALID 路由表。
- R13：按需审计强度的收益/成本对比。

## 冻结门
v0.7 最终冻结前至少需要：
1. P0 全部完成；
2. 关键自动化 P1 至少形成一条完整 Reality 闭环；
3. 没有已知会破坏 v0.6 冻结合同的回归；
4. 主运行合同、方法文档、证据、Changelog 一致；
5. 明确 FINAL_VALID 范围，不把未测能力写成 PASS。

## 2026-10-04 现场新增 P0
- R14：透明有界调度：同一专用 browser/context 内 1 路 vs 2 路 vs 3 路 executor 页面；验证无第二浏览器、无无限标签、状态可见。
- R15：队列透明度：至少验证 QUEUED / DISPATCHED / RUNNING / WAITING_EXTERNAL / STALL_SUSPECTED / VALID，排队时必须可见 queue position。
- R16：模型强度路由：简单 executor 用 Instant/Medium、复杂任务按需 High，对比 T_VALID、返工率与高档额度消耗；禁止把 R14 的“恢复原 High”误当永久默认。
- R17：多入口竞争：两个普通浏览器/两个上层任务同时派发时，验证它们进入同一 scheduler 后不会争夺同一 page、不会双写、不会形成不可解释长黑箱。

