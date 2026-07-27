# Cursor 3.13.10 + Claude Code + DeepSeek V4 Pro 完整恢复流程

## 1. 适用场景

当用户出现以下任一情况时读取本文件：

- 桌面“Cursor 中文编辑器”打开后找不到 Claude Code 或 New Agent；
- Cursor 顶部菜单恢复成英文；
- Claude Code 能中文回答，但页面看不出实际模型；
- 需要证明 Claude Code 工具外壳走的是 DeepSeek V4 Pro，且绝不连接 Claude/Anthropic 官方模型；
- Cursor 升级后需要恢复经典菜单中文化；
- 用户要求实际打开、截图、两轮任务回答和模型可见证明。

触发关键词：`Cursor 中文编辑器`、`Claude Code 找回来`、`DeepSeek V4 Pro`、`模型看不出来`、`顶部菜单英文`、`Cursor 3.13.10 中文化`、`两轮截图验证`。

## 2. 2026-07-27 实测环境

- Windows 10
- Cursor `3.13.10`
- Claude Code CLI `2.1.179`
- Cursor 扩展 `anthropic.claude-code-2.1.220-win32-x64`
- 官方 DeepSeek Anthropic-compatible endpoint：`https://api.deepseek.com/anthropic`
- 主模型：`deepseek-v4-pro[1m]`
- Haiku/轻量子代理：`deepseek-v4-flash`
- Cursor 工作区：用户指定目录
- 最终结论：
  - `Claude Code 工具外壳 DeepSeek V4 Pro 转接路线: PASS`
  - `ACTUAL_OPEN_VERIFY_PASS`

## 3. 先复用，不要重建

开工前依次检查：

1. 本技能和 `references/BOUNDARY-20260702.md`；
2. `claude-code-cursor-super-tool-predeploy`；
3. `cursor-kilo-supertool-mature-stack` 的菜单中文化与失败复盘；
4. `ui-setting-actual-open-self-verify-loop`；
5. `computer-use-visual-recovery` 和 `screenshot`。

不得扫描 H/K 盘；C 盘正式副本缺失时停止并报告。

## 4. 环境和版本 Gate

只读检查：

```powershell
& "$env:APPDATA\npm\claude.cmd" --version
Get-ChildItem "$env:USERPROFILE\.cursor\extensions" -Directory |
  Where-Object Name -like 'anthropic.claude-code*'
(Get-Item "$env:LOCALAPPDATA\Programs\cursor\Cursor.exe").VersionInfo.FileVersion
```

PowerShell 执行策略可能阻止 `claude.ps1`；Windows 下优先调用 `claude.cmd`，不要把执行策略错误误判为 Claude Code 未安装。

## 5. DeepSeek-only 安全会话启动

优先运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File `
  ".\scripts\launch-cursor-deepseek-session.ps1" `
  -WorkspacePath "C:\path\to\workspace" `
  -OutputRoot "C:\path\to\evidence"
```

脚本行为：

1. 用 `Read-Host -AsSecureString` 读取 DeepSeek Key；
2. Key 只写入当前 PowerShell/Cursor 进程树：

```text
ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
ANTHROPIC_AUTH_TOKEN=<session only>
ANTHROPIC_MODEL=deepseek-v4-pro[1m]
ANTHROPIC_DEFAULT_OPUS_MODEL=deepseek-v4-pro[1m]
ANTHROPIC_DEFAULT_SONNET_MODEL=deepseek-v4-pro[1m]
ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek-v4-flash
CLAUDE_CODE_SUBAGENT_MODEL=deepseek-v4-flash
CLAUDE_CODE_EFFORT_LEVEL=max
```

3. 启动 Cursor 前执行：

```powershell
claude.cmd -p "只回复：DS_CLAUDE_CODE_OK"
```

4. 退出码必须为 `0`，输出必须包含 `DS_CLAUDE_CODE_OK`；
5. 通过后生成不含 Key 的 `DeepSeek-V4-Pro-当前会话路由证明.md`；
6. 启动 `Cursor.exe --classic --locale zh-cn --new-window <workspace>`；
7. 自动在 Cursor 打开路由证明。

禁止把 API Key、SecureString 明文、环境变量转储或进程环境转储写入报告或 Git。

## 6. 恢复 Claude Code 页签

Cursor 中可用命令：

- `Claude Code: Open`
- `Claude Code: Open in New Tab`
- `Claude Code: Focus Input`
- `Claude Code: New Conversation`

优先用 F1 打开命令面板并输入 `Claude Code: Open`。如果截图已经显示顶部 `Claude Code` 页签和底部 `Ask Claude to edit...` 输入框，不要重复打开。

窗口自动化必须：

1. 用 `Get-Process Cursor` 找到非零 `MainWindowHandle`；
2. 按句柄聚焦 Cursor；
3. 截图时使用 `take_screenshot.ps1 -WindowHandle <handle>`；
4. 每执行一个动作就重新截图确认；
5. 输入中文时可临时使用剪贴板，但应保存并恢复原文本剪贴板，且不得粘贴秘密。

## 7. Cursor 3.13.10 顶部菜单中文化

Cursor 更新会覆盖 `resources\app` 下的工作台资源。3.13.10 中菜单结构由旧版 `mnemonicTitle:S(...)` 变化为 `mnemonicTitle:C(...)` 风格，旧脚本不能直接假定仍匹配。

运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File `
  ".\scripts\repair-cursor-313-classic-menubar-cn.ps1" `
  -OutputRoot "C:\path\to\evidence\cursor-menubar-cn"
```

硬门禁：

1. Cursor 版本必须严格等于 `3.13.10`；
2. File/Edit/Selection/View/Go/Terminal/Help 每项原始签名必须恰好匹配一次；
3. 写入前备份：
   - `out\vs\workbench\workbench.desktop.main.js`
   - `product.json`
4. 替换七项菜单为中文 Unicode 签名；
5. 重新计算工作台 JS SHA-256，以 Base64 无填充格式写回 `product.json`；
6. 每项中文签名必须恰好出现一次；
7. 任一门禁失败立即停止，不能扩大正则或盲改资源。

更新后彻底关闭并重开 Cursor。截图必须看到：

`文件(F) / 编辑(E) / 选择(S) / 查看(V) / 转到(G) / 运行(R) / 终端(T) / 帮助(H)`

Cursor 再次升级后必须重新检查版本和签名；不要直接复用 3.13.10 脚本到未知版本。

## 8. 为什么 Claude Code 页面看不到 DeepSeek 模型

Claude Code Cursor 扩展页头显示的是工具外壳名称 `Claude Code`，不会显示自定义 Anthropic-compatible endpoint 的模型名。底部 `Manual` 是权限模式，不是模型名称。

因此禁止把以下内容作为唯一模型证据：

- 页面标题；
- 模型自己回答“我是 DeepSeek”；
- 只看环境变量配置；
- 只看用户口述。

正确证据必须合并：

1. 同一启动链路的安全路由记录；
2. Cursor 启动前 `claude -p` 的真实返回；
3. Cursor 内实际中文任务回答；
4. 第二轮 `Read` 工具读取路由证明。

把路由证明在 Cursor 中与 Claude Code 面板并排打开，使同一截图同时显示：

- `https://api.deepseek.com/anthropic`
- `deepseek-v4-pro[1m]`
- `DS_CLAUDE_CODE_OK`
- `Claude/Anthropic 官方模型：未启用`
- Claude Code 的实际中文回答

## 9. 两轮实际任务验收

第一轮示例：

```text
请用简体中文完成一次实际任务：列出3条验证 Cursor 中文菜单和 Claude Code 中文回答是否正常的检查结果。最后单独一行输出：DEEPSEEK_V4_PRO_中文回答_OK
```

通过标准：

- 中文回答非空；
- 包含三项检查结果；
- 最后一行包含 `DEEPSEEK_V4_PRO_中文回答_OK`；
- 截图同时显示 Claude Code 页签和中文顶部菜单。

第二轮示例：

```text
请读取当前打开的“DeepSeek-V4-Pro-当前会话路由证明.md”，只用简体中文回答其中记录的实际 API 端点、实际主模型、最小真实调用返回，以及 Claude/Anthropic 官方模型是否启用。最后单独一行输出：ROUND2_DEEPSEEK_ROUTE_FILE_READ_OK
```

通过标准：

- 页面显示真实 `Read` 工具调用；
- 返回四个正确字段；
- 输出 `ROUND2_DEEPSEEK_ROUTE_FILE_READ_OK`；
- 截图中路由证明与回答同时可见。

## 10. 2026-07-27 真实证据

- 资源修复报告：七项 `pass=true`，`overall_pass=true`
- 备份目录：`cursor-app-resources-20260727-185759`
- 真实烟雾测试时间：`2026-07-27T19:06:27+08:00`
- 真实烟雾测试：退出码 `0`，返回 `DS_CLAUDE_CODE_OK`
- 第一轮标记：`DEEPSEEK_V4_PRO_中文回答_OK`
- 第二轮标记：`ROUND2_DEEPSEEK_ROUTE_FILE_READ_OK`
- 截图：
  - `assets/evidence/round1-answer.png`
  - `assets/evidence/round1-route-proof-visible.png`
  - `assets/evidence/round2-answer-and-route-proof.png`

## 11. 回滚

菜单修复失败时：

1. 彻底关闭 Cursor；
2. 从本次 `backup\cursor-app-resources-<timestamp>` 按原相对路径恢复两个文件；
3. 重开 Cursor；
4. 截图确认英文原始状态或恢复状态；
5. 不删除备份，不修改 Kilo/Claude/DeepSeek/API Key/网络配置。

会话启动失败时只关闭该 PowerShell 和其启动的 Cursor；Key 未持久化，不需要清理注册表。

## 12. 下次开工前检查

使用 `references/CHECKLIST-CURSOR-CLAUDE-DEEPSEEK-20260727.md`。先确认版本、端点官方文档和旧失败记录，再做任何写入。
