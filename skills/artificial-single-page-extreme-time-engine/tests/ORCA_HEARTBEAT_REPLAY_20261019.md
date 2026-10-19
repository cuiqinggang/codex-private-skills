# Orca heartbeat 历史故障机制隔离复跑｜2026-10-19

## 历史根据
原始源码：`tasks/ORCA_CODEX_VALUE_VALIDATION_20261014/analysis/suite-ab-r3.py`。曾存在 `run_model` 同步发送 heartbeat，异常传播触发 finally 终止模型进程，随后 `label-done.json` 未写入的真实失败。历史文档 `CEO_SUITE_REALITY_REPORT_V1.md` 记录 F003 heartbeat 25s 超时导致任务未交付。

## 本次实际执行
Windows C 通道，本机 Python 运行 `tests/orca_heartbeat_historical_replay.py`。从真实历史源码核实心跳代码与回执位置，用独立的真实本地 Python 子进程模拟一段业务执行，并主动触发 heartbeat 请求超时情形。

- 原处理逻辑：子进程被终止，状态 FAILED_LOST_FINAL_RECEIPT，派发1次，回执0次。
- 改进处理逻辑：控制信道超时设 UNKNOWN，不重复发 heartbeat，不终止业务子进程；结果文件验收后写 DONE，派发1次、回执1次，脚本耗时8898.51ms。
- 再次运行：checkpoint DONE，直接返回，不重复派发，原回执保持。
- 本地脚本退出码0，SUMMARY.json 和 events.jsonl 保存在 `tests/orca_historical_replay_results/`（原始大日志只保留本机）。

## 边界及下一门槛
这是历史故障**机制复现**与真实本地子进程试验，不是官方 Orca 服务本身超时，也未重启/恢复正在执行的 Codex 模型会话；没有部署修补原运行器，不能宣布 Orca 正式生产闭环通过。对真正的 worker_done UNKNOWN 仍需官方 task-list/dispatch-show 只读对账，确认身份、状态与副作用后才可以继续；无证据禁止重发完成消息。要全体验收，需在授权独立运行环境中实际运行官方 Orca 生命周期，完整记录模型和控制面所有异常与最终 T_VALID。

此次无需人工节点级审批，测试固定故障路径中一次运行完成，但不能据此推断面对未知故障完全自治或提高10倍速度。
