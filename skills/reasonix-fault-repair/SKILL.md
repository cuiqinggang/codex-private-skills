---
name: reasonix-fault-repair
version: 1.0.0
chinese_name: Reasonix 故障诊断与成熟修复
summary: 统一收录 Reasonix 已验证故障案例、诊断路径、最小修复策略、验收门与复发处置。当前包含空会话 hydration/ready 竞态与启动 startup_timeout/readiness 竞态两类成熟案例。
tags:
  - reasonix
  - troubleshooting
  - startup-timeout
  - readiness-race
  - empty-session
  - hydration-race
  - electron
  - renderer
  - codex
  - gpt-review
  - protective-repair
---

# Reasonix 故障诊断与成熟修复

## 1. 目标

本技能不是“某一个补丁”，而是 Reasonix 故障修复统一入口。遇到 Reasonix 异常时，优先搜索本技能，先匹配成熟案例，再决定是否需要新诊断。

固定原则：

1. 先保存成功态与失败现场，再修。
2. 先排除数据库、更新器、网络、版本指针、重复进程等基础原因，再进入代码层。
3. 不因为报错文案相似就把不同故障混为一类。
4. 只修真正根因，避免清缓存、重装、删库等扩大修改面操作。
5. GPT 负责根因判断和补丁范围；Codex 负责本机检索、修改、测试、备份和部署。
6. 所有写入动作前备份并回读；成功态恢复后，不为“理论完美”扰动当前可用系统。

## 2. 当前已验证成熟案例

### Case A：新建空会话偶发“加载会话历史失败”

入口：`cases/empty-session-race.md`

核心根因：

```text
EnsureBlankSurface / EnsureBlankTab
        ↓
visible tab 已返回，但 controller ready=false
        ↓
前端提前 loadSessionDataForTab
        ↓
TranscriptSnapshotForTab -> workspace-not-ready
        ↓
UI 映射为“历史加载失败”
```

最终修复：前端 hydration 在 controller ready 前禁止读取会话数据；等待 `waitForTabReady` 后再加载。

已验证热修复 SHA-256：

```text
5C5C6C26DA638680F63533CFC9A234A38F327697C8D1967ED3BEB4681A131447
```

状态：`PASS / RUNTIME_ACCEPTANCE_PASS`

### Case B：Reasonix 启动时报 startup_timeout / startup_failed

入口：`cases/startup-readiness-timeout.md`

本次最终分类：

```text
TRANSIENT_COLD_START_ANOMALY
```

失败现场核心时间线：

```text
backend ready
  ↓
desktop/domReady timeout
  ↓
window native-call timeout
  ↓
rendererAttached timeout
  ↓
迟到生命周期响应被记录为 orphan-response
  ↓
shell readiness timeout
  ↓
launcher ~31s 判定 startup_failed
```

关键判定：

- backend 实际已 Ready；
- SQLite quick_check=ok；
- updater 非根因；
- 无端口冲突；
- 无重复实例证据；
- 空会话补丁哈希未漂移；
- 后续两次完整冷启动均 PASS；
- 因此当次不打代码补丁。

两次恢复验证：

```text
RUN1 backend_ready=2524ms dom_ready=3643ms renderer_attached=6241ms app_usable=9836ms
RUN2 backend_ready=2344ms dom_ready=3377ms renderer_attached=5122ms app_usable=6601ms
```

同时发现潜在设计弱点：

```text
TIMEOUT_BUDGET_INVERSION=YES
LATE_RESPONSE_VALID=YES
```

但只有在同类 readiness 失败连续两次可复现时，才重新打开代码补丁设计。

状态：`PASS / HEALTHY / NO_PATCH_REQUIRED`

## 3. 快速路由

出现以下现象时：

### 新建空会话失败，但发第一条消息后恢复

优先匹配 Case A。

### 启动窗口显示：

```text
startup_failed
startup_timeout
startup was not verified within 30 seconds
Reasonix did not become ready within 30 seconds
```

优先匹配 Case B。

第一步不是重装，而是确认：

```text
backend_started?
backend_ready?
domReady?
rendererAttached?
orphan-response?
SQLite quick_check?
updater state?
duplicate process?
```

## 4. 启动故障复发时的固定处理顺序

```text
保留失败现场
↓
确认版本与补丁哈希
↓
读取 desktop-shell logs
↓
确认 backend 是否 Ready
↓
确认 renderer/domReady/native-host 握手
↓
确认 updater / SQLite / 重复进程 / 端口
↓
完整结束 Reasonix 失败进程树
↓
确认进程数=0
↓
等待约5秒
↓
正常冷启动并计时至少60秒
```

如果恢复：

```text
TRANSIENT_COLD_START_ANOMALY
NO CODE CHANGE
```

如果一次失败一次成功：

```text
INTERMITTENT_READINESS_RACE
```

如果连续两次均复现：

```text
DETERMINISTIC_READINESS_BUG
```

此时才允许进入最小 readiness 补丁设计。

## 5. 禁止默认操作

除非证据明确支持，不得默认：

- 重装 Reasonix；
- 升级/降级；
- 清整个 AppData；
- 删除 SQLite；
- 重建历史会话；
- 修改系统代理或 FlClash；
- 回滚已验收空会话补丁；
- 把所有 timeout 粗暴改成 60/120 秒；
- 删除 lock 文件而未先确认相关进程已退出。

## 6. Readiness 设计原则

若未来 Case B 稳定复现，补丁应遵循：

```text
backend alive + backend ready + renderer handshake 有进展
        ↓
保持 STARTING，不直接 FAILED
```

生命周期迟到响应若仍属于当前 startup generation / renderer / correlation，应作为 `late-but-valid lifecycle response` 接纳，而不是简单丢为 orphan。

外层 launcher deadline 与内层 domReady/native-call/rendererAttached timeout 必须统一预算，避免 timeout budget inversion。

## 7. 证据与验收

每次修复至少保存：

- 版本号；
- 进程树；
- 关键日志；
- SQLite quick_check；
- updater 状态；
- 关键文件 SHA-256；
- 修改前后 diff；
- 冷启动时间线；
- 回归结果。

详见：

- `DECISION-TREE.md`
- `ACCEPTANCE.md`
- `RECURRENCE-RUNBOOK.md`
- `cases/empty-session-race.md`
- `cases/startup-readiness-timeout.md`
