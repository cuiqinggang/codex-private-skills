# 本机公网服务分支 V1.0

日期：2026-10-29（Asia/Shanghai）。任务：AIORG-PUBLICWEB-20261029-001。

## 合同与成熟路径

让用户自己的 Windows 电脑真正运行服务，通过免费 HTTPS 网址供其他人访问。允许关机、睡眠、断网时停止服务；暂不租云服务器或购买域名。默认发布专用展示站，不擅自公开原租赁系统、客户记录、管理后台、MCP、浏览器调试端口或私有文件。

采用已有官方 cloudflared 2026.10.4、Python 3.13 标准库 HTTP 服务及 Windows 自带任务计划程序。frp 自建中转不进入本次部署，因为当前没有必要新增公网中转服务器。不要照搬旧 A-Transport 测试中的 MCP 网关，只复用其已存在的官方二进制。

cloudflared SHA256：411b16d40c8d872243efeb52c550053d00af0a8a97fbb32e730fb8aba429eaa8。

## 已部署入口

- 程序：`C:\AI\Public-Server\public_server.py`。
- 唯一静态发布根：`C:\AI\Public-Server\public`。
- 本机网站：`http://127.0.0.1:18780`；隧道就绪探针：`http://127.0.0.1:18781/ready`。
- 配置、状态、当前地址：根目录下 `config.json`、`status.json`、`CURRENT-URL.txt`；它们不在公开目录内。
- 桌面：`我的公网服务器` 文件夹内的启动、停止、查看公网网址、打开共享目录四个入口及中文说明。
- 任务计划：`AIORG-PublicWeb-Origin`、`AIORG-PublicWeb-Tunnel`。以当前用户登录触发、最低权限运行；重复启动由 IgnoreNew 防止多开，失败重启配置为 1 分钟、最多 3 次。
- `停止`同时停止并禁用这两个任务；`启动`重新启用。没有更改电源睡眠、路由器、防火墙、系统代理、DNS、已有 A/B 通道或其他业务服务。

重启隧道后随机网址会变。每次分享前读取当前状态，不把验收报告中的网址当永久域名。Windows 登录自动运行已经配置；本任务未通过整机重启测试，不写“跨开机已认证”。

## 最短操作

先按当前执行桥发现 A 在线设备并探针。使用 Python 文件，不再嵌套拼接复杂 PowerShell/Windows 引号。

```text
python C:\AI\Public-Server\public_server.py status
python C:\AI\Public-Server\public_server.py start
python C:\AI\Public-Server\public_server.py stop
python C:\AI\Public-Server\public_server.py open
```

要发布新静态站，创建 `public\项目名\index.html`，访问“当前公网网址/项目名/”。只复制准备公开的构建产物，不复制 `.env`、源码仓库、凭据或整个桌面。展示目录禁止列表浏览、禁止符号链接越界，仅监听本机回环；公网只读，不接受上传/写入。

动态应用须先独立运行，并确认用户授权公开该应用及其中的数据，再将隧道指向它的明确回环端口。例如：

```text
python C:\AI\Public-Server\public_server.py target --url http://127.0.0.1:3000
```

此命令先检查目标，再停止本分支隧道、更改目标、重新启动；不是自动安装该应用、数据库或支付服务。新应用须分别检查页面、API、登录、数据和外部依赖。不得把默认静态站验收扩成任意动态应用已验收。

## 恢复与经验

- 首次建立隧道时出现 `region2.v2.argotunnel.com ... no such host`；只读 DNS 查询成功后再次运行恢复。推断为瞬时解析问题，未证明其唯一根因。未修改系统 DNS、hosts 或代理。
- 启动入口现有界等待 75 秒，必要时通过系统解析器查询两个官方区域，最多向同一任务追加两次启动请求。IgnoreNew 防止对正在运行的隧道重复创建进程；这是启动阶段恢复，不是全天独立守护承诺。
- 若仍未就绪，读 `logs\tunnel.log` 与两个任务状态；真实故障只修受影响节点。不重跑旧业务、不切 B/C、不回显日志中的私有信息。
- 早期验收把路径越界拒绝写死为 404；Cloudflare 实际返回 400，属于有效拒绝。正确判断为 400/403/404 且未泄露私有内容。初始失败报告保留在本机，没有回填为通过。
- Python `-c` 经 Windows 多层引号进行文本替换曾失败；采用直接写入完整 `.py` 文件修复，后续复用此路线。
- 状态文件采用同目录唯一临时文件后原子替换；不要恢复成并发共享同一个 `.new` 临时名。

## 实测证据与边界

原始证据：本机 `installation.json`、`acceptance.json`、历史 `acceptance-*.json`、`logs\`；脱敏结果见[本分支验收记录](public-server-acceptance.json)。

已经实测：公网 HTTPS 主页字节哈希与本机一致、演示子页、配置/脚本/日志拒绝、路径越界拒绝、新增文件即时可读、文件更新即时生效、拒绝 POST；公网路由检查 9/9 通过。停止后两个本机监听均关闭，重新启动恢复，临时网址确实变化。源码复用验证还在隔离环境通过目录列表禁止、符号链接越界、父目录读取、HEAD 与缓存控制检查。

公网请求从用户本机经 Cloudflare 边缘再返回源站，响应含 Cloudflare 路由及动态缓存标识；不能冒称独立外网手机或第三地测试。独立执行环境访问被出口限制阻断，浏览器自动化连接超时，未完成 UI 点击验收。新电脑部署、真实关机/重启恢复、任意动态应用、长期在线率、高并发和商业 SLA 未认证。

本次新增云服务器/穿透订阅费用为 0；本机电费、宽带和维护成本未计量。整个接单前段未建立完整计时，完整 T_VALID_E2E=NOT_MEASURED；仅保存执行观察窗口与具体启动耗时，不以它宣称全球最短。

## 迁移复用

技能携带 `scripts/public_server.py`、`scripts/verify_public_server.py` 和 `assets/public-server/`。部署到 Windows 的本分支根目录，将静态模板置于 `public`；复用官方 cloudflared 后运行 install。首次安装先检查端口 18780/18781 不被其他程序占用；同名任务不含本分支标记时拒绝覆盖。不要打包无关 node_modules、模型或 Docker 镜像。

## 官方依据

- [Cloudflare Quick Tunnels](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/)：免费临时入口、地址变化、无在线率保证、200 个同时在途请求、不支持 SSE。
- [Cloudflare 故障排查](https://developers.cloudflare.com/tunnel/troubleshooting/)：区分 DNS、传输和源站错误。
- [Cloudflare 运行参数](https://developers.cloudflare.com/tunnel/reference/run-parameters/)：HTTP/2、日志、metrics 和重试等官方接口。
- [Python http.server](https://docs.python.org/3/library/http.server.html)：本分支只用于受限临时展示；正式商用应用使用其成熟生产服务器。
