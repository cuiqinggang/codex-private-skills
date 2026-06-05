---
name: hermes-watchdog-修复失败总结
description: >
  Hermes Gateway Watchdog 自动恢复机制修复的完整失败记录。
  尝试修复 Mutex 单实例锁、启动项冲突、Gateway 自动拉起等问题，
  最终因 Watchdog 自身崩溃、两代脚本互锁失效、Gateway 启动秒死等原因未能完成。
  保留此记录以避免未来重复踩坑。
category: devops
version: 1.0
created: 2026-05-22
updated: 2026-05-22
tags:
  - watchdog
  - gateway
  - 失败总结
  - 自动恢复
  - mutex
  - powershell
  - windows
---

# Hermes Gateway Watchdog 修复失败总结

## 目标

让 Hermes Gateway（端口 8642）具备持久化自动恢复机制：Gateway 崩溃后 Watchdog 自动拉起，且保证单实例运行不冲突。

## 失败的修复过程

### 阶段一：发现并修复 Mutex Bug（✅ 成功但不够）

**Bug 1 — $LogDir 未初始化导致锁文件路径错误**
- 脚本中 `$LockFile = "$LogDir\watchdog-8642.pid"` 在第16行执行时 `$LogDir` 尚未定义
- 导致锁文件写入根目录 `\watchdog-8642.pid`，完全无效
- 修复：将所有路径定义移到锁代码之前

**Bug 2 — Global\ Mutex 需要管理员权限**
- 原代码 `$MutexName = "Global\HermesGatewayWatchdog8642"`
- 普通用户无 `SeCreateGlobalPrivilege`，Mutex 创建静默失败
- 修复：改为 `$MutexName = "Local\HermesGatewayWatchdog8642_v3"`

### 阶段二：运行验证中暴露新问题（❌ 连锁失败）

**问题 1 — 两代 Watchdog 同时运行**
- v1 使用 `Global\HermesGatewayWatchdog8642`（需要admin，静默失败）
- v2 使用 `Local\HermesGatewayWatchdog8642_v3`（加了 `_v3` 后缀）
- **Mutex 名字不同，互锁完全无效**，两个 Watchdog 竞争同一个 8642 端口
- 日志出现两个独立的失败计数（#1 vs #53）交替记录

**问题 2 — Watchdog 自身崩溃退出**
- v2 Watchdog（PID 12856）运行 1.5 小时后，累计 203 次失败后消失
- `while($true)` 循环 + `$ErrorActionPreference='Continue'` 理论上不该退出
- 推测：PowerShell 宿主进程崩溃或资源泄漏
- **致命后果：Watchdog 没有守护者，死了就死了，Gateway 在裸奔**

**问题 3 — Gateway 恢复启动秒死**
```
14:24:31 +++ Initiating recovery (failure #1)
14:24:32 Launched PID 19184
14:24:39 Gateway PID 19184 did not become healthy within 120s  ← 仅7秒!
```
- `StartupTimeout=120s`，但只等了 7 秒（进程已退出）
- PID 19184 **在 gateway-exit-diag.log 中完全无记录**，说明 atexit hook 都没执行
- 直接崩溃，死因不明

**问题 4 — 启动项体系碎片化**
- Startup 文件夹 `.cmd` → 转发到另一个 `.ps1`（有自己的 Mutex，和 Watchdog 不同）
- 计划任务 `HermesGatewayWatchdog_Logon` → **禁用**  
- 计划任务 `HermesNewApiAutoRecover_Logon` → **禁用**
- 三套独立的启动机制，互不协调，不知道到底谁启动谁

### 阶段三：端到端验证（❌ 未能执行）

计划人为 Kill Gateway 观察 Watchdog 恢复行为，但因为 Watchdog 已经自己死了，无法进行。

## 根本原因分析

1. **PowerShell 不是可靠的守护进程运行时** — 长时间运行会崩溃，没有自愈能力
2. **Mutex 方案在普通用户 Windows 环境脆弱** — Global vs Local 语义差异、名称冲突
3. **Hermes 自身 Gateway 启动不稳定** — PID 19184 秒死说明 Hermes 在某些条件下无法正常启动
4. **碎片化的启动体系** — 缺乏统一的进程管理入口

## 残留状态（2026-05-22）

| 项目 | 状态 |
|------|------|
| Gateway | ✅ 正常运行（无守护） |
| Watchdog | ❌ 已死亡 |
| Mutex | 空闲 |
| 启动项 | 碎片化，计划任务均禁用 |

## 避免重复踩坑的教训

1. **不要在 PowerShell 中实现长期守护进程** — 用 Windows Service 或 NSSM 包装
2. **Mutex 名称不要随意加后缀** — 改名前确保旧实例已被清理
3. **任何守护进程必须有守护者的守护者** — 嵌套监督或服务自动重启
4. **启动 Gateway 前先确保 `--replace` 能正确清理旧进程**
5. **失败次数必须设上限 + 冷却退避 + 告警**，不能无限循环

## 相关文件

| 文件 | 路径 |
|------|------|
| Watchdog 脚本 | `C:\Users\A\Hermes_AutoStart\HermesGatewayWatchdog.ps1` |
| Watchdog 日志 | `C:\Users\A\.hermes\logs\watchdog-8642.log` |
| Gateway 诊断 | `C:\Users\A\.hermes\logs\gateway-exit-diag.log` |
| Startup cmd | `C:\Users\A\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Hermes_Gateway.cmd` |
| 全量备份 | `H:\_FULL_RECOVERY_Hermes_Windows_Native_014_20260520` |
