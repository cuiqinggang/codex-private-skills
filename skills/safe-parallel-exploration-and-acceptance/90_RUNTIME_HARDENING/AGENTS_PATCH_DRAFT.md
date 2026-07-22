# AGENTS.md 补丁草案

## Windows Git 与锁定资产硬门禁

- 不得用 `Test-Path .git` 判断仓库有效性；使用 Git plumbing 判定 worktree、bare、broken marker 或 non-git。
- 在 Windows 上执行 checkout/worktree 前，先审计目标 Git tree 是否含尾随空格/点、设备保留名、非法字符或控制字符。
- 历史树含 Windows 非法路径时，不反复尝试 checkout；使用 bare 证据仓库和 Windows-safe 隔离分支恢复，保留基线 ref，禁止自动合并主线。
- 哈希锁定资产使用 `.gitattributes -text`，同时核验工作副本和 staged blob 的 SHA-256。
- 破坏性测试只修改沙箱副本；源文件只读属性和哈希必须保持不变。
- 修复现有技能后，至少完成候选副本、集成副本和正式安装副本三层测试；未全部通过不得标记完成。
