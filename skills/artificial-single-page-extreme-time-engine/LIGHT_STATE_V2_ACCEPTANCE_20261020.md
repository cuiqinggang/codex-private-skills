# 轻量状态持久化 V2 验收记录

STATUS=PARTIAL_PASS_NOT_FULL_PASS
SOURCE=n8n-local 2.38.7; Windows C direct

## 本轮独立容器真实执行
- n8n 导入两个离线隔离工作流：IMPORT_RC=0
- 正常计算：SUCCESS_RC=0, status=success, storedAt=db, finished=true
- 执行起止时间 2026-10-19T17:16:35.669Z 到 17:16:38.102Z，内部区间 2.433 秒
- 主动抛出 INJECTED_FAILURE_SAFE：FAILURE_RC=1；节点故障被识别且未错误宣布成功
- 整个容器导入及两次执行命令 38.13 秒，不可用作热态业务性能比较
- 正常和失败日志分别在桌面 N8N_V2_SUCCESS.log 与 N8N_V2_FAILURE.log

## 未通过的能力门
- 故障自动重试后成功交付：未验证
- Wait / 容器重启续跑：未验证
- 长任务执行中断后的同身份接续：未验证
- 外部副作用重复提交防护：未验证
- GPT-only 与 GPT+n8n 同业务完整有效时间比较：未验证

## 结论
n8n 继续作为 V2 已采用组件，但不能据此认定解决了完整状态持久化。不得发布 FULL_PASS。生产容器未更改。

## 后续补测：正常 Wait 恢复 PASS
- 隔离工作流 Manual -> Before -> Wait(5 seconds) -> After，导入返回码0，执行返回码0。
- n8n 执行记录内部起止：2026-10-19T17:23:43.346Z -> 17:23:50.475Z，7.129秒；结束状态success、finished=true，storedAt=db。
- 等待前后的 marker 均为 XYZ-20261020；lastNodeExecuted=After，说明等待后继续执行。
- 此测试没有重启执行宿主，不能当作跨重启恢复 PASS。
- 原始证据：C:\Users\A\Desktop\N8N_WAIT_TEST.log，测试源：C:\Users\A\Desktop\N8N_V2_WAIT.json。
- 生产级状态仍为 PARTIAL_PASS，未验收跨重启和外部 Exactly-once。

## 第三轮成熟能力现实验收（同日追加）
1. 持久化跨宿主重启 PASS：隔离 sqlite 的 execution_id=2 在 Wait(120s) 阶段记录为 waiting，原容器停止后新 n8n 服务从相同 SQLite 恢复，最终 status=success, finished=1；执行窗口 17:28:03.427Z～17:30:06.439Z。原始执行数据 Manual/Before/Wait/After 均仅1次，marker RECOVERY-20261020 保留。
2. 瞬时 HTTP 故障重试 PASS：首次服务返回503，第二次成功；n8n execution_id=3 status=success、finished=1；flakyCalls=2，执行窗口 17:33:02.955Z～17:33:05.286Z（2.331秒）。
3. 外部业务幂等 PASS（依靠接收端成熟原子幂等语义，不是 n8n 本身恰好一次）：同一 Idempotency-Key 两次 POST；effectCalls=2、effectCommits=1；n8n execution_id=4 status=success，执行窗口 17:33:13.209Z～17:33:14.232Z（1.023秒）。
4. 原先故意抛出不可恢复业务异常已确认 FAILURE_RC=1，不会误标成功。普通 Wait 5秒内部7.129秒，输出同一标识。
证据在桌面 N8N_V2_ISOLATED_DB/database.sqlite、N8N_RETRY_TEST.log、N8N_DEDUPE_TEST.log、N8N_MOCK_COUNTERS_20261020.json、N8N_WAIT_TEST.log；生产容器未更改。
## 明确边界
技术隔离合同验证通过；尚未在真实 Gmail/Orca 跨会话业务中完成端到端 QA，不将隔离测试冒充全部实际业务 FULL_PASS。ChatGPT 未委托给持久宿主的推理无法靠 n8n 自动唤醒。未进行生产级断电数据库一致性及大规模并发压力测试。

## GPT→n8n 任务移交：真实隔离 E2E
任务 ID GPT-HANDOFF-20261020-001；GPT 写入 handoff.json 和工作流，隔离 Docker n8n CLI 自主运行，输出持久化于独立 SQLite；从原任务 ID 及 execution_id=1 找回业务 QA PASS、结果268和最终 COMMITTED。n8n status=success，finished=true；Start、Contract、PersistWait、Deliver 各运行一次；数据库记录 11.604 秒（含9秒 Wait）。证据：桌面 GPT_N8N_HANDOFF_V2_20261020 目录及 verified_receipt.json。
边界：仅证明委托后独立运行及回执恢复；当前 GPT 会话并未实际终止，不能声称任意聊天上下文自动重建 FULL_PASS。
