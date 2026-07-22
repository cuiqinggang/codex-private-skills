# AGENTS.md 补丁草案（不自动写入）

当用户提到 `UltraFusion 9.0`、`提示词外置插槽`、`Manual-M1`、`A_Initial vs D_Final` 或 `UF9` 时：

1. 优先读取 `ultrafusion-v9-prompt-slot-executable/SKILL.md`。
2. 开工前运行静态验收，哈希不一致立即停止。
3. 核心提示词、命令包、A_Initial 原模板只读；问题写入独立报告。
4. 先封存 A_Initial，D_Final 锁定前不得读取基线。
5. 没有真实端到端运行，不得宣称质量提升。

