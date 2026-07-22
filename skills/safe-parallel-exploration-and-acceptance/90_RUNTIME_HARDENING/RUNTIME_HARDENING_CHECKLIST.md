# 运行时加固验收清单

- [x] PowerShell 和 Python 语法检查通过。
- [x] 空 `.git` 被识别为 `BROKEN_GIT_MARKER`。
- [x] 正常 worktree、bare repository、非 Git 目录均能正确分类。
- [x] 合法 Git tree 的 Windows 路径审计为 `PASS`。
- [x] 尾随空格/点、保留名和非法字符能阻断 checkout/worktree。
- [x] Windows-safe 隔离恢复不改变基线 ref，且只创建本地分支/标签。
- [x] `core.autocrlf=true` 时，带 `-text` 的锁定资产保持精确字节。
- [x] 缺少 `-text` 导致字节漂移时测试必须失败。
- [x] 只读沙箱可注入修改，源资产哈希前后不变。
- [x] 非 Git 安装副本可通过安装副本验收。
- [x] 原有三轮验收全部通过。
- [x] 候选版、集成副本、正式安装副本分别复测。
- [x] 验收页人工检查并保存截图。
- [x] ZIP 清单和 SHA-256 已生成。
