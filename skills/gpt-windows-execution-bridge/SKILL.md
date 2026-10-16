---
name: gpt-windows-execution-bridge
description: GPT连接Windows的正式通道路由入口。适用于《GPT直连Windows双路执行桥》及《三人行》调用Windows执行器的任务；默认读取V9.0规则，C绝对优先，失败后才可降级A、B。
---
# 《GPT直连Windows双路执行桥》正式入口：V9.0

权威路由规则：`skills/gpt-windows-execution-bridge/v9-deterministic-routing.md`，仓库 `cuiqinggang/codex-private-skills`，分支 `main`。

## 确定性要求
- 新任务路由只能采用 C→A→B。先 C 健康及无副作用业务执行检查；C 成功必须使用 C；禁止以方便、习惯、历史路由为理由直接选择 A。
- C 实际失败后有界重试一次，仍失败方可转 A；A 亦失败才可转 B。每次降级保存可审计证据。
- C 恢复后的新任务自动回 C；执行中任务保护 exactly-once，避免重复执行或中断副作用操作。
- 无权操作现有网络配置、FlClash、代理、登录浏览器、密钥或隧道。不能以旧设备ID离线认定C故障。
- 验收以真实的 C 业务执行与路由决策日志为准；规则文件保存不等于所有执行器已加载、也不等于故障切换已通过。

## 与《三人行》关系
任何版本《三人行》调用Windows桥，首先读取本入口和上面的V9.0规则；本入口**不擅自改变《三人行》方法版本指针**。第3版具体权威方法源码仍须独立确认及接入。
