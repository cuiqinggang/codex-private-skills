# EXP-OPENMAUS-001｜成熟智能体平台与确定性直达的合同边界
版本V1；核查日期2026-11-01；类别CASE/ERROR/CANDIDATE_RULE；证据=OpenMausBot官方Windows npm服务及原48/480行订单本地限定对照。

触发：希望将OpenMausBot平台接入现有AI自动化组织V5，以更直观的Windows工作台代替既有订单流程。环境：OpenMausBot 0.1.136本地npm server及网页工作台，原订单配方、相同独立QA和输入SHA。
LAST_GOOD：原确定性订单直达原配方及校验器。FIRST_DELTA：平台初次batch 242.449s超时无产物；项目工作目录过宽导致git add checkpoint等待120s，以及工具配置/审批模式不匹配。最小处理：按原合同隔离订单workspace并限制工具和配置，保留原输入与独立20项验收器。
回归：平台最终normal/batch/recovery三种订单各20/20、哈希一致且一次生成；官网npm工作台可运行。原确定性直达normal=14.464s、batch=25.910s、recovery=19.462s；平台normal=90.213s，隔离batch/normal约234.5s、recovery=41.378s，单次顺序且系统资源负载变化，计时口径不同，不能视为完整公平T_VALID或全平台性能排名。
决策：原订单保持V5成熟确定性直达，不为了视觉工作台引入额外启动、模型和审计成本。桌面NSIS安装器退出2未修；npm工作台PASS不等于桌面安装器PASS或平台跨重启认证。
适用：固定结构本地订单及成熟平台净收益筛选；不适用：浏览器、研究、视频、跨整机重启、真正长期无人值守等未经测试任务，模型账单亦NOT_MEASURED。
TASK_ID=OPENMAUSBOT-COMPARE-20261101。原证据：C:\Users\A\Documents\DSH-Workspace\openmausbot-comparison-20261101\COMPARISON.json、COMPARISON.txt、ROUTING-DECISION.json、ISOLATION-FREEZE.json。
