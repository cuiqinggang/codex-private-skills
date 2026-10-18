---
name: gpt-windows-execution-bridge
description: GPT连接Windows的正式通道路由入口。V10.0要求先动态发现在线C设备并真实验证；旧ID离线不得误降级。C>A>B。
---
# 《GPT直连Windows双路执行桥》正式入口：V10.0

**权威规则**：`skills/gpt-windows-execution-bridge/v10-deterministic-routing.md`（仓库 `cuiqinggang/codex-private-skills`，分支 `main`）。

## 每个新任务必经的执行顺序
1. **先走 C 的 list_devices**：枚举所有当前会话设备，按已授权电脑名寻找 Online ID。不能先按保存的旧 ID 检查，也不能因旧 ID 离线就转 A。
2. 对当前在线的 C 设备 **ping + 无副作用 PowerShell 命令** 验证目标电脑。若同名多实例，逐一核查并唯一确定；不能判断则停止报告。
3. C 真实执行验证 PASS ⇒ **锁定 C**；严格禁止走 A/B。
4. C 发现/验证失败 ⇒ 重新动态发现、**限一次有界重试**；仍明确失败并保存证据才能 A，A 也失败才能 B。UNKNOWN 不能自动算作 FAIL。
5. 每个新任务重新进行动态发现，历史路由不继承。切换遵循 Exactly-once 和安全检查点。
6. 保存最小审计：任务、时间、设备列表、当前 ID、ping、真实业务探针、降级原因。
7. 不得更改 FlClash、代理、Windows 网络配置、登录浏览器、密钥、隧道。

## 与《三人行》第3版关系
凡由《三人行》第3版或其他执行体系请求 Windows 执行，都必须先读取本入口和 V10.0 权威规则。本文件不擅自改变《三人行》方法版本指针。

## 验收与版本声明
2026-10-18 C 通道已真实验证：动态发现在线 ID、ping pong、PowerShell 返回目标主机名及桌面存在。**GitHub 保存与回读不等于所有外部执行器自动加载**；跨会话规则加载及故障转移仍须独立验收。
