# Case B — Reasonix 启动 readiness 超时 / startup_timeout

## 1. 症状

用户可见错误：

```text
Reasonix could not finish startup or update.
startup_failed: startup was not verified within 30 seconds
```

以及：

```text
Startup incomplete / 启动未完成
startup_timeout
Reasonix did not become ready within 30 seconds.
```

关键日志目录：

```text
C:\Users\A\AppData\Roaming\reasonix\desktop-shell\logs
```

## 2. 本次诊断结果

版本：`v1.38.7`

诊断结论：

```text
PRIMARY_CATEGORY=C. CORE_READY_BUT_SHELL_MISDETECTED
SECONDARY=D. STARTUP_TOO_SLOW
```

后端已经启动且 Ready，故障发生在 Electron Shell / Renderer / native-host 生命周期握手阶段。

首次失败证据：

```text
19:43:41 backend ready
19:43:52 desktop/domReady timeout
19:43:58 / 19:44:01 window native-call timeout
19:44:02 rendererAttached timeout
随后迟到响应被记录为 orphan-response
19:44:04 shell readiness timeout
```

总失败时间：

```text
launcher = 31.224s
shell = 31.259s
backend ready = shell + 7.791s
```

## 3. 已排除

- backend 未启动；
- backend crash；
- SQLite 损坏；
- updater / manifest / latest.json 本次阻塞；
- 版本指针不一致；
- TCP 端口冲突；
- 重复 Reasonix 实例；
- Windows Application Error；
- 空会话热修复缺失或哈希漂移。

SQLite：

```text
quick_check=ok
```

Updater：

```text
DISABLED_BY_CONFIG
```

通信方式：

```text
--host-rpc 标准输入输出通信
```

因此无 LISTENING_PORTS 属正常现象。

## 4. 空会话热修复一致性

当次空会话修复包哈希仍为：

```text
5C5C6C26DA638680F63533CFC9A234A38F327697C8D1967ED3BEB4681A131447
```

说明本次启动故障不应直接归因于既有空会话补丁。

## 5. 受控冷启动验证

第一次冷启动：

```text
COLD_START_1=PASS
BACKEND_READY=2524ms
DOM_READY=3643ms
RENDERER_ATTACHED=6241ms
APP_USABLE=9836ms
TIMEOUT_SEEN=NO
LATE_RECOVERY=NO
```

第二次冷启动：

```text
COLD_START_2=PASS
BACKEND_READY=2344ms
DOM_READY=3377ms
RENDERER_ATTACHED=5122ms
APP_USABLE=6601ms
TIMEOUT_SEEN=NO
LATE_RECOVERY=NO
```

最终分类：

```text
RESULT=TRANSIENT_COLD_START_ANOMALY
PATCH_NEEDED=NO
```

## 6. 发现但暂不修的设计弱点

```text
TIMEOUT_BUDGET_INVERSION=YES
LATE_RESPONSE_VALID=YES
```

解释：

1. backend 已 Ready，但整体 readiness 仍依赖 domReady / native-call / rendererAttached；
2. 内层生命周期等待与外层 launcher 30 秒 deadline 可能存在预算倒置；
3. 请求超时后 pending entry 可能被清理；
4. 同一启动代次中的合法迟到生命周期响应随后被记录为 orphan-response；
5. 这会把“仍在正常初始化”错误升级为“启动失败”。

但由于随后两次冷启动完全正常，本次不修改代码。

## 7. 为什么不直接把 30 秒改成 60 秒

粗暴延长 timeout 只能掩盖竞态，不能修复状态机语义。

若未来稳定复现，正确方向应为：

- backend alive + backend ready + renderer 有真实进展时保持 STARTING；
- fatal IPC / renderer crash / process exit 立即 FAILED；
- 当前 startup generation 内的 late-but-valid lifecycle response 可以更新 readiness；
- 外层 deadline 与内层 timeout 使用统一 budget；
- 允许合理 grace period，但不能无限等待。

## 8. 复发门槛

一次出现后，通过完整退出 + 两次冷启动恢复：

```text
TRANSIENT_COLD_START_ANOMALY
NO_CODE_CHANGE
```

一次成功一次失败：

```text
INTERMITTENT_READINESS_RACE
```

同类故障连续两次冷启动均复现：

```text
DETERMINISTIC_READINESS_BUG
```

只有第三种情况才重新进入代码补丁设计。

## 9. 不得执行

默认禁止：

- 重装；
- 清 AppData；
- 删除数据库；
- 修改代理；
- 回滚空会话补丁；
- 删除 lock 而未确认进程归零；
- 为规避错误大范围增加 timeout。

## 10. 本案例最终状态

```text
FINAL_STATUS=PASS
CURRENT_STATE=HEALTHY
PATCH_APPLIED=NO
REGRESSION=2/2_PASS
ROOT_CAUSE_CLASS=TRANSIENT_COLD_START_ANOMALY
REOPEN_CONDITION=SAME_READINESS_FAILURE_REPRODUCED_TWICE
```
