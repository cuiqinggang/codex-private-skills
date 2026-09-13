# Reasonix 故障修复验收门

## 通用验收

- 当前版本与版本指针一致。
- 关键文件修改前后 SHA-256 已保存。
- SQLite 只读 `quick_check=ok`，除非故障证据明确指向数据库。
- 不修改系统代理、FlClash 或 Windows 网络设置。
- 所有写入前有备份，可回滚。

## 空会话竞态验收

至少要求：

```text
QUICK_NEW_SESSION_TEST >= 10/10 PASS
ZERO_SESSION_FIRST_OPEN >= 30/30 PASS
RAPID_NAVIGATION_ERROR_COUNT=0
FIRST_MESSAGE_TRANSITION=PASS
ZERO_SESSION_RESTART >= 10/10 PASS
OLD_SESSION_REGRESSION >= 5/5 PASS
```

## 启动 readiness 故障验收

受控恢复阶段至少：

```text
COLD_START_1=PASS
COLD_START_2=PASS
startup_timeout=NO
startup_failed=NO
```

记录：

- backend_ready_ms
- dom_ready_ms
- renderer_attached_ms
- app_usable_ms

如果两次冷启动都通过，则默认：

```text
PATCH_NEEDED=NO
CURRENT_STATE=HEALTHY
```

## 如果实施 readiness 补丁

必须追加：

1. backend ready 仍可快速确认；
2. renderer/native-host 正常慢启动时不会被过早判死；
3. fatal renderer crash/IPC error 仍立即失败；
4. late-but-valid 生命周期响应只接受当前 startup generation；
5. 不接受旧 renderer / 旧 correlation 的迟到响应；
6. 连续冷启动至少 5/5 PASS；
7. 新建空会话回归仍 PASS；
8. 旧会话加载 PASS。
