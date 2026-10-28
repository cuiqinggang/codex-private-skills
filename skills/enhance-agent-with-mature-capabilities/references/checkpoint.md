# V1检查点

> 以下为V1原始历史起点。2026-10-29已完成DSH补测与迟后接续；先读[最新续接](dsh-continuation.md)，不要重跑库存题或沿用“DSH尚未执行”的旧状态。

TASK_ID：PI-DEFAULT-AGENT-20261029-001。封存：2026-10-29 01:37:51北京时间。
状态PAUSED_FOR_SKILL_HANDOFF：18条轨迹已结束，0条未结束，没有后台继续任务。
用户要求保存第1版，新页面继续；优先成熟现成方法，停止自制方案逐步试错导致过慢。

## 生产与候选

原默认入口：`C:\Users\A\Documents\DSH-Workspace\pi-capability-enhancement-20261028\Open-Pi.cmd`。
生产包装器1.3.1-scoped；Pi上游CLI1.4.0是另一版本概念。

前轮生产有固定订单、固定官方简报、精确归档、混合文件读取等限定直达链与可选recipes配置，不代表通用整体升级。
本轮通用候选在`C:\Users\A\Documents\DSH-Workspace\pi-default-agent-20261029\candidate`，增加原始技能摘录发现、原ACL内通用Python、混合文档批读和官方promptSnippet/promptGuidelines；**未部署生产**。

## 成果位置

任务根：`C:\Users\A\Documents\DSH-Workspace\pi-default-agent-20261029`。

| 文件 | 用途 |
|---|---|
| V1-CHECKPOINT.json | 生产状态与18条轨迹摘要、实际目录 |
| CANDIDATE-FROZEN.json | 最初通用候选 |
| REGISTRATION-REPAIR-FROZEN.json | 同名工具注册冲突的最小修复 |
| NATIVE-EXPOSURE-FROZEN.json | 官方原生工具说明字段接入后的冻结 |
| SUITE-FROZEN.json / RESULTS.json / SUMMARY.json | 第一阶段12条轨迹，跨配置，不是单一最终配置成绩 |
| FINAL-PROFILE-RESULTS.json | 最终候选下对账、文档、代码、页面4条轨迹 |
| HOLDOUT-FROZEN.json / HOLDOUT-RESULTS.json | 最终配置冻结后新生成的一组库存复合题 |
| FAULT-ORACLE-REPAIR.json / RECOVERY-REAUDIT.json | 故障见证误报分析；B未获重新接受 |
| PRODUCTION-BEFORE.json / production-rollback | 原入口摘要及原文件备份 |

初版两个B在模型启动前因工具重名退出。中间代码和页面的慢样本保留。最终B恢复业务数据正确，但故障见证误报后追加修复又超时，NOT_VALID仍保留；只读复核未满足重新接受条件，禁止擅改为PASS。

## 唯一NEXT_ACTION

新页面先按执行桥A核对生产CURRENT、V1回执和必要文件，然后优先用**现成DSH成熟交付入口**补做最小同合同对照，复用已冻结库存新题和现成验收资源，不扩建自制框架。

DSH截至V1仅完成源文件、配置、原恢复器读回，**未执行本轮新题**。按`next-method.md`处理native skill、session、日志差异；过去的DSH局部通过不算本轮通过。

禁止自动执行历史`deploy.py`：原发布门未满足，旧聚合逻辑不能自行解决跨版本、误报、超时和真实货币成本缺口。
