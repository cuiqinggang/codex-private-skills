# Failure Review

记录每次失败的假设、修改、测试、根因、可保留部分、禁止重复的方法、替代方向和工作树清理资格。没有真实失败时保留此入口，不伪造条目。

## 2026-07-11

- 失败：直接用 Windows PowerShell 管道向 Hook Python 进程传含中文路径的 JSON，子进程未收到可解析 UTF-8，错误回退到当前目录。
- 修复：使用 Python `subprocess.run(..., encoding='utf-8')` 发送 JSON；route-a 正确 allow，route-b 正确 block。
- 规则：跨 PowerShell/Python 传中文 JSON 时显式声明 UTF-8，不以控制台默认编码做验收。
- 失败：主线准入建议脚本在输出父目录不存在时写入失败。
- 修复：写入前显式创建输出父目录。
- 规则：所有报告脚本必须创建受控父目录，再写文件。
- 失败：中文菜单直接写入 UTF-8 BOM `.cmd` 后，`cmd.exe` 出现乱码并把部分文本误当命令。
- 修复：`.cmd` 改为纯 ASCII 启动器，中文菜单迁移到 UTF-8 BOM PowerShell；增加 `-Choice` 非交互自检。
- 规则：Windows 中文复杂菜单使用 PowerShell 承载，批处理只做 ASCII 转发。
- 失败：4 个工作树摘要以秒级时间命名，同一秒内发生覆盖，只留下 3 份。
- 修复：归档名加入工作树 slug 和毫秒时间戳。
- 规则：多路线并行证据文件名必须包含路线/工作树标识，时间戳不能是唯一去重字段。

## 2026-07-12 — UltraFusion V9 首次真实运行

- 失败：桌面目录存在空 `.git`，仅用 `Test-Path .git` 被误判成有效仓库。
- 修复：新增 Git 运行时上下文检测，以 `git rev-parse` 区分 `WORKTREE`、`BARE_REPOSITORY`、`BROKEN_GIT_MARKER`、`NOT_GIT`。
- 规则：文件系统标记只能作为线索，不能替代 Git plumbing。
- 失败：历史 Git tree 含 `TESTS/Q3_V15_MetaOpt ` 尾随空格目录，Windows 普通 clone checkout 失败；`--no-checkout` 和 sparse checkout 仍不能可靠解决。
- 修复：checkout/worktree 前先审计 Git tree；命中 Windows 非法路径后，使用 bare 证据仓库、本地保护标签和无父提交隔离分支建立 Windows-safe 工作树。
- 规则：隔离分支无原历史祖先关系，只能作为恢复/重建区，禁止自动 merge 或 push 到主线。
- 失败：Git `core.autocrlf` 可能改变哈希锁定的提示词与命令包字节。
- 修复：锁定资产登记 `.gitattributes -text`，比较源文件、工作副本和 Git index blob 的 SHA-256。
- 规则：锁定资产不得为通过格式检查而自动改换行、BOM、尾随空格或编码。
- 失败：只读违规测试用 `shutil.copy2` 后，沙箱副本继承只读属性，导致测试不能注入修改。
- 修复：只清除沙箱副本的只读属性，注入后验证源文件哈希前后不变。
- 规则：破坏性测试永远不直接修改源资产，也不得改变源只读属性。
- 失败：测试脚本用错误的 `Path.parents` 层级定位脚本目录。
- 修复：使用显式技能根参数和存在性自校验。
- 规则：测试路径推断必须先验证目标入口确实存在。
- 失败：正式技能副本不在 Git 中，被 Git-only 验收误判为不可验证。
- 修复：安装副本使用安装清单、文件哈希、静态测试和运行时测试验收；Git 上下文只影响 Git 功能，不影响技能有效性判断。
- 规则：部署检查与源码仓库检查是两种契约，不能混为一谈。
- 结论：本轮修复只有在候选、集成、正式安装后三层实测全部通过后才能记录为成功复用。
