# 回滚操作指南

## 如何回滚

1. 查看所有快照：
```bash
ls -la ~/.hermes/skills/productivity/overseas-ai-region-setup/snapshots/
cat ~/.hermes/skills/productivity/overseas-ai-region-setup/snapshots/snapshot_*.json
```

2. 读取初始快照，逐项恢复：
   - IP → 切回跑跑云原节点
   - 时区 → 恢复为 Asia/Shanghai
   - 浏览器语言 → 恢复为 zh-CN
   - 系统区域 → 恢复为 CN
   - WebRTC → 恢复默认
   - Billing Address → 恢复原设置

3. 无法自动恢复的项（需手动）：
   - IP切换（需在Clash中操作）
   - OpenRouter Billing Address（需在OpenRouter网站操作）
   - 指纹浏览器配置（需在AdsPower中操作）

## 快照命名规则

```
snapshot_YYYYMMDD_HHMMSS.json
```

每次修改前必须创建新快照。初始快照标记为 `INITIAL_`。
