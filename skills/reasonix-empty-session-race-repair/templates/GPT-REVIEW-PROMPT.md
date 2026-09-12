# GPT 补丁复核模板

你是本任务唯一的核心分析/补丁决策者。

请基于 Codex 提供的：

- 版本/commit
- 复现条件
- 成功/失败会话对照
- 后端 empty-state 源码测试
- 前端 navigation/controller ready 时序
- 最小补丁 diff
- 已执行测试

严格输出：

```text
PATCH_REVIEW_DECISION=APPROVE 或 REVISE
ROOT_CAUSE_AGREEMENT=YES 或 NO
PATCH_SCOPE=FRONTEND_ONLY / BACKEND_REQUIRED / OTHER
DEPLOYMENT_AUTHORIZED=YES 或 NO
REQUIRED_CHANGES=<无则 NONE>
RATIONALE=<简洁技术结论>
```

禁止：

- 把 Codex 当根因决策者。
- 用“清缓存/重装”替代已确认根因修复。
- 没有证据时扩大到用户数据。
