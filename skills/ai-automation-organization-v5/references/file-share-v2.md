# 本机文件与网站分享 V2.0

组织版本保持 V5.0；本分支从 V1.0 升至 V2.0。日期：2026-10-29，Asia/Shanghai。任务：AIORG-FILESHARE-20261029-001。

## 现行配方

复用 Copyparty 官方 Windows 示例，配置专用卷及权限；不自行开发网盘、上传器、下载器、用户系统或链接系统。复用原 cloudflared 和任务计划。按用户最新要求，本机管理无需登录；公网只读。为分开两类连接，本次将隧道源站切到 IPv6 回环，隧道重启后网址会变化。

- 上游：Copyparty v1.20.26，官方 `copyparty-sfx.py`，1,206,486 字节。
- SHA256：`8f9a0def8a9c15252a06395781ec083372043b60caa80fb33c3d6dafa7f1b40a`。
- Windows 根：`C:\AI\Public-Server`；监听 `127.0.0.1:18780`（本机管理）及 `[::1]:18780`（隧道访客）；仅回环可连接。
- 外网入口：当前免费 Cloudflare 隧道；从 `public_server.py status` 读回。

| 路径 | 对应目录 | 访问范围 |
|---|---|---|
| `/`、`/demo/` | `public` | 原网站展示，访客读取网页 |
| `/download/` | `shared` | 访客浏览/下载；本机自动识别后上传、移动、删除 |
| `/private/` | `private` | 仅本机直接管理；访客拒绝 |
| `/s/随机链接/` | 上游受控分享 | 本机创建，可设密码及有效期 |

数据库、配置、登录说明和程序位于公开卷之外。账号配置采用上游同格式 scrypt，凭据及配置通过 Windows ACL 限制到本人、SYSTEM、管理员；不得将这些文件复制到共享目录或技能包。

## 用户操作

桌面「我的公网服务器」保留启动/停止，日常入口整理为：

- `放文件（拖到这里即可分享）`：Windows 原生目录联接，直接对应 `shared`；拖入文件后即出现在下载区。也可以先打开文件夹，再拖入；Ctrl+拖拽为复制。
- `本机上传（免登录）.cmd`：打开 `http://127.0.0.1:18780/download/`，本机自动管理，不要求登录。
- `给别人下载（打开后复制网址）.cmd`：打开当前公网只读下载页；复制地址给别人，新增文件后刷新页面。

旧命令和快捷方式移至「其他入口」保留。公网页只供读取，不能把“在自己电脑打开公网网址”当作本机管理；不能把下载页的拖拽失败解释为已上传。运行 `public_server.py repair-controls` 可幂等修复桌面入口，无需重启隧道。

只放准备公开的文件到 `shared`。需要保护的文件放 `private`，通过密码/有效期链接分享，不把公开下载区的链接当作隐私保护。

## 程序与恢复

入口：`public_server.py`。新增 `downloads`、`admin` 操作；原 `start/stop/status/open/target` 保留。原 `AIORG-PublicWeb-Origin` 任务现在直接启动官方 Copyparty；原隧道任务改为连接 `[::1]:18780`；管理入口固定使用 IPv4 `127.0.0.1`。关机/睡眠/断网仍会暂停，登录自启仍为已配置、未以本次整机重启认证。

`upgrade_file_share.py prepare` 先校验上游摘要、备份旧源站/配置/首页和任务定义、生成受保护账号和卷配置。`verify_file_share.py --stage` 在回环 18782 端口核验，通过 27 项才允许 `activate`。使用上游 IP 自动识别：IPv4/IPv6 默认映射到 `visitor`，本机 `127.0.0.1/32` 更具体地映射到 `owner`；`ipr` 将两者限制在 IPv4 回环，所有外部 `visitor` 均降为匿名 `*`。仅信任 `::1/128` 的 Cloudflare 来源头，使用 `rproxy: 1` 正确识别 HTTPS；即使缺少来源头，IPv6 代理连接仍是访客。禁止将本机 IPv4 管理地址作为隧道源站；入口程序已阻止此操作。升级不新增服务管理器，不改系统代理、DNS、路由器或现有 A/B 通道。

```text
python C:\AI\Public-Server\public_server.py status
python C:\AI\Public-Server\public_server.py downloads
python C:\AI\Public-Server\public_server.py admin
python C:\AI\Public-Server\verify_file_share.py
python C:\AI\Public-Server\upgrade_file_share.py checkpoint
```

公网复验通过后执行 `checkpoint`，保存一份 ACL 保护的已验证配置及配套程序；`share-upgrade.json` 的 `verified_backup` 是优先恢复点，`backup` 仅是升级前快照，可能属于失败尝试，不能当已验证版本。发生源站启动失败时先停止原两任务，成套恢复已验证目录内的 `config.json`、`copyparty.conf`、本机凭据、首页和配套程序，再按恢复后的设置登记/启动任务并复验。分享文件及数据库不包含在这个配置检查点中。禁止把隧道改回 IPv4 本机管理地址却保留自动管理权限；缺少配套旧配置时保持现行 IPv6 隔离，先对账。提交状态 UNKNOWN 先检查当前源站与任务，不盲跑第二份。旧 V1 配方与证据见 [public-server.md](public-server.md)，不得将 V1 的只读 POST=501 检查当作 V2 上传能力合同。

## 验收与诚实边界

本机预检覆盖网页/文件列表、访客越权拒绝、管理员上传字节一致、匿名下载、Range 206、中文文件名、ZIP 打包、私有卷与配置拒绝、Windows 目录联接越界拒绝、密码/有效期分享创建、未提供分享密码拒绝、正确分享密码读取，以及管理员改名和删除。另核验免登录管理员权限、访客只读权限、浏览器同源请求头、IPv4/IPv6 代理来源映射和跨站本机写入拒绝。公网复验使用同一组接口和合成文件，管理写入走 IPv4 本机免登录入口，访客读取/拒绝检查走公网入口；原始结果为本机 `share-stage-acceptance*.json`、`share-public-acceptance*.json`，脱敏合并记录见 [验收文件](file-share-v2-acceptance.json)。到期参数创建已测，不冒充实际等待到期后的访问实测。

HTTP 接口实测不冒充浏览器鼠标拖拽、全部媒体格式或大型文件实测。目录联接样例通过不等于操作系统级沙箱；不把 xvol/xdev 当作独立安全边界，依靠明确卷、访客只读和本机/隧道连接分离。禁止对外开放 FTP、SMB、SSH、MCP、系统文件或匿名写入。

文件由本机提供，但公网仍经 Cloudflare 转发，省掉先上传网盘这一步，不声称物理路径最短或下载一定比商用网盘快。实际速度受本机上行带宽、线路、磁盘和对端网络影响。普通桌面软件的安装包可以下载；让软件在浏览器操作需要它本来具有网页服务入口，不能仅靠文件共享自动实现。

新增软件/穿透订阅费用为 0；电费、带宽、维护成本未实测。完整接单计时缺前置部分，T_VALID_E2E=NOT_MEASURED；另记录观察窗口，不宣称极限最短。

## 本次修正经验

- 不通过整套应用的 CLI 传递明文密码做散列：首次尝试 20 秒超时，异常命令行可能包含临时密码。上线前已换新，改用与上游 `pwhash.py _gen_scrypt` 完全一致的参数和格式；当前密码未写入工具输出、技能或公网目录。
- 初始检查错误地用 GET 请求测试重命名。上游默认不允许 GET 修改；改为官方 POST 接口，保留旧失败记录，不开启不必要的 GET 修改功能。
- 用户纠偏后撤掉本机登录步骤，采用上游 IP 自动识别和代理访客映射；不向公网开放免登录管理。保留一个现成文件服务器和原任务计划即可。UI、上传分块、下载 Range、打包、预览、登录和分享均复用上游，避免自研同类功能。

## 官方来源

- [项目及权限说明](https://github.com/9001/copyparty)
- [官方 Windows 示例](https://github.com/9001/copyparty/blob/v1.20.26/docs/examples/windows.md)
- [固定版本发行包](https://github.com/9001/copyparty/releases/tag/v1.20.26)
- [固定版本密码格式](https://github.com/9001/copyparty/blob/v1.20.26/copyparty/pwhash.py)

- 上游空字符串/直接匿名 IP 映射在本机触发 KeyError，改为映射独立 `visitor` 身份再用上游 `ipr` 降为匿名；保留本机 IP 自动管理规则，不改上游源码。为真实客户端 IPv4/IPv6 添加默认映射；不能用 `rproxy: 0` 掩盖映射问题，否则浏览器 HTTPS 同源请求可能被拒绝。账号散列必须互异，不能复用同一密码散列。预检使用独立 shares/sessions 数据库、hist 和配置目录，遵守上游并发锁，禁止关闭数据库锁。

## 2026-10-29 拖拽操作修正

用户实际拖拽失败后补验收。原 27 项仅是 HTTP 接口合同，不能据此宣称已测试鼠标拖拽。当前使用 Windows 原生文件夹入口，已用鼠标 Ctrl+拖拽复制合成文件，核对文件落盘、字节一致、目录联接对应关系及公网读取。证据见 [拖拽验收](file-share-v2-drag-acceptance.json)，原 27 项记录作为历史保留。

浏览器控制发生超时，网页里的鼠标拖拽仍未实测；不得将文件夹拖拽或选择文件/API 上传冒充网页拖拽通过。当前日常推荐已实测的原生文件夹路径。本机网页上传入口保留，公网上传继续禁止。
