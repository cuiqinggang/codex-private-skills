---
name: onion-network-superpowers
description: 连接和验证用户已有的 Tor Browser，复用 D 通道与本机 windows-mcp-v1 完成 Windows 桌面查看、点击、输入及错误诊断。用户提到洋葱网络超能力、V4、Tor 未连接、云端控制本机或归档 Tor 连接方法时使用；保留 V3 历史与独立 Tor、浏览器、onion、传输、重启各自的验收边界。
---

# 洋葱网络超能力 V4.0

版本：4.0.0。日期：2026-11-03（北京时间）。设备：DESKTOP-4A1EGTM。
目标：在现有安装和现有网络条件下完成连接，保留可复用步骤与真实证据。

## 最短执行顺序

1. 确认用户任务范围，继承“不修改 FlClash、不重装、不改系统网络”的边界；不重复部署和历史验收工程。表内 PASS 是上次观察，新的连接任务仍须取得本次桌面和两个网页证据。
2. 先区分通道与桌面工具：D 通道负责云端调用本机；windows-mcp-v1 负责本机截图、点击、输入。详见 [连接链路与完整步骤](references/connection-runbook.md)。
3. 在会话中发现 windows-mcp-v1 的原生工具；若已暴露，直接调用 Snapshot。若仅本机 Codex 已配置而云端会话未暴露，经已授权且已连通的 D 通道调用原配置的 stdio 服务；不重装、不改成公网服务、不通过其他接口绕过拒绝。复用 [现有 MCP 调用脚本](scripts/windows_mcp_session.py)。
4. 先获取实际桌面画面，再切换已有 Tor 窗口；未运行时才启动已有可执行文件。优先精确中文窗口名“Tor 浏览器”，确认画面和前台身份。
5. 在原生连接页点击“连接”，等待“已连接”及新标签页。已连接则直接进入验证。不能把安装成功、进程存在或端口监听当成连接完成。
6. 在同一 Tor Browser 中打开 https://check.torproject.org/ ，确认绿色成功提示；另开标签访问 https://www.torproject.org/ ，确认正文实际渲染。
7. 出现错误时读取可见报错与官方 Tor 日志，按 [故障与避错](references/troubleshooting.md) 定向处理；只在授权范围内继续。未获证据时保持 UNKNOWN。
8. 留下实际状态、证据来源和未完成项。正常结束本轮自建 MCP 客户端，不关闭用户的 Tor 窗口、D 隧道或其他共享进程。

## 2026-11-03 本会话验收快照

| 能力 | V4 当前状态 | 证据范围 |
|---|---|---|
| 云端经 D 调用本机 | PASS | 本会话实际命令往返 |
| windows-mcp-v1 桌面查看与操作 | PASS | Snapshot / App / Click / Shortcut / Type 实际返回及桌面画面 |
| 现有 Tor Browser 连接 | PASS | 点击“连接”后显示“已连接”并进入新标签页 |
| 浏览器内官方 Tor 检测页 | PASS | 绿色成功提示，确认该浏览器使用 Tor |
| 浏览器内 Tor 官网 | PASS | 同一浏览器第二标签加载中文首页正文 |
| 独立 Tor 的检测与官方 onion 访问 | 历史 PASS | 继承 V3，未在 V4 重跑 |
| 浏览器内 .onion 网页 | UNKNOWN | 不以独立 Tor 或 HTTPS 官网代替 |
| 正常关闭并重开浏览器后恢复 | NOT TESTED | 不以本次点击连接代替 |
| Windows 整机重启、无人值守恢复 | NOT TESTED | 不为文档升级重启电脑 |
| OnionShare 本机回环传输 | 历史 PASS | 仅 local-only；外部经 Tor 传输仍 UNKNOWN |
| I2P / Tails / Whonix | NOT INSTALLED | 保留候选，不自动部署 |

完整回执见 [V4 实际证据](references/acceptance-v4.md)。
V3 原包文字保存在 assets/v3-original/；其 FAIL 是当时状态，保留原义，不能覆盖 V4 较新证据，也不能倒改历史。

## 必须保持的区分

- 本次成功链路：云端助手 → 已连接 D 插件 → 本机命令 → windows-mcp-v1 stdio → 当前 Windows 桌面。windows-mcp-v1 不是云端到本机的公网隧道。
- 本地 Codex 已注册 windows-mcp-v1，不代表每个云端会话自动暴露同名工具。
- D 通道是本轮实测选择；不能宣称任何云端桌面连接都只能使用这一种组件。
- Tor 不需要创建账号才能连接网络。网页账号登录是另一任务，本轮未登录任何第三方账户。
- V4 的连接方法是“复用现有配置并点击连接”，本轮未修改 FlClash、代理、torrc、防火墙或重新安装软件；不能断言历史故障只有一个根因。
- 只操作获授权的桌面与资源。不要使用被拒绝的内部控制、认证或浏览器调试接口代替原生 GUI。
