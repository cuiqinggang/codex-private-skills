# SHARED REPOSITORY RULE（共同仓库制度）

`SHARED_WORKSPACE_REPOSITORY=cuiqinggang/codex-private-skills`

本仓库是本项目 GPT、Codex 与其他执行智能体的共同事实源、共同办公区和长期版本库。关键资料不得只存在本机 C 盘。

## 默认读取入口

1. fetch / pull 共同仓库最新 `main`。
2. 读取 `skills/absolute-time-fireworks-optimization/SKILL.md`。
3. 读取 `references/CURRENT-STATE.md`。
4. 读取 `references/FAST-PATH.md`。
5. 异常时才读取 `references/FAILURE-INDEX.md`。
6. 审计、复盘或升级时才读取完整 EVIDENCE / HISTORY（证据与历史）。
7. 阶段成果同步共同仓库。

## 必须同步的事件

- `NEW_BEST（新的最好成绩）`
- `NEW_FAILURE（新的失败经验）`
- `NEW_FAST_PATH（新的成熟最短路径）`
- `METHOD_CHANGE（方法变化）`
- `ROOT_CAUSE_FOUND（找到根因）`
- `99_REOPEN（99 重新开启）`
- `NEW_99_FREEZE（新的 99 冻结）`

同步内容不仅是结论，还包括影响复现或决策的命令、代码、脚本、配置、原始结果、错误输出、根因、修复、版本、SHA、报告、技能更新与进度账。

## 边界

- 性能关键路径只负责快；同步发生在 `RESULT_READY` 后或阶段结束后。
- 禁止上传密钥、认证正文、浏览器登录数据或无关私人文件。
- 不 force push，不删除旧技能、Measurement V2 或历史证据。
- C 盘正式副本用于执行；H 不读写；K 仅在用户对当次备份明确授权后使用。
