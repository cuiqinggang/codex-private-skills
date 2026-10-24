# N004｜真实 Tymeslot 预约写入中断、对账和安全续跑 R1
日期：2026-10-24；TASK_ID AIORG-20261024-004/N004/V1。
真实 Windows Puppeteer 执行端向本地 Tymeslot 预约页面提交一笔合成预约，在提交动作后立即以退出码 77 中断（故障位于响应确认前）。主控重新查询同一测试邮箱的真实 PostgreSQL 预约表：1 条 confirmed。按 Exactly-once 原则，本次不盲目再次提交，而是选择 READBACK_ONLY_NO_DUPLICATE 并确认原预约有效。
业务对账耗时 11.548 秒（该测试脚本内部 wall time）；worker exit=77；booking_count=1，原 meeting id 651f890e-5528-47c0-8e20-66a91ff17dd5。该记录为隔离测试数据，不是客户预约。
随后通过官方业务取消页面删除合成预约，退出码 0，取消脚本运行 6.97 秒；直接 SQL 只读复核测试邮箱结果 cancelled|1，确认没有重复预约并完成清理。
第一次清理脚本复制到新目录时相对 require('./docker-ops.cjs') 报 MODULE_NOT_FOUND；修正为已存在的绝对模块路径后重新运行通过。失败修复所耗时间未纳入 11.548 秒；不可声称为原任务完整 T_VALID。
本轮判定：REAL_WRITE_INTERRUPT_RECONCILE_NO_DUPLICATE=PASS；真实提交后执行端崩溃情况下，发现已确认副作用便不重做。没有覆盖请求完全未进入服务端时的“确认未执行后重新提交”分支，也没有证明服务端断电、真实 GPT 网页重发、改期、CalDAV/邮件全量独立验收或整任务 T_VALID。N004 和 INC-002 仍 OPEN。
本地原始回执：C:\AI\AIORG-Shared\tasks\AIORG-20261024-004\N004-REAL-WRITE-INTERRUPT-R1.json，执行程序 n004_real_write_interrupt.cjs。
