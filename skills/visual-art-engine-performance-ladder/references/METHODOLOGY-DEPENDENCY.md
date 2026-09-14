# Methodology Dependency

- Skill ID: `mature-replication-four-column`
- Required method: `First-Principles Four-Column Method V4.0`
- Required metadata version: `4.0.0`
- Installed path: `C:\Users\A\.codex\skills\mature-replication-four-column`
- Entrypoint SHA-256 at v1.0.0 integration: `3813A15C3493A4446E9362E6E61238412EB8F395BD65727C540AF4F19F263D32`
- Source-definition SHA-256 declared by V4.0 acceptance: `37ABD8CA203975B41568DFCB1F6A8A507B9452D9013ABD2E4751FDE4A097320B`

运行任何性能阶段前必须读取该正式 `SKILL.md`，并在需要工作表时读取其 `references/four-column-worksheet.md`。本技能只调用和映射，不复制为第二套方法，也不得修改依赖技能。

若技能缺失、版本不是 4.0.0、四列名称不一致或依赖哈希发生未审计变化，返回 `METHODOLOGY_DEPENDENCY=FAIL`，禁止进入优化。
