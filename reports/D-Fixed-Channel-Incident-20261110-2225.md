# 固定D通道故障诊断与恢复

日期：2026-11-10，北京时间约22:20—22:26。入口Windows D 20261110-02。

## 结论
固定网址仍可用，未发现固定域名配置错误或自动到时失效证据。此次观察到公网访问瞬时超时/连接关闭，之后在没有重启服务、没有修改配置的情况下恢复。确切网络责任点（本机出口、运营商、ngrok边缘或客户端路径）未被独立定位，不把推断写成唯一根因。

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

状态：NATIVE_READ_AND_HOSTNAME_RETURNED；以原生退出码读回后完成最终签收。整机重启/长时稳定仍不由此次短测推定。
