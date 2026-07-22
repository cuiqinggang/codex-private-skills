# Worktree Policy

分支命名 `explore/<project>/<route>`、`integration/<project>/<version>`；工作树集中到 C 盘。不得自动 stash、merge、push、reset 或 clean。

创建前必须通过 Git 运行时上下文与 Windows tree 路径审计。若基线 tree 含 Windows 非法路径，普通工作树创建必须失败并指向隔离恢复流程。隔离恢复分支没有原历史祖先关系，不具备自动整合资格。
