# Changelog

## 1.1.0 - 2026-09-18

- 改为 `CODEX_FIRST_NUMBERED_GITHUB_BUS` 架构。
- Codex 成为唯一常驻主动循环；GPT 改为按需 planner/judge。
- GitHub 成为编号化不可变命令/结果总线和唯一业务事实源。
- AI Browser 从长文本搬运器降为 GPT wakeup/ACK transport。
- GPT 被唤醒后直接读 GitHub 请求并直接写下一条编号消息。
- 新增六位单调消息序号、ACTION_ID、LAST_CONSUMED_SEQ、DO_NOT_REPEAT 与并发冲突规则。
- Shadow Pilot 升级为 v2：Codex 000001 → GPT 000002 → Codex 000003 → GPT 000004。

## 1.0.0 - 2026-09-17

- 初始 GPT/Codex 双向自动 transport、GitHub共同工作区、checkpoint/idempotency 与 capacity-router 设计。