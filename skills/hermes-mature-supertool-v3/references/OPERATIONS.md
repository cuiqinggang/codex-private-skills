# 安装、排障与复验

## 本机入口

| 入口 | 打开方式 | 适用场景 |
|---|---|---|
| Windows 命令行 | 在 PowerShell 运行 `hermes --cli`。需要全屏文字终端时运行 `hermes --tui` | 手工命令、脚本、批量和重复任务 |
| Dashboard 网页终端 | 复用 `http://127.0.0.1:9119/chat?profile=default`。需要启动 Dashboard 时运行 `hermes dashboard --host 127.0.0.1 --port 9119 --no-open` | 查看控制面板、诊断和在浏览器中使用文字终端 |
| Webapp 图形聊天 | 复用专用 Chrome 已登录的 `9120` 标签。需要重开时运行 `hermes webapp` | 口述、手工聊天、看历史、加附件 |

PowerShell 找不到 `hermes` 时，用已安装的 `& "$env:LOCALAPPDATA\hermes\bin\hermes.exe"` 代替命令名。使用当前 `default` Profile 和 Flash 1017。

### 图形聊天登录与恢复

- 首选现有已登录标签，可在该标签刷新。新标签打开裸地址会显示登录说明。用官方启动命令获取一次性登录，链接仅可使用一次，有效期 60 秒。沿用当前专用 Chrome，避免写出或分享一次性链接。
- 如果系统默认浏览器和专用 Chrome 分开，确认正在运行的专用 Chrome 程序路径与用户数据目录（本机实测为 `shared-mcp`）。只给当前 PowerShell 进程设 `BROWSER`，命令格式为 `"<Chrome程序路径>" "--user-data-dir=<现有数据目录>" --new-tab %s`。当前 Chrome 已指定 `--profile-directory` 时一并保留。运行官方启动器后恢复该环境变量，验证原专用 Chrome 的新标签已进入图形消息框。已确认前端构建可用时用 `hermes webapp --skip-build`。
- 排障先用 `hermes webapp --status`。首次启用时核对 `9120` 空闲和回环绑定，先校验 `config.yaml` 备份。缺前端时运行 `hermes webapp --build-only`，再运行 `hermes config set webapp.enabled true`。确认网关空闲后运行 `hermes gateway restart`。复验 `8642/health`、`9120` 页面、已登录的图形消息框和一条真实回复。日常打开时直接走启动器。
- 网关故障沿用官方启动器和现有健康检查。涉及安装或恢复时先核对实际运行版本、官方发布、现有目录和备份。验收读取 HTTP、WebSocket RPC 和真实任务回执。

### 鼠标语音与效率

- 这类鼠标语音输入法通常把转写文字交给当前获得焦点的输入控件。Webapp 有普通可编辑的消息框。Dashboard 的 `/chat` 用 xterm.js 把输入转换为发给终端进程的字符流，内部用隐藏文本控件接收输入。某些输入法整段提交或替换文字时会与该机制不兼容。上游有类似报告，本机的结论以用户实测为准。
- 口述时把光标放在 Webapp 底部消息框，再按平时的鼠标语音键。遇到输入问题，分别检查中文键入、鼠标听写和真实收发。用户的鼠标输入法与 Hermes 内置听写按钮分开记录。
- 固定任务可用 `hermes chat --oneshot --query-file .\task.txt`，减少点击，便于批处理。口述、附件和会话切换优先图形版，减少人工操作。模型生成速度需用同模型、同任务、同工具和上下文做对照，计入输入、执行、核对和返工。

[官方 CLI（v0.22.7）](https://github.com/NousResearch/hermes-agent/blob/v0.22.7/website/docs/reference/cli-commands.md) · [官方图形工作区（v0.22.7）](https://github.com/NousResearch/hermes-agent/blob/v0.22.7/website/docs/user-guide/desktop.md) · [Dashboard 聊天实现（v0.22.7）](https://github.com/NousResearch/hermes-agent/blob/v0.22.7/web/src/pages/ChatPage.tsx) · [xterm.js 输入法兼容报告](https://github.com/xtermjs/xterm.js/issues/6012)

## 网页与角色验收

1. 使用无敏感内容的隔离任务，记录任务号、工作项、预期产物和计时口径。
2. 用正式工具集运行 `browser_exec`。v0.22.7 的工具可见性依赖 `terminal`。在受控网页验打开、填表、单次提交和读回，由服务端日志和会话工具事件对账。
3. 经平台获准的入口向指定 GPT 网页派单。等实际完成，沿原会话读回回复或生成物，核对标记和结果。提交状态不明时先只读对账。Work Browser 的站点拒绝只说明该自动化入口受限。
4. 用 [固定的 ECC 3.1.1](https://github.com/cuiqinggang/ecc-v3.1.1/tree/b9e651bc6c6751bff43db30b80d9cab983a7c412) 跑引擎及冷恢复。业务试验中控制、资料、执行、审计各有可追溯上下文。仅执行者写约定产物，独立审计读取冻结合同及证据。核对实际文件操作，包含缓存和临时目录。
5. 同一回执记录模型、角色、耗时、错误、恢复、产物哈希和独立验收。失败时先定位最小原因，再复验受影响的功能。

[官方 Windows 安装说明](https://hermes-agent.nousresearch.com/docs/user-guide/windows-native) · [Hermes 原生浏览器说明](https://hermes-agent.nousresearch.com/docs/user-guide/features/browser)
