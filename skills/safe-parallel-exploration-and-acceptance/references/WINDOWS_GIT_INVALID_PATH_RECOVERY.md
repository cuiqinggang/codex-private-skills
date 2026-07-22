# Windows Git 非法路径恢复策略

## 先审计，后 checkout

使用 `scripts/git/get-git-runtime-context.ps1` 判定实际 Git 上下文，再用 `scripts/git/audit-windows-git-paths.py` 审计目标 ref。不得把空 `.git` 当作有效仓库。

审计命中尾随空格、尾随点、Windows 保留设备名、非法字符或控制字符时，普通 checkout/worktree 必须阻断。`--no-checkout` 和 sparse checkout 不是可靠绕过方案。

## 隔离恢复

`scripts/git/create-windows-safe-isolated-worktree.ps1` 只用于已经确认存在 Windows 非法路径的仓库：

1. 解析并记录基线 commit。
2. 可选创建本地保护标签。
3. 生成空树的无父提交。
4. 创建本地隔离分支和 C 盘工作树。
5. 再次确认基线 ref 未变化。

隔离分支没有原历史的祖先关系，不得自动 merge、push 或替代原主线。需要恢复的文件必须经过清单、哈希和人工批准后选择性导入。
