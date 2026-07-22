# Git Local Policy

Git 用于本地版本历史和差异追踪；GitHub 是可选远程，本技能不自动创建远程或 push。

- 仓库有效性必须由 `git rev-parse` 判断，不得仅检查 `.git`。
- 支持识别普通 worktree、bare repository、broken `.git` marker 和 non-git。
- Windows checkout/worktree 前必须审计目标 tree 的路径兼容性。
- 历史 tree 含 Windows 非法路径时，停止普通 checkout，按 `references/WINDOWS_GIT_INVALID_PATH_RECOVERY.md` 隔离恢复。
- 哈希锁定资产使用 `-text` 和 staged blob SHA-256 验收。
