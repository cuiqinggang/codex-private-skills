# UltraFusion V9 运行复盘：可执行经验

1. `.git` 存在不等于 Git 仓库。必须以 `git rev-parse --is-inside-work-tree` 和 `--is-bare-repository` 判定运行上下文。
2. checkout、sparse checkout 和 `--no-checkout` 都不能保证绕过 Windows 非法路径。执行 worktree/checkout 前先审计 Git tree。
3. 遇到历史树含 Windows 非法路径时，保留远端或 bare 仓库为只读证据；建立本地保护标签后，创建无父提交的 Windows-safe 隔离分支/工作树。该分支不能自动合并主线。
4. 被哈希锁定的提示词、命令包和基线资产必须使用 `.gitattributes` 的 `-text`，并比较源文件、工作副本和 staged Git blob 的 SHA-256。
5. 只读资产的破坏性测试只能修改独立沙箱副本；复制后如继承只读属性，只能清除副本属性，不能改源文件。
6. 测试脚本必须自校验脚本根路径，禁止依赖错误的 `Path.parents[n]` 推断。
7. 安装在技能目录的正式副本可以不是 Git 仓库；应使用安装副本哈希、静态测试和运行时测试验收，不得仅因无 `.git` 判失败。
8. `git diff --check` 对锁定资产的历史尾随空格/CRLF 只能作为提示，不得自动格式化；真值是清单与哈希。
9. 中文 PowerShell/Python/JSON 交互必须显式 UTF-8。
10. 修复后必须完成候选版、集成副本、正式安装后三层复测；任一层失败均不得宣布完成。
