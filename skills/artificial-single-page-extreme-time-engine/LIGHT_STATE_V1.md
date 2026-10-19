# 轻量状态持久化 V1
VERSION=1
STATUS=RULE_FROZEN_REAL_ORCA_E2E_PENDING
PARENT=SANRENXING_V4.md
BRIDGE=V10_C_A_B
IMPLEMENTATION=REUSE_EXISTING_CHECKPOINT
## 统一入口
交代任务时指定「《三人行》第4版 + 轻量状态持久化 V1 + V10执行桥」。默认一项任务连续自主执行到 DONE、STOP_GATE 或真正需要用户授权，禁止每个节点都暂停征询。
## 仅保留六个字段
TASK_ID, STATE, ROUND(0..3), IDENTITY(任务/dispatch/进程), RECEIPT(哈希/状态), NEXT_ACTION。
字段不足时可引用外部证据文件路径，避免重复复制信息。
## 唯一状态路径
READ_CONTRACT -> RUNNING -> CONTROL_UNKNOWN -> RECONCILE -> RUNNING 或 DONE / STOP_GATE。
CONTROL_UNKNOWN 不等于业务失败。先只读核对业务进程、dispatch 身份和 task-list；业务仍运行就继续等已有执行；已提交则记录确认，绝不重新发 worker_done；进程确实结束且结果未提交才按受控恢复处理。UNKNOWN 无法确定则安全停止副作用，留下唯一 NEXT_ACTION。
## 三轮限额
最多三轮优化方案循环；恢复过程必须有界，不能靠无限重启扩大三轮限额。允许在一轮中诊断、修正和测试。每次更新 checkpoint 采用先临时写再原子替换；UTF-8 无 BOM。写入操作先确认是否已经提交（Exactly-once）。
## 版本规则
只用 V1,V2,V3 自然数递增，每次版本必须有 CHANGELOG: 故障、修改、现实测试、未通过项、可回退版本。版本号变化不等于自动通过完整生产验收。
## V1 历史记录
2026-10-19：T03 零任务报告故障回归通过；heartbeat 历史故障机制在真实本地子进程隔离重放通过；发现 PowerShell UTF-8 BOM 使 JSON checkpoint 解码失败。修正规则为统一无 BOM 编码、CONTROL_UNKNOWN 独立对账、确认提交后不重派。
## 未通过的生产门
真实 Orca 服务发生 heartbeat 超时后的同身份继续、worker_done 对账、业务独立 QA 和完整 T_VALID，尚无本版本的新端到端验证。不得标记 FULL_PASS。
