# Hermes Gateway Watchdog 全面排查报告

**时间**: 2026-05-22 16:15 CST  
**目的**: 发送给 GPT 重新制定执行计划

---

## 一、当前状态（实时检测结果）

| 项目 | 状态 | 详情 |
|------|------|------|
| Gateway | ✅ **正常** | PID 13924，16:01 启动，health返回 `{"status":"ok"}` |
| Watchdog | ❌ **已死亡** | 最后日志 15:49，进程已不存在 |
| Mutex锁 | ❌ **FREE** | `Local\HermesGatewayWatchdog8642_v3` 无人持有 |
| 进程数 | ⚠️ | Gateway相关有3个进程(PID 14496/16460/13924) |

**结论：Gateway 在裸奔，没有任何守护进程保护它。**

---

## 二、已修复的Bug（确认有效）

### Bug 1: `$LogDir` 未初始化 → 🔧 已修复
- **原代码**: `$LockFile = "$LogDir\watchdog-8642.pid"` 在第16行，但 `$LogDir` 在第38行才定义
- **后果**: 锁文件路径变为 `\watchdog-8642.pid`（根目录，无效）
- **修复**: 将所有路径定义移到锁代码之前（第11-17行）
- **状态**: ✅ 已修改到 `C:\Users\A\Hermes_AutoStart\HermesGatewayWatchdog.ps1`

### Bug 2: `Global\` Mutex 需管理员权限 → 🔧 已修复
- **原代码**: `$MutexName = "Global\HermesGatewayWatchdog8642"`
- **后果**: 普通用户无 `SeCreateGlobalPrivilege`，Mutex创建静默失败 → 零防范
- **修复**: 改为 `$MutexName = "Local\HermesGatewayWatchdog8642_v3"`
- **测试**: 已验证，第二个实例正确输出 "MUTEX BLOCKED" 并退出
- **状态**: ✅ 已修改

---

## 三、新发现的关键问题

### ⛔ 问题1: 两代Watchdog同时运行（互锁失效）

**根本原因**: v1脚本使用 `Global\HermesGatewayWatchdog8642`（需要admin），v2脚本使用 `Local\HermesGatewayWatchdog8642_v3`。两者的Mutex名称**不同**，所以互锁完全失效。

**证据** — watchdog-8642.log 同一时间段出现两个独立的失败计数：
```
14:23:50 *** Port 8642 NOT LISTENING (failure #53)   ← v1旧脚本的计数
14:23:50 FATAL: Reached MaxFail=10                     ← v1
14:24:19 *** Port 8642 NOT LISTENING (failure #1)     ← v2新脚本的计数
14:24:19 Grace period: sleeping 10s                    ← v2
14:24:23 *** Port 8642 NOT LISTENING (failure #54)    ← v1
14:24:23 FATAL: Reached MaxFail=10                     ← v1
```

**后果**: 两个watchdog竞争同一端口，可能互相误杀。资源浪费。

### ⛔ 问题2: Watchdog 自身崩溃/退出

**现象**: v2 watchdog (PID 12856) 在运行1.5小时后（14:23→15:49），累计203次失败后消失。脚本使用 `while($true)` 且 `$ErrorActionPreference='Continue'`，理论上不应退出。

**可能原因**:
- PowerShell 宿主进程崩溃
- 资源泄漏（203次 `Get-NetTCPConnection` + `Invoke-WebRequest` 调用）
- 被外部进程杀死

**后果**: **Watchdog 没有守护者**。它死了就死了，Gateway 在裸奔。

### ⛔ 问题3: 恢复失败——PID 19184 秒死

**日志证据**:
```
14:24:31 +++ Initiating recovery (failure #1)
14:24:32 === Launching Hermes Gateway ===
14:24:32 Launched PID 19184
14:24:39 Gateway PID 19184 did not become healthy within 120s  ← 仅7秒!
```

**关键发现**: `StartupTimeout=120s`，但实际只等了7秒。原因是 `Wait-GatewayHealthy` 内部的进程检测发现 PID 19184 已退出，立即break了循环。**PID 19184 完全不存在于 `gateway-exit-diag.log` 中**，说明它可能连 atexit hook 都没执行就直接崩溃了。

**推测**: hermes.exe 启动时遇到了某种致命错误（比如端口已被占用？配置文件损坏？），但没有任何诊断日志。

### ⚠️ 问题4: 启动项体系碎片化

存在三套独立的启动机制，且互不协调：

| 机制 | 路径 | 状态 |
|------|------|------|
| Startup文件夹 .cmd | `Hermes_Gateway.cmd` → `Hermes_NewAPI_AutoRecover.cmd` | ✅ 启用 |
| 计划任务 | `HermesGatewayWatchdog_Logon` | ❌ **禁用** |
| 计划任务 | `HermesNewApiAutoRecover_Logon` | ❌ **禁用** |

`Hermes_Gateway.cmd` 的内容只是简单转发：
```
@echo off
call "C:\Users\A\.hermes\gateway-service\Hermes_NewAPI_AutoRecover.cmd"
```

而 `Hermes_NewAPI_AutoRecover.ps1` 是一个独立的恢复脚本（有它自己的Mutex: `Local\HermesNewApiAutoRecover`），和 watchdog 不是同一个东西。

### ⚠️ 问题5: 多个 gateway 进程并存

当前 Gateway 有 3 个进程 (PID 14496/16460/13924)，进程树可能源于 hermes.exe → python 的层级关系，但需要确认是否是 `--replace` 未正确清理旧进程。

**diag.log 曾记录双 Gateway 竞态**:
```
03:05:07 gateway.start pid=18360
03:05:08 gateway.start pid=21812   ← 仅差1秒
03:05:09 asyncio.run.returned pid=21812 success=false
```
这说明当两个 Gateway 几乎同时以 `--replace` 启动时，第二个会失败。

---

## 四、Watchdog 脚本剩余隐患（代码层面）

即使修复了 Mutex 和路径问题，当前脚本仍有设计缺陷：

1. **无自身守护**: Watchdog 死了没人重启它
2. **无持久化机制**: 只依赖手动启动，没有计划任务/服务化
3. **$failCount 无上限**: 理论上会一直累加（已到203），可能触发整数溢出或日志膨胀
4. **恢复失败后降级不足**: 恢复失败只是 `$inRecovery = $false`，下次循环可能再次尝试但可能无限失败
5. **Gateway启动后健康检查等待** (Wait-GatewayHealthy) 如果进程先退出会立即返回，不会等待120秒

---

## 五、已完成的修复 vs 待解决问题

### ✅ 已解决
- Mutex 路径依赖问题（$LogDir 顺序）
- Global→Local Mutex 权限问题
- 单实例锁已验证可用

### ❌ 未解决（需GPT重新规划）
1. Watchdog 自身崩溃恢复机制
2. 两代脚本互锁冲突
3. Gateway 启动秒死诊断（PID 19184 无日志）
4. 启动项体系整合（三套机制选一套）
5. 端到端验证（模拟 Gateway 崩溃 → 观察恢复）
6. 重启后持久化验证

---

## 六、关键文件路径

| 文件 | 路径 |
|------|------|
| Watchdog脚本 | `C:\Users\A\Hermes_AutoStart\HermesGatewayWatchdog.ps1` |
| Watchdog日志 | `C:\Users\A\.hermes\logs\watchdog-8642.log` |
| Gateway诊断日志 | `C:\Users\A\.hermes\logs\gateway-exit-diag.log` |
| Hermes配置 | `C:\Users\A\.hermes\config.yaml` |
| Startup .cmd | `C:\Users\A\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Hermes_Gateway.cmd` |
| NewAPI恢复脚本 | `C:\Users\A\.hermes\gateway-service\Hermes_NewAPI_AutoRecover.ps1` |
| PID锁文件 | `C:\Users\A\.hermes\logs\watchdog-8642.pid` |
| Mutex名称 | `Local\HermesGatewayWatchdog8642_v3` |
| Gateway地址 | `http://127.0.0.1:8642` |

---

## 七、建议 GPT 重新规划的方向

1. **合并启动体系**: 只保留一个入口（计划任务或服务），清理 Startup 文件夹和旧 cmd
2. **Watchdog 自愈**: 要么用 Windows 服务（自动重启），要么外部再套一层 watchdog-of-watchdog
3. **完善恢复逻辑**: 限制重试次数 + 冷却时间 + 告警通知
4. **诊断 Gateway 秒死**: 需要抓取 PID 19184 的 stderr 输出
5. **端到端测试**: 先做完整一轮模拟故障→恢复验证
