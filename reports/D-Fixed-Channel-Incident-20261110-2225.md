# 固定D通道故障诊断与自动重连验收

日期：2026-11-10，北京时间约22:20—22:26。入口Windows D 20261110-02。

## 结论
固定网址未变且有效；已直接抓到ngrok隧道会话断开、端点离线与重连期间CRL下载超时。22:26:32原ngrok进程自动重连，随后同一D插件原生读文件与hostname退出0。初始远端EOF/心跳超时的网络责任点（本机出口、运营商或ngrok侧）未独立定位；CRL超时是一次重连失败的明确原因，不扩大为所有前期超时的唯一根因。

## 事实链
- 固定配置URL仍为https://ogle-grooving-skipper.ngrok-free.dev/mcp，本机端口17677。
- server PID17984、ngrok PID15864，自18:21左右运行，诊断期间未变化。
- 22:20:11健康回执：本机metadata 200，公网TimeoutError，DEGRADED，两个进程alive=true。
- 直接检查：本机authorization-server与protected-resource/mcp均JSON 200，issuer与resource精确指向固定origin。
- 同一诊断公网authorization-server一次UND_ERR_SOCKET，而protected-resource/mcp为200；稍后连续三次authorization-server 200，约1292/1367/1700ms。
- 22:24:02自动健康回执：local/public均200，started=false，SERVICE_READY_PLUGIN_LINK_NOT_VERIFIED。
- 当前ngrok日志1558行：过滤正常join connections后，仅观察到18:21建立session和started tunnel，无所查日志中的重连/配额/认证错误。日志级别和覆盖有限，不能据此保证外部路径始终健康。
- 仅只读查询OAuth表结构、行数和expires_at：当前仍存在未过期access token及refresh token；未读取或输出token内容/哈希、client秘密或Owner凭据。不能据此认证客户端全套刷新行为。
- D原生open_workspace最终成功，workspace_id=ws_9cc8f3af26；read(channel-probe.txt)返回D_CHANNEL_PROBE_R6_OK；hostname返回DESKTOP-4A1EGTM。进程退出结果另以原生write_stdin读回。

## 处理
只读诊断、复用原固定入口；未重建插件、未更换URL、未重启服务/Windows、未修改代理/网络/OAuth配置，未停止其他任务。恢复后应默认回到D，不因短时故障每天重建固定入口。

## 已知薄弱点
当前ensure-fixed能在本地端口拒绝连接时启动原配方，但本地OPEN且公网失败时只写DEGRADED并退出2，不执行公网故障恢复。这不是自动修复所有网络中断的成熟认证。此次公网自行恢复，不应加猜测性重启来掩盖问题。后续若同类故障持续，保留连续公网失败、ngrok session/endpoint证据，再按成熟诊断选择隧道级恢复；不改全局代理。

## 官方依据
https://ngrok.com/docs/pricing-limits/free-plan-limits ：免费endpoint无固定运行超时；分配的dev domain在agent重启后不变。这只能说明机制，不能取代本机实测。
https://github.com/ngrok/skills/blob/main/skills/troubleshoot-ngrok/SKILL.md ：按错误及live state区分endpoint、agent、上游与认证，不凭猜测重建。

## 后续现场捕获（覆盖前面的瞬时恢复结论）
- 22:25:46 ngrok: session closed, starting reconnect loop；err=read EOF from remote peer。
- 随后D原生read/write_stdin均返回404，payload明确The endpoint ... is offline，ERR_NGROK_3200；按官方说明这是端点离线，不是文件不存在或Owner密码错误。
- 22:26:11与22:26:21 heartbeat timeout。
- 22:26:21 failed to reconnect session：failed to send authentication request: failed to fetch CRL. errors encountered: timed out fetching CRL。
- 22:26:32 client session established、tunnel session started；可见离线区间约46秒，只覆盖此轮有明确日志的断开，不是整次故障总时长。
- 复测CRL HTTP和HTTPS均200、743字节，约456ms和1820ms。当前无证据支持持续80端口阻断，不猜改crl_url；未关闭证书吊销校验。
- 复测同一D原生read返回D_CHANNEL_PROBE_R6_OK；新hostname命令返回DESKTOP-4A1EGTM、exit_code=0、服务端369ms。
- 初次hostname轮询先Internal error，后遇3200；恢复后旧session579已不可查询，保留Unknown process session，不把前次结果伪填0。最终签收依据新命令真实0退出。
- 原ensure-fixed被调用一次以检查原配方，started=false，写DEGRADED；没有重启进程。原ngrok重连恢复，无手工重建插件或改配置。

状态：NATIVE_RECOVERED_PASS_AT_CHECK / LONG_TERM_STABILITY_NOT_PROVEN。整机重启及长期稳定不由此次短测推定。

## 后续故障处理依据
https://ngrok.com/docs/errors/err_ngrok_3200
https://github.com/ngrok/ngrok-docs/blob/main/gateway/agent/config/v2.mdx
官方支持在明确80端口受阻时使用crl_url=https://crl.ngrok-agent.com/ngrok.crl（3.39.7及以后），保持CRL签名验证。当前HTTP/HTTPS均通，暂不改变运行配置；不得用crl_noverify绕过校验或把改全局代理当默认修复。

