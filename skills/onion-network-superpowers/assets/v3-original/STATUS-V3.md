# 《洋葱网络超能力》V3.0 — 冻结状态与后续验收
版本日期：2026-11-03；类型：整数升级；本轮仅归档整理，不宣称新增修复成功。
## 已完成（有本机证据）
- Tor Browser 16.0 官方发行包下载安装成功；Windows 数字签名有效，校验值记录在 V1/V2 验收历史中。
- 发现直接连接中继超时的主要网络因素：本机外部网络使用 HTTP(S) 代理 127.0.0.1:7890。
- 独立 Tor 0.4.9.15 设置 HTTPSProxy 127.0.0.1:7890、SOCKS5h 127.0.0.1:9251：Bootstrap 100%；Tor 检测 API 返回 IsTor:true；该测试 PASS。
- 独立 Tor SOCKS5h 请求经官方目录核对的 Tor 博客 .onion 服务，HTTP 200，约 00:07:045：PASS。
- OnionShare 2.7.1 已安装，CLI 可执行；本机 local-only 分享测试文件、另一次下载成功且 SHA256 一致：PASS（仅本机回环）。
- V2 资源入口、技能说明、修复笔记、验收记录、桌面快捷方式已建成，V3 继承。
## 未完成 / 失败（禁止冒称已通过）
- 【FAIL】桌面 Tor Browser GUI 未连通。真实界面显示“未连接”，9150 SOCKS 未监听，浏览器自己的 Tor 进程仍带 DisableNetwork 1。已在 GUI 设置 HTTP/HTTPS 127.0.0.1:7890、点击连接、正常重启，仍未通过。
- 【UNKNOWN】桌面 Tor Browser 内打开 https://check.torproject.org/ 返回 Tor 成功提示；未获证据。
- 【UNKNOWN】桌面 Tor Browser 实际打开 .onion 页面（独立 Tor 已成功，不可代替此项）。
- 【UNKNOWN】OnionShare 通过 Tor 网络与另一独立终端真实传输（local-only PASS 不可代替）。
- 【NOT TESTED】整机重启后的恢复与重新连接。
- 【NOT INSTALLED】I2P（与 Tor 不同的匿名网络，需匹配新版本及依赖）、Tails（USB 启动）、Whonix（虚拟机）。Tails/Whonix 目前没有刚需，不应为了装全而占用资源。
- 【UNKNOWN】所有导航网址的实时可达率、资料实用性、自动化持续可用性。
## 故障复盘
独立 Tor 成功，桌面 Tor Browser 失败，根因不能简单归为外部代理。Tor Browser 在启动时管理 Tor 连接状态、覆盖 torrc，保持 DisableNetwork 1。GUI 填写代理参数、点击连接并重启后仍失败。不要尝试把独立实例的 IsTor:true 当作浏览器成功，也不要使用访问受限的内部控制/认证接口强制突破。优先官方 GUI/诊断日志与可核查修复。
## 后续最小执行顺序
1. 对桌面 Tor Browser 做原生连接诊断，提取可见错误与完整日志（不暴露令牌），识别 DisableNetwork 1 持续原因。
2. 通过官方连接方式完成实际 GUI 联通；浏览器内打开 check.torproject.org 判定 PASS；再打开官方 .onion 地址。
3. 正常关闭、重新启动浏览器复测；必要时维护现有本机 7890 网络依赖检查。
4. OnionShare 两终端经 Tor 测试文件一致性；不分享真实敏感文件。
5. 在不打断现有系统的适当窗口做整机重启恢复验证。
6. 若确有独有需求，再验证 I2P；Tails/Whonix 有明确隔离用例才安装。
## 版本门
V3.0 表示“证据与能力目录规范升级”，不是所有能力验收通过。后续任何 PASS 必须附操作回执/网络检测与用时，失败如实保留。评价指标：T_VALID_E2E（含重试恢复、安全与人工介入）。
