# Worktree Readiness

检查仓库、HEAD、主工作区、分支/路径冲突、秘密风险、嵌套仓库、异常 worktree 记录和项目是否以大型素材为主体。

额外强制检查：

- `.git` 是否只是空/损坏标记。
- 当前上下文是 worktree 还是 bare repository。
- 目标 Git tree 是否包含 Windows 尾随空格/点、保留名、非法字符或控制字符。
- 锁定资产是否声明 `-text` 并有 SHA-256 清单。
