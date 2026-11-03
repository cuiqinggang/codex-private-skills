# 《洋葱网络超能力 V2.0》当前验收
日期 2026-11-03，设备 DESKTOP-4A1EGTM
- V2 资源导航与部署技能：PASS（文件实际写入）
- Tor Browser 16.0 安装及签名：PASS（已在 V1 完成）
- 独立 Tor 通过本机 HTTPS 代理 7890 连通：PASS，Bootstrap 100%；官方 API IsTor:true，出口 IP 192.42.116.92
- Tor Browser 配置写入：PASS；tor --verify-config：PASS
- Tor Browser 重启后实际浏览：UNKNOWN
- 官方 .onion 网页加载：UNKNOWN
- Windows 整机重启恢复：UNKNOWN
- OnionShare 2.7.1：INSTALLED（Windows 卸载记录核对），发送/接收/聊天：UNKNOWN
- I2P、Tails、Whonix：候选，NOT INSTALLED
- 本地资源中心链接：已收录；各网站实时可达与内容质量：NOT EXHAUSTIVELY CHECKED
- 旧版本证据：CHECKS-V1-ARCHIVE.md

## 2026-11-03 真实补充验收
1. 独立 Tor SOCKS5h 127.0.0.1:9251 访问 Tor Project 官方博客 onion（从 onion.torproject.org 验证地址），HTTP 200，7.045 秒：PASS。
2. OnionShare 2.7.1 命令行：--help 可执行，PASS。本机 --local-only 分享测试文本，另一个 HTTP GET 获得 HTTP 200、52 字节；与原文件 SHA256 一致：LOCAL FILE TRANSFER PASS。注意本地回环模式不等于通过公开 Tor 网络的端到端交付，外部接收者 UNKNOWN。
3. Tor Browser 重启后确实已启动 firefox 进程，但未取得浏览器连接界面或浏览器通过 Tor 的网页输出：BROWSER NETWORK UNKNOWN。不能把独立 Tor 检测结果当作 Tor Browser 验收。
4. 独立 Tor 的官方 onion HTTP 200 PASS；浏览器内 onion 打开 UNKNOWN。
5. Windows 整机重启恢复 NOT TESTED（避免中断现有自动化与代理）。
6. C 盘可用 230934138880 字节（约215 GiB），空间不是主要限制。
7. I2P 独立网络：官方当前 2.14.0；winget 当前 Easy Install 2.12.0 比官方旧，避免安装旧包。候选 i2pd 3.0 需要另行判断，当前未安装。
8. Tails 需 USB 开机进入独立系统，Whonix 需虚拟机和系统资源；对现阶段只读信息访问无必要，暂不安装，避免额外维护与系统影响。
9. Tor 不需要创建账号登录；当前用户看到的更可能是连接未建立，而非账号未登录。需浏览器 UI 复核后确认。

## 桌面 GUI 2026-11-03
Tor Browser GUI process present; Browser torrc overwritten to DisableNetwork 1; browser SOCKS 9150 not listening, confirmed FAIL. Local proxy 127.0.0.1:7890 is available. Opened official about:preferences#connection. Direct browser control command was blocked by security policy and not retried. Browser needs native Connection > Advanced > Configure proxy: HTTPS 127.0.0.1 port 7890 > OK > Connect > Always connect automatically. GUI connected state NOT VERIFIED, do not label PASS.
