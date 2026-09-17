# GPT-Codex Convergence Orchestrator v1.1.0

当前架构：`CODEX_FIRST_NUMBERED_GITHUB_BUS`。

- Codex：唯一主动循环与确定性执行器。
- GPT：按需规划器/裁决器，不轮询、不常驻。
- GitHub：编号化不可变命令/结果总线与唯一事实源。
- AI Browser：只负责唤醒 GPT 与接收短 ACK，不搬运长业务正文。
- Capacity Router：处理 Codex 模型容量故障，不重放已完成本地工作。

正式协议：`references/CODEX-FIRST-NUMBERED-BUS-v1.md`。

Shadow Pilot：`docs/h3-p0/20260917-mature-convergence-v2/H3-P0-GPT-CODEX-AUTOMATION-PILOT-COMMAND-v2.md`。
