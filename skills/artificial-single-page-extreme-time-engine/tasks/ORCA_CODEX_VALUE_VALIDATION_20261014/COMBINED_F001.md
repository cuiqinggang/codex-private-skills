# COMBINED-F001｜Orca与Codex同一T01业务冻结
日期2026-10-16北京时间。用户本轮明确要求把两条已验路径合起来完成同一项真实业务。CEO_APPROVAL=APPROVED_THIS_SCOPED_NODE_AFTER_STATIC_REVIEW；不沿用旧空F001或冒充三任务N002批准。
方法沿本项目三人行V2 C002，桥V7 C优先/A暂停/B备用。

## 业务与输入
选固定数据集原始BAD的T01响应打分语义修复。新副本C:/AI/Orca-Codex-Validation-20261014/combined-business-20261016-r1。此前原生Codex基线中的T01成功不等于本管理链成功，本轮是新隔离联合验收，不修改既有GOOD；不重做已验T03。
输入沿DATASET_MANIFEST.json逐文件SHA核对，requests/T01.md原需求；代码llm_verifier/fine_grained_reward.py。仅允许修改该代码、新tests/test_t01_offline.py和DELIVERY.md；编译缓存单列。其他原输入摘要必须保持一致。
独立固定验证器SHA256=2d6f62b3205454ce5758c98c0160d7aa03b2820f7f05f9c1302a89651cb24979，选T01九项+ALL_source_compile共10项；原BAD必须检出失败，最终10/10且模型新增回归测试独立运行exit0，人工审查差分，才接受。不让模型读隐藏验证器/旧答案。

## 唯一组合与实际角色
官方Orca隔离runtime→协调终端run/task→独立worker终端→context-only dispatch返回原preamble→同一worker下Codex exec UTF8 stdin→独立QA→父执行器在真实原身份发worker_done→协调者回读task/dispatch及worker_report→外部差分/测试/产物摘要/清理/证据回读。
原preamble完整保留并散列；明确父执行器负责heartbeat/完成回执，模型只完成代码业务、不自行再次发送管理消息。父执行器不替模型写业务修复。
Codex0.160.0、gpt-6.1-sol、ultra、priority请求；workspace-write/on-request/auto_review、network_access=false，真实home复用已有登录、不读认证。最终以本次精确session的turn_context核对实际策略；priority实际tier未知不得冒称。
Orca固定v1.4.224资产、后台0.1.0+9e2e3cd709d0，本机127.0.0.1/no-pairing、无托管账户、hooks及预信任关闭；仅命令行精确信任本次fixture/worktree。
context-only为unsupervised；这里是GPT批准的一次任务薄适配，不新造通用调度器。

## 有界恢复及故障推演
初次360秒。自然超时→只停并wait所属Codex子树→对账该精确session、现有差分和QA；已合格不重做，未完成才保留恢复前副本、同终端同工作树同参数官方exec resume一次，最多600秒。
保持Orca runtime/terminal/pane/process incarnation，恢复前后必须一致；不新建终端冒用旧dispatch；session未知、子树未退出、安全/权限/额度拒绝不盲重发。非超时业务失败先保存，不偷偷启动第二个新会话。
全节点1200秒，模型为验收/结算预留180秒；CLI25秒，worker_done150秒受全局余额限制。父级每300秒发心跳但不延长任务预算。完成请求UUID先持久化；UNKNOWN不重发新请求。此次不再人为注入已验故障，不为了证明恢复而破坏正常业务。
产物通过但Orca结算失败：只修管理回执，不重跑Codex；Orca完成但外部QA失败：不接受。外部未解释报错回虚拟分析，禁止原脚本无差分重跑。

## 资源/计时/回滚
新节点存在即拒重跑；入口核对本任务未遗留Node/Codex、至少4GiB可用内存，不停其他任务。至多一个Codex模型进程，无额外模型协调者。
入口单调时钟在资源/输入核对前开始；本地终点包含QA/清理/结果写入回读。首次GitHub证据归档回读后追加最终时间。更早规划部署未测成本仍UNKNOWN，不用该任务冒称完整项目T_VALID/净节时。
回滚只关闭本任务终端/所属进程，保留新工作树与全部失败证据；不改代理/ACL/全局配置，不触及历史被拒工作流。

## 冻结
analysis/combined-business-r1.py@59b62af13c899395e3aea2433c8288be2b5bd09f
SHA256=fca83d88fc75c62640251aa52dc6f69f88edca1db266017bad83a83a74d9dc77
Python编译检查通过；复用已通过的same-pane身份、官方settlement、预算函数及exec/resume输入机制，仅合并上述业务。一次真实联合验证后保存结果，不增加完整三任务/十轮/AB计数。
