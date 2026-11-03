# 云端到 Windows 与 Tor 连接步骤

## 1. 组件映射

| 名称 | 本次作用 | 已证事实 |
|---|---|---|
| D 插件：Windows D 20261103-01 | 让云端在用户 Windows 执行已授权命令 | 本会话 open_workspace、exec_command、write_stdin 成功 |
| windows-mcp-v1 | 本机桌面查看、窗口切换、点击、输入 | 本机 Codex 配置中已注册，实际 stdio 调用成功 |
| 本机 Codex | 现有 MCP 配置的持有者 | 配置文件含对应服务器项；本轮未使用 Codex CLI 运行模型 |
| Tor Browser | 用户现有浏览器及自带 Tor 网络客户端 | 本轮在已有窗口点击连接，两个官方网页通过 |

插件命名带日期数字只表示本轮实际入口。下次动态发现当前有效 D 插件，不照搬已经失效的插件名称或临时网址。
连接 D 的恢复按现行 Windows 执行桥执行，优先复用活跃连接；不保存 Owner 令牌或临时公网地址到此包。

## 2. 先检查工具是否直接可用

- 查找 windows-mcp-v1 的 Snapshot、App、Click、Type、Shortcut 等工具。
- 若原生已暴露，直接使用；先 Snapshot，再操作。
- 若云端未暴露，而本机已配置：使用已连通 D 作为传输，读取本机配置中仅对应 windows-mcp-v1 的非敏感项。
- 不把“工具未暴露”描述为插件断线，也不要求重新安装已经可用的工具。

本轮读取到的配置节选（本机已验证，不表示所有电脑相同）：

```toml
[mcp_servers.windows-mcp-v1]
command = 'C:\AI\Windows-MCP-V1\.venv\Scripts\python.exe'
args = ["-m", "windows_mcp", "serve", "--transport", "stdio"]
startup_timeout_sec = 45
```

配置文件：C:\Users\A\.codex\config.toml。
本机组件说明：C:\AI\Windows-MCP-V1\VERSION_V1.md；当时登记 Windows-MCP 0.8.7 / Python 3.14.5。
本机曾登记 127.0.0.1:8766/mcp，但本轮没有使用或验收该 HTTP 服务，不要把它当云端公网地址。

## 3. 经 D 复用已配置的 MCP stdio 服务

1. 没有可复用 workspace_id 时，对已授权的工作目录调用 D 的 open_workspace；读取其返回的 AGENTS。已有同目录 workspace_id 就复用。
2. 先核对当前 D 的命令宿主。此次 Windows D 20261103-01 实际接受 cmd 风格：在该宿主中直接调用带引号的 PowerShell 7 路径，不在前面加 &。这是本次入口的事实，不能推广为所有 D 插件的 shell 规则；若当前入口为 Git Bash 或 PowerShell，按对应引号、路径与调用语法执行。
3. 脚本必须先保存到 Windows 上的实际 V4 目录；云端 /root 路径不会自动出现在本机。只用现有 Python ≥3.11、现有 mcp SDK，截图压缩使用现有 Pillow，不安装新依赖。在本机用原虚拟环境 Python 启动随包脚本。下面是本次 cmd 宿主的一次性验证示例；换宿主时先调整调用语法：

```text
C:\AI\Windows-MCP-V1\.venv\Scripts\python.exe "<V4包路径>\scripts\windows_mcp_session.py" --config "C:\Users\A\.codex\config.toml" --server-cwd "C:\AI\Windows-MCP-V1" --tool DisplayInventory
```

4. 先 --list-tools 核对当前工具名与 schema。DisplayInventory 和显示器 [1] 都只是本轮已观察例子，不保证别的设备相同。多次操作使用 --interactive。脚本只启动已配置的 windows-mcp-v1 stdio 子进程，不修改配置、不开放端口。
5. 等待 MCP_READY 后再按行发送 ASCII JSON；中文可写成 JSON 的 Unicode 转义。输入输出显式 UTF-8。每行一个请求，等待上一请求结果并核对后再决定下一次操作。
6. 若 D 返回 session_id，通过原 write_stdin 接续；不要重新启动整批。首次加载曾耗时数十秒，running 不等于失败。脚本继承配置 startup_timeout_sec 限制初始化；超时是连接错误。工具调用中断或无回执必须先核对效果，不能盲重发副作用操作。
7. 结束输入 EXIT，仅结束本轮客户端及其拥有的 MCP 子进程；Tor Browser 保持打开。

交互请求例：

```json
{"name":"Snapshot","arguments":{"use_vision":true,"use_annotation":false,"use_ui_tree":false,"display":[1]}}
{"name":"App","arguments":{"mode":"switch","name":"Tor \u6d4f\u89c8\u5668"}}
```

示例两行是不同请求，不是要求盲发一批。先阅读 Snapshot，再执行窗口切换；每个依赖操作都读取返回值。
界面工具的实时 schema 以 list_tools 为准；脚本支持 --list-tools，保留原配置的 enabled_tools / disabled_tools 限制。退出码 0 表示至少一次成功调用且无工具错误；退出码 1 表示有错误；空交互会话返回 2，不作验收成功。

## 4. 把截图真正回传给云端查看

D 只返回文本；必须把 MCP 的 image 内容还原为图片后查看，不能看见 base64 或 Screenshot 文本回执就说已看到桌面。
脚本默认将图片转为 JPEG（宽度最多 1280），返回实际缩放前后尺寸；需要原图时传 --image-max-width 0。

云端代码模式按以下方式处理本轮协议（示意，D 工具名和会话号使用当前实际值）：

```javascript
// D read/poll 的文本位于 result.structuredContent.result。
// 每个 MCP_RESULT= 后是一整行 JSON；跨次 poll 的不完整行先缓存，补齐后再解析。
for (const line of completeLines) {
  if (!line.startsWith("MCP_RESULT=")) continue;
  const response = JSON.parse(line.slice("MCP_RESULT=".length));
  for (const block of response.content || []) {
    if (block.type === "image") image(block);
    if (block.type === "text") text(block.text);
  }
}
```

- 本轮实际对截图读取使用 max_output_tokens=60000，并在代码层解析后只输出图片和必要文字，未把 base64 原文打印给用户。
- 若返回 output_truncated=true 或 JSON 尚不完整，不能据此点击。先区分分段与截断：分段可续读原会话并拼完整行；截断不能靠拼后续行修复。
- 截断时，对纯只读截图可在当前允许的有限重试内缩小 region 或将图片宽度调低再取图；不重放点击等副作用请求。
- 截图可能包含其他窗口的私人信息，只供当前内部检查，不上传到共同工作区或作为报告附件。
- image(block) 必须由支持图像的云端工具上下文实际执行；若当前宿主只能读文本，报告图像查看能力缺口，不假称已验收桌面。

## 5. 识别桌面和 Tor 窗口

本轮设备有三块显示器：
- 显示器 0：(-3840,-189) 到 (0,1971)。
- 显示器 1：主屏 (0,0) 到 (2560,1440)。
- 显示器 2：(2560,0) 到 (4480,1080)。

这些是本轮快照，不作为以后固定坐标。先查看当前显示布局。
全桌面图像可能缩放；点击坐标必须换算为虚拟桌面真实像素，并考虑裁剪原点及额外图片缩放。
优先准确 UI 元素或窗口名；只有当前画面已确认时才使用坐标。不要复制本轮“连接”按钮坐标到下一台电脑。

App(mode="switch", name="Tor Browser") 曾选中标题含 Tor Browser 的 Chrome 聊天窗口。
改用精确中文名“Tor 浏览器”并看图确认，或在已观察的任务栏选择 Tor 窗口。
不要只凭 App 的成功回执断言已切对窗口。

已有程序位置：
C:\Users\A\Desktop\Tor Browser\Browser\firefox.exe。
这里只说明已有软件的位置，技能包本身不存到桌面。
程序未运行时才使用 App(mode="launch_executable", executable=<已核对路径>)，避免第二份实例。

## 6. 点击连接

1. 看见原生“连接 Tor 网络”页面后，点击“连接”。
2. 若“始终自动连接”已经开启，保持现状；本轮它已开启，但页面仍需一次实际点击。
3. 观察“正在建立连接”→“已连接”→新标签页，期间先等待并观察，不能把进度条当作最终成功。
4. 本轮截图在点击约 3 秒后显示建立连接，随后追加 10 秒观察显示已连接；这是离散观察窗口，不是精确连接耗时，不能据此报告 T_VALID。

## 7. 分别验证两项

1. Tor Browser 中 Ctrl+L；Type 必须传 loc 或 label，clear=true，输入 https://check.torproject.org/ 并 press_enter=true。
2. 若出现是否请求英文网页的首次提示，本轮选择“否”，保留原语言偏好。这不是网络报错。
3. 看见绿色 Congratulations. This browser is configured to use Tor.，才记录浏览器使用 Tor 的检测 PASS。
4. Ctrl+T 新开第二标签，访问 https://www.torproject.org/，等正文渲染。标题出现而正文空白时先继续观察，不能提前报官网 PASS。
5. 本轮官网在 8 秒快照中仍为空白，追加 10 秒观察后中文正文已显示。不是精确网页加载耗时。
6. 保留两个标签作为现场核对入口。普通浏览器或云端能打开官网不能代替本机 Tor Browser 的测试。

## 8. 新任务如何继承状态

current-state.json 与验收表是历史快照；新任务仍要取得当前桌面与两个网页证据。只继承安装和旧工程的证据范围，不能继承未来网络一定可用。

## 9. 错误与恢复

连接失败时转 references/troubleshooting.md。
不要自动重装、重启电脑、更换 FlClash 配置或启停代理。
不要把历史 9151 控制端口、9150 SOCKS、9251 独立实例混在一起。
正常关闭并重开 Tor、整机重启、浏览器 onion 与外部传输均是独立验收；本轮文档升级不执行这些动作。
