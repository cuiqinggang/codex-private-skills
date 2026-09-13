# Reasonix 故障复发处置手册

## 1. 启动故障 startup_timeout

出现以下错误时：

```text
startup_failed
startup_timeout
startup was not verified within 30 seconds
Reasonix did not become ready within 30 seconds
```

按以下流程执行：

```text
保存失败现场
↓
读取 desktop-shell/logs
↓
确认 backend_started / backend_ready
↓
确认 domReady / rendererAttached / native-call / orphan-response
↓
检查 updater / SQLite / 重复进程 / 版本指针
↓
确认当前空会话 hotfix SHA256
↓
完整结束当前 Reasonix 进程树
↓
确认 Reasonix 进程数=0
↓
等待约5秒
↓
正常冷启动，计时至少60秒
↓
再次完整退出并第二次冷启动
```

### 分类

两次 PASS：

```text
TRANSIENT_COLD_START_ANOMALY
NO_CODE_CHANGE
```

一 PASS 一 FAIL：

```text
INTERMITTENT_READINESS_RACE
```

两次同类 FAIL：

```text
DETERMINISTIC_READINESS_BUG
```

此时重新打开最小 readiness 补丁设计。

## 2. 空会话加载失败

若零消息新会话偶发“历史加载失败”，优先检查：

```text
visible tab 已创建？
controller ready？
hydration 是否早于 ready？
Transcript/History 是否在 ready=false 时被调用？
```

已知成熟修复：

```text
waitForTabReady
↓
navigationCompletionCurrent
↓
loadSessionDataForTab
```

不得把 zero-message session 本身当成数据损坏。

## 3. 固定证据目录建议

```text
C:\AI\Reasonix-<Issue>-<Date>\
  before\
  logs\
  evidence\
  backup\
  after\
```

至少保存：

- 版本号；
- 进程树；
- 日志；
- SQLite quick_check；
- updater 状态；
- SHA256；
- 修改前后 diff；
- 冷启动时间线；
- 验收结果。

## 4. 永久禁止默认绕过

没有直接证据时不要：

- 重装；
- 清空 AppData；
- 删除数据库；
- 修改系统代理；
- 修改 FlClash；
- 回滚已验收补丁；
- 删除历史会话；
- 无限延长启动 timeout。
