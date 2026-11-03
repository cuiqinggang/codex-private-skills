# 错误、避错与恢复

## 本次成功路径的适用边界

起点是已有 Tor 窗口显示“连接 Tor 网络”，点击后完成连接。没有复现 V3 的持续失败。
本轮没有修改 FlClash、代理、torrc 或重新安装；不能认定已根治所有历史网络故障。

## 本次工具层真实错误

| 现象 | 原因或证据 | 已采用修正 |
|---|---|---|
| D 命令以 & 开头报语法错误 | 此处命令入口按 cmd 解释 | 直接调用带引号的 PowerShell 7 路径 |
| stdio 请求含中文后出现 surrogate / UnicodeEncodeError | Windows 客户端默认文本编码与输入不匹配 | stdin/stdout 显式 UTF-8；跨通道 JSON 用 ensure_ascii=true |
| CallToolResult 没有 isError 属性但响应成功 | 本机 SDK 使用 Python 字段 is_error，序列化别名 isError | 从 model_dump(by_alias=true) 兼容读取错误字段；本机复验退出 0 |
| Type 报 Either loc or label must be provided | 未传入目标字段位置 | 当前画面确认地址栏后传 loc 或 label |
| App 英文名称切到 Chrome 聊天窗口 | Chrome 标题也包含 Tor Browser | 使用精确中文名，截图复核前台身份 |
| UI tree 500 元素被截断，Tor 未列入 | 多窗口桌面造成无关内容占满默认树 | 单显示器或 region；只需看图时 use_ui_tree=false；勿全量扫描无关窗口 |
| 点击回执成功但预期界面没有变化 | 回执只能证明点击发出；可能焦点、遮挡或用户移动 | 重新截图确认窗口与目标后再操作，不盲重试整批 |
| 官网已有标题但正文空白 | 本轮继续等待后正文出现 | 保留加载中状态，直到正文实际显示再报 PASS |

## Tor 连接错误的顺序

1. 看当前原生连接状态；已有“已连接”就验证检测页，不擅自改配置。
2. 若连接失败，读取错误与 Tor 日志：设置 → 连接 → 高级 → 查看 Tor 日志。记录关键错误，删去凭据和无关隐私。
3. 仅只读核对现有网络依赖、本地监听和时钟；没有新授权不更改 FlClash、系统代理、DNS、防火墙、服务、启动项或计划任务。
4. V3 历史独立 Tor 的 HTTPSProxy 127.0.0.1:7890 / SOCKS 9251 成功，只是历史条件；不得自动把该配方写进浏览器 torrc。
5. 不把 Tor 启动命令中的 DisableNetwork 1 单独当根因；浏览器有自己的连接管理，须结合当前 GUI 与实际网页判断。
6. 不使用被拒绝的内部控制或认证接口。新的平台明确拒绝也不通过另一路重试绕过。
7. 保持“独立实例 / Tor Browser / 官方 HTTPS / 浏览器 onion / 传输 / 重启”分项状态。

## D 暂不可用

先按现行 Windows 执行桥处理。云端不能直接调用 windows-mcp-v1 时，只说明原生工具未暴露；不能假称已经看见桌面。
配置启用不等于会话已连接。临时 D 地址改变时，按既有快捷恢复方法更新连接；不创建新隧道或暴露桌面服务。
写入或点击无回执先核对界面状态；不盲重发已完成动作。

## 官方资料

- 首次连接与自动连接：https://support.torproject.org/tor-browser/getting-started/first-launch/
- 连接问题与 Tor 日志：https://support.torproject.org/tor-browser/encountering-issues/troubleshooting/
- 官方连接检测：https://check.torproject.org/
- 官方网站：https://www.torproject.org/
- 官方 onion 地址目录：https://onion.torproject.org/

官方排障中可能包含重装或系统操作；本用户明确禁止的动作仍不执行。
