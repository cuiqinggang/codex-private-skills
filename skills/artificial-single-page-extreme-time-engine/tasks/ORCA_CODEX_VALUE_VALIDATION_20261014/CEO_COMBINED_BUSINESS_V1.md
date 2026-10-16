# Orca＋Codex 同项真实业务联合验收 V1

2026-10-16。方法《三人行》第2版 C002 不变；桥 V7，C优先，A暂停。用户授权把已验执行恢复路径与已验管理链结合完成同项真实业务。本节点已完成，结论为 RECOVERED_ACCEPTED，非一次无故障通过。

## 实际交付
在全新隔离工作树重放 T01 模型响应解析真实缺陷。原始隐藏验证 4/10，最终外部验证 10/10；独立运行新增离线 unittest 15/15（0.061s 为测试局部耗时）。源码修改仅新增共用响应文字恢复函数，替换两处文字获取，并阻止空白 token 覆盖评分分布；新增 tests/test_t01_offline.py 与 DELIVERY.md。已验 T03 的三个摘要与入口逐项一致，其他输入保持不变。

冻结 COMBINED_F001.md@bf3edba8a48e9ab386b9b28a865a5b9ed2b8ff7a；执行脚本 analysis/combined-business-r1.py@59b62af13c899395e3aea2433c8288be2b5bd09f，SHA256 fca83d88fc75c62640251aa52dc6f69f88edca1db266017bad83a83a74d9dc77。

## 同一条真实管理与执行链
官方本机隔离 runtime → 官方 coordinator terminal → run/task → 独立 worker terminal → context-only dispatch 返回官方 preamble → stdin Codex exec → 精确 session resume → 外部检查 → official worker_done → task与dispatch回读 completed。协调器为一次性确定性脚本，无额外模型、无自研通用调度器。

run=run_dd371e211c8c
task=task_625c7c2df964
dispatch=ctx_0dd2a061001d
worker=term_cdc83131-d1a2-42c3-bc8f-70d610309314
session=01a1445c-129f-78d2-b78f-5bb71e2029e6
request=5206f365-5f1f-4884-b932-f7dd4251c98e
message=msg_3e3fd4beaa6e

初次 exec 360781.670ms 到预算，终止所属子进程并确认退出；代码已通过10/10但无交付文件。在同一 Orca terminal/pane 保留身份恢复上述确切会话，仅一次 resume，219693.890ms 后 exit0。worker_result provenance=worker_report，outcome=succeeded，messageId 与 worker_done 一致。没有创建第二个业务任务或重派UNKNOWN请求。

实际会话记录确认 gpt-6.1-sol、ultra、workspace-write、network_access=false、on-request、auto_review、正确工作目录；priority仅请求值，service_tier=null，不能声称服务端已采用priority。真实用户home保留，不复制凭据，不改全局配置。

## 本轮故障与最小纠正
1. 初次与恢复均出现网络重连/请求超时；Codex官方记录从WebSockets回落HTTPS，随后完成业务。未改代理/网络，不声称网络根因解决或人为断网恢复通过。
2. 原验收脚本在业务已结算后报 AGENTS.md：准备阶段主动把隔离fixture的AGENTS.md写成冻结SPEC，而末尾错误地要求与原数据集相同。原 result.json passed=false 与670113.090ms失败计时保留。
3. 独立纠正脚本仅核验既有成果：AGENTS.md字节必须等于冻结SPEC且等于git HEAD；其余非目标输入仍逐个比原摘要；独立运行15项测试、检查diff/输出/旧T03/所属进程。没有修改业务代码、冻结执行脚本或重跑模型。本次不是未经修改的冻结版本无故障通过。

原异常使显式 terminal close 步骤未到达，但 finally 已终止本次runtime及其子进程；独立检查本节点Node/Codex无残留。隔离数据库中的终端元数据可能保留，不把进程清理冒称官方逐个close成功，不为美化记录重启运行时。

## 计时
入口至原失败回执本地回读：670113.090ms。
入口至纠正验收本地回读：731617.153ms（12分11.617秒），包含超时、恢复、管理结算、验收脚本误报、诊断与独立核验。排除此前分析/部署以及之后网上归档回读。
首份完整证据已上传并逐字回读；随后取远端单调时钟时C报告无在线设备，未得到最终计时回执，因此入口至网上归档回读精确耗时 UNKNOWN。不能用本地12分11.6秒代替完整项目耗时或效率增益。此次离线提示发生在业务验收与首份归档回读完成后。

## 归档
evidence/COMBINED_R1_ACCEPTANCE.json@785e2e40159e2bcfbc8aef3437fbcbae49dcba41：含原失败、官方完成回执、实际参数、两次模型运行、外部检查、最终源diff、独立测试输出、三份成果全文与原文件摘要。已逐字回读。
evidence/COMBINED_R1_ARTIFACTS/：三个成果文本分别保存并逐字回读；不是全部大型原始日志备份。
analysis/combined-reconcile-r1.py@187bb747d856755cb67bb7b2e77b772fb9d4e8c1：最小纠正核验脚本，已回读。
Windows：C:/AI/Orca-Codex-Validation-20261014/combined-business-20261016-r1/worktrees/fixture/lifecycle

## 边界与接续
同项T01真实业务联合闭环已验收，不再标为“只有启动没有产物”。不要重新修复T01或既有T03。项目正式三任务整套Reality、连续十轮及A/B配对仍0；融合技能包未正式发布，三人行未升级V3。整运行时退出后的派发身份恢复、容量、净节时未认证。
后续若批准扩大业务，先将AGENTS基线纠正纳入新的不可变冻结，并明确异常清理与持久终端记录语义；本次单任务成功不替代全套虚拟成熟或公平效率比较。
