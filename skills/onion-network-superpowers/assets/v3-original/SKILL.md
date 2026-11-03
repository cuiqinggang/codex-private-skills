# 《洋葱网络超能力 V3.0》超级能力包
版本：V3.0.0 | 2026-11-03 | Windows DESKTOP-4A1EGTM | 安全用途：公开信息研究、匿名隐私访问与安全协作

## 唯一入口
桌面“洋葱网络超能力 V3.0.lnk” → 本地“INDEX.html”资源导航，单击访问官方来源。日常操作不需要重新安装。
## 当前真实状态
- Tor Browser 16.0：安装 PASS。软件位置 C:\Users\A\Desktop\Tor Browser。
- Tor 网络真实访问：独立 Tor 0.4.9.15 已通过 HTTPSProxy 127.0.0.1:7890，SOCKS 127.0.0.1:9251 引导到 100%，官方 API 返回 IsTor:true（PASS）；Tor Browser 直接访问及重启恢复尚未重新验收（UNKNOWN）。
- OnionShare 2.7.1：从官方 winget 来源安装，卸载注册表检测到版本 2.7.1（INSTALLED）；分享/接收/聊天功能尚未进行真实传输验收（UNKNOWN）。
- 导航首页、使用说明、故障修复说明：已写入；外链访问需实时校验。
- I2P、Tails、Whonix：候选，未部署。不能称全部能力均安装。
## 高频成熟能力与用途
1. Tor Browser：匿名公开网页、.onion 网站访问；官方 https://www.torproject.org/download/
2. Ahmia：可公开检索的 onion 搜索（不保证结果安全）；https://ahmia.fi/
3. OnionShare：点对点文件发送/接收、临时匿名网站、聊天；https://onionshare.org/
4. SecureDrop：媒体机构的匿名线索提交系统与公开目录；https://securedrop.org/directory/
5. Onion Services：隐藏真实服务地址的服务开发架构；https://onionservices.torproject.org/
6. Tor Project onion 服务导航：https://onion.torproject.org/
7. 安全情报：CISA KEV https://www.cisa.gov/known-exploited-vulnerabilities-catalog ; MITRE ATT&CK https://attack.mitre.org/ ; CVE https://www.cve.org/
8. 调查新闻：ProPublica https://www.propublica.org/
9. I2P：另一独立匿名网络，https://i2p.net/ （按需安装）。
10. Tails：USB 隔离操作系统，https://tails.net/ （需实际 USB 和重启验收）。
11. Whonix：虚拟机隔离的 Tor 操作系统，https://www.whonix.org/ （需独立虚拟化验收）。

## 标准使用选路
普通公开安全资料→普通浏览器优先。必须 onion→Tor Browser，先连通检测。敏感文件合法分享→OnionShare，仅选择明确文件/目录。独立匿名网络→I2P。一次性隔离→Tails。高隔离虚拟机→Whonix。不要把任何未验证候选描述为已可用。

## 故障修复：已在本机真实验证的方法
现象：Tor 直连卡 Bootstrapped 5%；连接中继报 WSAETIMEDOUT。原因：此 Windows 会话走本机 HTTP(S) 代理 127.0.0.1:7890，直接访问中继超时。
实际修复：Tor 支持 HTTPSProxy 127.0.0.1:7890，建立 Tor 出口；独立实例 SOCKS5h 127.0.0.1:9251 通过官方 check.torproject.org/api/ip 证实 IsTor:true。浏览器 torrc 已备份并加入 HTTPSProxy 127.0.0.1:7890 / DisableNetwork 0，tor --verify-config PASS。
重要：浏览器控制端口 9151 ≠ SOCKS 9150；配置验证 PASS ≠ 浏览器连通 PASS。若代理未启动，不可假称 Tor 可用；恢复时先检查 7890 本地监听与 Tor Browser 内置连接配置。独立 Tor 和浏览器实例不可混为一谈。不要反复启动相同 SOCKS 端口造成冲突。
参考：参见 REPAIR.md / CHECKS.md，保留 V1 验收归档。不要更改现有 Windows 执行桥的 D 优先规则。

## 安全与升级门
只访问合法公开资源；不收集未经授权的密码/凭证、不下载或运行不明二进制；不把支付账户、GitHub 密钥、真实客户数据暴露给匿名网站。Tor 不是绝对匿名保证。禁止为追求联通关闭防火墙或全局代理。每次升级只合并有来源与现实证据的功能。T_VALID_E2E 需包含失败恢复、人工成本和质量约束。状态分 PASS/INSTALLED/UNKNOWN/FAIL。


## V3.0 冻结状态
本次整数升级详见 STATUS-V3.md；桌面 Tor Browser GUI 连接仍 FAIL，其他逐项状态详见该文档。

