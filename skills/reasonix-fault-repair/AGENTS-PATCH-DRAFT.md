# AGENTS.md Patch Draft

仅作为候选，不自动覆盖全局 `AGENTS.md`：

```markdown
## Reasonix 空会话竞态复用

出现“新建零消息会话偶发加载历史失败、发第一条消息后恢复”、`ready=false` 或 `workspace-not-ready` 时，优先读取 `C:\Users\A\.codex\skills\reasonix-fault-repair\cases\empty-session-race.md`。先确认 active build、hotfix 哈希和 controller-ready/hydration 顺序；不得默认删库、清缓存或同版本重装。
```
