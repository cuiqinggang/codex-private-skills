# 官方 context-only 派发路线审查
固定 Orca 提交 2bb20586ebc39d605e16d95f57420e20a16e7485。

在R3等待期间核对，不产生新Windows业务动作：
- CLI dispatch-handlers.ts blob c8ade53e907a5ecc2c4276988a5a3db3ae802954：orchestration dispatch 只有显式 --inject 才注入PTY；--return-preamble可返回官方完整任务正文。
- RPC runs/dispatch-methods.ts blob 041ae7fff3834892a4e91041328c6b9aa66d1aa9：非inject也创建真实Dispatch；绑定真实coordinator/run/task和assignee。任务须ready；不是自行写数据库。context-only自派发源码明确合法，但不能冒称有监督worker。
- manual-dispatch-observation.test.ts blob 06b16eaff1ac34220a47258b52f862aabd5e5c37：此类任务workerShow显示unsupervised/context_only；release/stop不自动关操作者终端。源码测试存在，不等于本机测试通过。
- task-handlers.ts blob d6201087792c31e917a7111ea1f31c00c168e364：官方run/task创建与task-update入口存在，但成功状态必须来自实际业务验收，不能预填completed。

候选：真实Orca协调终端建立Run/Task/Dispatch，return-preamble走Codex exec stdin；任务结束由合法身份提交完成/失败，外部QA独立验收。可避免PTY正文粘贴，无需修改官方源码或自建调度器。仍需核对最终身份/完成协议并做实际验收；R3只跑基础terminal→exec，不冒充此编排链已执行。

R3中Codex本身出现request timed out，网络/服务响应问题与输入传输问题分列。网络/代理不在本次修改范围，不用配置放宽、切换账号或绕过challenge来修复。先等本次有界结果并保全证据，再按具体失败节点处理。正式业务十轮与AB不增加。
