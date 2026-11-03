# 《洋葱网络超能力 V2.0》故障复用
## 原始故障
Tor Browser 16.0 安装成功，但 Tor 直连中继超时，日志卡在 Bootstrapped 5%（WSAETIMEDOUT）。
## 根因与实证
本机上网使用 127.0.0.1:7890 的 HTTP(S) 代理。经 7890 请求 Tor 官方检测页成功；直接连接 Tor 中继超时。
## 已成功的修复
以 Tor 0.4.9.15 独立实例设置 HTTPSProxy 127.0.0.1:7890 和 SOCKS5 127.0.0.1:9251，Bootstrap 达到 100%；通过 curl socks5h://127.0.0.1:9251 请求 https://check.torproject.org/api/ip ，返回 IsTor:true，出口 IP 192.42.116.92（仅为当时出口，可能变化）。
## 持久化
Tor Browser 的 torrc 已备份 torrc.backup-v1，并配置 HTTPSProxy 127.0.0.1:7890、DisableNetwork 0。tor --verify-config 返回 Configuration was valid。
## 重要差别
独立 Tor 实例联网成功不等于 Tor Browser 重新启动已通过。重启/浏览器网页访问/.onion 测试仍待真实验收；不能用 9151 控制端口误认为 9150 SOCKS 可用。
## 回归步骤
1. 确认本机 7890 代理仍在监听并能访问可信 HTTPS 网站。
2. 启动 Tor Browser，检测 https://check.torproject.org/ 。
3. 验证官方 .onion 页面，确认网页能够加载。
4. 重启电脑并重复，记录失败、用时及恢复步骤。
5. 如果出现问题，先检查代理、原配置备份和端口冲突，避免关闭 Windows 防护或修改全局网络。
