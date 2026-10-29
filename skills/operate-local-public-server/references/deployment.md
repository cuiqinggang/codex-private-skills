# 部署和恢复

本技能V1.0封装的是2026-10-29已部署的文件分享服务。现有电脑无需重新部署。程序实现分支保持V2.0，不改变AI自动化组织V5或备用系统版本。

## 固定成熟部件

| 部件 | 固定版本/位置 |
|---|---|
| 文件服务器 | Copyparty v1.20.26，官方 `copyparty-sfx.py` |
| Copyparty SHA256 | `8f9a0def8a9c15252a06395781ec083372043b60caa80fb33c3d6dafa7f1b40a` |
| 公网入口 | 官方 cloudflared 2026.10.4，现有电脑已安装 |
| cloudflared SHA256 | `411b16d40c8d872243efeb52c550053d00af0a8a97fbb32e730fb8aba429eaa8` |
| 程序根 | `C:\AI\Public-Server` |
| 文件区 | `shared`公开下载、`public`静态网站、`private`私有卷 |
| 本机管理 | IPv4 `127.0.0.1:18780`，上游IP自动识别为owner，无需登录 |
| 隧道源站 | IPv6 `[::1]:18780`，公网仅匿名只读 |
| 其他端口 | metrics 18781、预检18782，禁止公开 |
| 持久运行 | 原 Windows 任务计划 `AIORG-PublicWeb-Origin`、`AIORG-PublicWeb-Tunnel` |

cloudflared复用原已验证二进制，不复制原MCP网关或凭据。Copyparty安装器固定官方发行URL及SHA256。散列、凭据、数据库位于公开卷之外，Windows ACL限制本人、SYSTEM和管理员。技能包不得携带这些运行时秘密。

## 原部署如何完成

1. 使用A发现在线Windows并探针。核对端口、任务归属和现有文件。建立专用根和模板，复用官方cloudflared，登记当前用户登录触发、最低权限、IgnoreNew的两个原任务。
2. 先以Python标准HTTP服务完成临时网站的启动、停止、重启和9项公网检查，再原位升级为成熟Copyparty。历史实现不作为当前文件上传协议。
3. 下载并校验官方Copyparty。备份原程序/配置/首页/任务。配置专用卷、本机owner权限、公网匿名只读、密码/有效期分享、独立数据库、日志及ACL。
4. 在18782独立预检，shares/sessions/hist均不与生产争锁。27项全过后，先停隧道和源站，将隧道源站切到IPv6，再登记并启动原两任务，完成27项公网接口复验。
5. 本机IPv4免登录，Cloudflare请求来自IPv6。IP映射使用默认visitor，再以ipr降为匿名；只信任IPv6回环的CF来源头，rproxy=1识别HTTPS。禁止将免登录IPv4管理口接入隧道。
6. 公网读取成功后执行checkpoint，保留已验证恢复点。用户拖拽失败后修正桌面入口为原生目录联接，实际Ctrl+鼠标拖拽复制，核对落盘和公网下载字节；未将HTTP测试冒充网页拖拽。

## 在现有电脑接续

读当前 `status`、`config.json`、`share-upgrade.json`，缺少操作助手时仅复制附带 `share_file.py` 到根目录。不要为日常分享执行install/prepare/activate，不重启正常隧道。文件助手直接使用现有服务。

## 新电脑或确需重新安装时

新电脑部署尚未认证，必须按实际输入验收，不直接继承旧PASS。

1. 确认Windows有Python、IPv6回环可用、18780/18781/18782未被其他程序占用，没有同名无关任务。取得官方对应cloudflared发行包并验证上述摘要；版本不同则重新核验官方制品及影响，不静默替换。
2. 将附带 scripts 中四个 `.py` 放到 `C:\AI\Public-Server`，将 `assets/public-server` 模板放到 `public`。不要复制现有电脑的凭据、数据库或个人分享文件。
3. 运行 `public_server.py install --cloudflared-source <官方二进制绝对路径>`，再 `upgrade_file_share.py prepare`。此时尚不对外发布免登录管理服务。
4. `verify_file_share.py --stage`通过27项后运行 `upgrade_file_share.py activate`。后者先停止两个原任务，设定IPv6隧道目标，再启动；未通过预检不得直接暴露新源站。
5. 运行 `verify_file_share.py`公网复验，之后 `upgrade_file_share.py checkpoint`。再实际分享合成文件，验证当前网址及源文件保留。需要认证鼠标交互时另测UI，不能用文件复制代替。

## 恢复

先检查运行状态与原任务；UNKNOWN先对账，不双开。服务失败时停止原两任务，读取 `share-upgrade.json` 的 `verified_backup`；`backup`只是升级前快照，可能属于失败尝试。成套恢复已验证目录中的程序、config、copyparty配置、本机凭据和首页，按恢复设置重新登记任务再启动并复验；最后repair-controls修复桌面入口。分享文件、数据库不在配置检查点内，不擅自清理或覆盖。

原manager在start时有75秒界，最多向同一IgnoreNew任务追加两次启动请求；不另造全天监护器。停止同时禁用自启，启动重新启用。登录触发已配置，实际整机重启和长期稳定性未认证。

## 已知教训

- Windows中文文件指定UTF-8，PowerShell脚本文件用UTF-8 BOM。避免嵌套多层引号。
- 上游空字符串/直接`*`的IP映射曾触发KeyError；采用已有visitor+ipr配方，不改上游源码。账号散列不得相同。
- rproxy=0影响HTTPS同源请求；保持rproxy=1及跨站本机写入拒绝，不为拖拽方便开放公网上传。
- 重命名/删除用官方POST，不开启GET修改。xvol/xdev和一个目录联接拒绝样例不是操作系统沙箱。
- 明确本机和公网入口；日常由AI复制文件、返回链接，减少用户手工操作。

## 官方来源

- https://github.com/9001/copyparty/tree/v1.20.26
- https://github.com/9001/copyparty/blob/v1.20.26/docs/examples/windows.md
- https://github.com/9001/copyparty/releases/tag/v1.20.26
- https://github.com/cloudflare/cloudflared/releases/tag/2026.10.4
- https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/
