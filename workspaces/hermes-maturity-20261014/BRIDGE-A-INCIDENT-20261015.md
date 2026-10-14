# A路故障差分与成熟方法边界（2026-10-15）
STATUS=FIRST_DELTA_ISOLATED;A_TOOL_CALL_FINAL_VALID=NO
SOURCE_METHOD=skills/extreme-time-automation-bridge/SKILL.md@3.0.0
A_RECOVERY_SOP=skills/extreme-time-automation-bridge/TUNNEL_AUTORECOVERY_V2_20261015.md
SCOPE=本次HERMES-ECO-20261014接续，只记事实，不升级全局版本。

## 已验证的事实
1. V3.0 B路官方Artifact 5/5 PASS，不包括A路MCP初始化、进程退出恢复、开机自启动认证。
2. 先前额外执行的临时恢复验证脚本 `C:\AI\GPT-Windows-Bridge-B\persistence\Validate-OneTunnel-Recovery-20261015.ps1` 含对旧PID17876的定向Stop-Process；随后原回执 `NO_AUTORECOVERY_WITHIN_100_SECONDS`。不能将该次中断归咎于偶发网络波动。该自建脚本与现有A路SOP的“不主动终止正常实例”原则冲突，禁止再运行，不删除证据。
3. 用户重新连接后，主通道实测到PID46772、同Tunnel ID、单实例；用户权限现场证实该新进程携带官方 `mcp.stdio-send-initialized-notification` 标志。不能再沿用旧PID17876“没有shim”的结论。
4. 通过ChatGPT调用A工具时真实出现 `409 mcp_initialization_required`、`UNAVAILABLE Connection failed` 及工具内部失败；某些读取曾成功，因此不是“所有调用一直失败”。
5. 已复用成熟GitHub B独立只读工作流 `.github/workflows/tunnel-r2-oob-readonly-20261014.yml`，对历史Run 38595535165的inspect Job 115961165293执行一次原生Rerun。新Job 116016675767完整PASS；未写脚本、未断线、未重建进程。
6. B真实回执UTC 2026-10-14T18:02:43：Windows上 `TUNNEL_COUNT=1`, `PID=46772`，父PowerShell存活，临时防火墙规则0，历史R2临时guard不存在；最近健康采样 `ready=true`，`control_plane=polling`，`poll_failures=0`，`mcp=initialized`，`mcp_child=running`，`response_delivery=accepted`，`dispatcher_failures=0`，`mcp_generation=2e038e1e778e4655586a1aae4dfdee04`。
7. B Runner身份无法读完整进程参数（ARGS_READABLE=false）；此项不能推翻先前用户权限下对shim标志的直接核验。
8. 上述健康回执不等于ChatGPT端一次真实read_file成功。当前A端到端依然NOT_ACCEPTED。

## 官方成熟方法的唯一故障门
- 官方 `openai/tunnel-client/docs/configuration.md`：旧式tools/call前必须成功initialize与notifications/initialized，缺条件返回409 / -32002。客户端shim只能在成功initialize之后补发通知，不能自己建立缺失的initialize，也不能重试被拒绝的请求。
- 官方 `docs/troubleshooting.md` 与 `plugins/tunnel-mcp/skills/tunnel-mcp/references/troubleshooting.md`：依次用现有进程、health/ready、control-plane、MCP child_generation、response-delivery、dispatcher和真实工具回执分层对账。不要以health=200推出端到端功能。
- 官方既有受管 `runtimes connect/status` 是未来单实例生命周期管理候选，不与当前run/已注册Supervisor并存运行；切换仅在授权维护窗口按SOP单次、有回滚、且先验证凭据可用后进行。
- 若客户端初始化缺失出自ChatGPT调用方，Windows本地脚本不应伪造initialize；需通过平台支持的连接初始化或提交脱敏官方故障证据调查。

## 未完成 / 限制
- 尚无本轮有效A端到端连续8次读取与5次独立运行；未证明A的409已修复、Supervisor自动恢复、开机登录恢复或长期无故障。
- 本轮未更改FlClash、Windows代理、认证、Runner配置、已登录浏览器及线上隧道。不得重复执行临时Stop-Process、盲目更换凭据、盲重发UNKNOWN副作用任务。
- 当前停止点：Windows本地链路健康且A调用失败；需要调用方初始化证据或一次正式远端read_file成功才更新A状态。
