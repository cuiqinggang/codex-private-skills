# V4 实际证据与升级范围

日期：2026-11-03，北京时间。设备：DESKTOP-4A1EGTM。
任务：使用已启用 windows-mcp-v1 操作已有 Tor Browser，不修改 FlClash、不重装；先确认桌面，再分别验证浏览器网络与官网。

## 直接观察

| 项目 | 本轮证据 | 状态 |
|---|---|---|
| D 原生往返 | Windows D 20261103-01 的 open_workspace / exec_command / write_stdin 返回 | PASS |
| 本机 MCP 配置 | C:\Users\A\.codex\config.toml 含 windows-mcp-v1 与原 Python/stdio 参数 | PASS |
| 桌面可见 | Snapshot 实际截图含三块显示器与 Tor 窗口；主屏截图可读 | PASS |
| 桌面操作 | 切换 Tor 中文窗口、Click、Shortcut、Type 均实际返回；随后画面变化 | PASS |
| Tor 连接 | 未连接页面 → 点击连接 → 正在建立连接 → 已连接新标签页 | PASS |
| 浏览器网络 | https://check.torproject.org/ 绿色文字“Congratulations. This browser is configured to use Tor.” | PASS |
| 官网显示 | 同一 Tor Browser 第二标签 https://www.torproject.org/ 的中文导航与正文实际显示 | PASS |
| 收尾 | 临时 MCP 会话输入 EXIT，返回退出码 0；两个 Tor 标签保留 | PASS |

证据来源为本对话实际工具返回和已查看的截图；没有另存截图文件或编造原始日志路径。
未收集任何账户密码、令牌或网页登录态。Tor 检测页出口地址可变化，不作为验收固定条件。
独立 Tor 成功没有被用来替代浏览器检测。
历史 V3 中 GUI FAIL 保留为历史，在当前状态中由这次浏览器直接证据更新。

## 明确未测

- 重新关闭并启动浏览器；Windows 整机重启、无人值守、多日稳定性。
- 浏览器内 .onion 页面与 OnionShare 跨终端经 Tor 文件传输。
- 自动连接设置在未来启动是否有效。
- 所有资源导航链接的实时可达率。
- 新安装组件、替换网络配置、全平台接入或全局自动加载。
- 精确 T_VALID_E2E：NOT_MEASURED；不可拿人工设置的等待窗口当精确时长。

## V3 继承

原来源：
C:\Users\A\.codex\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS\03_SKILLS\onion-network-superpowers。
原 V3 文件未原地修改。assets/v3-original/ 为本轮读取后保存的文字副本，未声称逐字节封袋。
保留历史独立 Tor 与本机回环 PASS，保留候选组件及未完成事项。
V4 是连接流程与证据升级，不表示所有匿名网络能力均已验收。

## 接手最短提示

使用《洋葱网络超能力 V4.0》，复用当前 D 通道和本机 windows-mcp-v1，先查看真实桌面，再操作已有 Tor Browser。保持 FlClash 和现有系统网络配置，确认检测页绿色成功与官网正文。已通过项不重复部署，未通过项保留具体状态；只处理当前授权任务。

## V4 文档与复用脚本验证

- 技能格式、Python 语法、Markdown 本地引用：PASS。
- 本机现有 Python / mcp SDK 实际调用随包脚本的 DisplayInventory：返回当前三屏信息，进程退出码 0，PASS（2026-11-03 20:45 北京时间）。不据此扩大为脚本全功能长期认证。
- 真实测试发现 SDK Python 字段为 is_error、序列化别名为 isError；已改为检查序列化结果，避免成功响应后误抛异常。前两轮脚本测试退出 1 已修正，未作为成功计入。
- V3 原目录写入前后哈希对比一致；保留旧冻结，不原地覆盖。
