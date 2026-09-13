# Reasonix 故障决策树

## 入口

### A. 新建空会话后历史加载失败

若满足：

- 新建会话；
- 零消息；
- 偶发加载失败；
- 发第一条消息后恢复；
- SQLite quick_check 正常；

优先匹配 `cases/empty-session-race.md`。

不要先删库、重装、清缓存。

### B. 程序启动时报 startup_timeout / startup_failed

若出现：

```text
startup was not verified within 30 seconds
Reasonix did not become ready within 30 seconds
```

按顺序检查：

1. backend 是否启动；
2. backend 是否 ready；
3. domReady 是否完成；
4. rendererAttached 是否完成；
5. native-call 是否 timeout；
6. 是否出现 orphan-response；
7. updater 状态；
8. SQLite quick_check；
9. 是否重复进程；
10. 是否端口冲突或 IPC 异常。

如果 backend 未 Ready：重新诊断，不套用 readiness 竞态结论。

如果 backend Ready，但 renderer 生命周期超时：进入 Case B。

## Case B 分类

### 两次冷启动均正常

```text
TRANSIENT_COLD_START_ANOMALY
PATCH_NEEDED=NO
```

### 一次成功一次失败

```text
INTERMITTENT_READINESS_RACE
```

先做最小源码定位，不立即扩大修改。

### 两次均失败，且时间线一致

```text
DETERMINISTIC_READINESS_BUG
```

允许进入 readiness 代码补丁设计。

## Readiness 补丁门

只有满足以下证据时才补：

- backend 已 Ready；
- renderer/native-host 仍有真实进展；
- 外层 deadline 先于内层生命周期完成；
- late response 属当前 startup generation；
- 同类失败可重复。

补丁目标：

- progress-aware STARTING；
- late-but-valid lifecycle response 可接纳；
- 统一 timeout budget；
- fatal 条件立即失败；
- 不无限等待。

## 默认停止条件

以下操作必须有明确证据与批准：

- 重装；
- 升降级；
- 删除数据库；
- 清整个 AppData；
- 修改代理；
- 大范围覆盖 app.asar；
- 回滚已验收空会话补丁。
