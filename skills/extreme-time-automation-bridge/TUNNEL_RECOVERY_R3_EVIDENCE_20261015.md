# GPT直连Windows双路执行桥 V1.0.1｜R3 独立取证与短周期验收（2026-10-15，北京时间）

STATUS=PARTIAL_PASS; NOT_FINAL_STABILITY_ACCEPTED
PATH_A=C:\AI\GPT-Windows-Bridge-B
CONSTRAINTS=不修改FlClash/Windows代理/浏览器；不读取或保存Runtime Key；单Tunnel ID不得双实例；不以一次健康/五次短测冒充断线恢复

## 1. 故障与进程时间线（实测）
- 2026-10-14 23:45:03：R2防护注册、原PID38324暂停；23:45:47恢复；23:45:48保护任务清理。本地凭证 `persistence/Tunnel-Pause-R2.jsonl`。
- 23:46:29：原隧道日志进入多个组件的 `OnStop`，具体触发条件**未查明**；不能断言是网络波动、暂停测试直接致死或客户端代码崩溃。
- 23:50:46：健康日志记录 `PROCESS_MISSING`，PID38324确实不存在。
- 23:55:25：新PID42388启动；23:55:47为 `MCP_NOT_INITIALIZED`；次日00:00:48 `HEALTHY`。
- 后续探测PID42388已不存在，下一次主通道操作返回原始 `409 MCP server is not initialized; send initialize and notifications/initialized`；这说明端到端初始化异常仍出现过，不等于永久性断线。
- 2026-10-15 00:05:26：第三个PID17876启动；00:08:52 GitHub独立Windows Runner读取 `TUNNEL_COUNT=1`、PID17876，原R2恢复guard不存在、R2 state不存在、临时防火墙rule=0。真实运行 [GitHub Run 38595535165](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38595535165)，结果success。
- 00:10:46 / 00:11:25：PID17876的 `MCP_STATE=initialized`、`HEALTH_READY=True`、控制平面连续轮询失败0，`initialize_epoch`达27；健康脚本判为HEALTHY。
- 进程重启是谁触发的**未知**；此前没有发现自动启动专用Tunnel的计划任务，不能宣称无人值守恢复PASS。

## 2. 官方通知shim：文件与运行进程必须分离验收
- 客户端 `tunnel-client.exe v0.0.16 run --help` 真实退出码0，存在 `--mcp.stdio-send-initialized-notification`。
- 00:08:13正式启动器 `Launch-OpenAI-Real-MCP.ps1` 已被更新，SHA256=`B825462C8C0E94194B6022B60035BA6D0E6A0E5F7C016FF346540A059744BA35`，PowerShell ParseErrors=0。
- 当前运行PID17876于**00:05:26**创建，主MCP通道Windows实测该进程命令行 **SHIM_FLAG=False**；因此虽正式脚本已有参数，**该正在运行的进程没有使用此参数**。补丁现场效果仍 `NOT_TESTED`，严禁将后续5次读取PASS归因于shim。
- 独立Runner以NETWORK SERVICE取不到该用户进程CommandLine，返回 `ARGS_READABLE=False`；这不反驳本机当前授权MCP的标志检测。
- 官方shim只在成功initialize回应后补发 `notifications/initialized`，不能合成缺失的initialize，也不能启动已退出的进程。官方依据：<https://github.com/openai/tunnel-client/blob/master/docs/configuration.md>。

## 3. 真正来自ChatGPT的五次连续只读调用
同一次有效主通道会话中，独立调用 `GPT-Windows-MCP-Bridge.read_file` 读取正式启动器头12行五次，逐次全部返回预期内容，未使用重试补偿：
- R3-1: 5.069秒 PASS
- R3-2: 6.896秒 PASS
- R3-3: 5.337秒 PASS
- R3-4: 5.265秒 PASS
- R3-5: 6.158秒 PASS

判定：`CURRENT_BASIS_READ_5_OF_5=PASS_SCOPED`；`SHIM_RUNTIME_REALITY=NOT_TESTED`；`NETWORK_INTERRUPTION_AUTO_RECOVERY=NOT_ACCEPTED`；`PROCESS_EXIT_AUTO_RECOVERY=NOT_IMPLEMENTED/NOT_ACCEPTED`；`LONG_STABILITY=NOT_ACCEPTED`。

## 4. 防重复与下一个验收门
- 本轮仅做只读 Windows诊断、五次真实读取、官方CLI帮助/脚本语法检查；**没有**重启或暂停现有隧道，也没有改 FlClash、系统代理、浏览器和密钥。
- 更新了现有 GitHub 只读应急取证工作流 `.github/workflows/tunnel-r2-oob-readonly-20261014.yml`，commit `74c6610a78ac26a92f327af7e0fbac5c91d816c2`，实际Run 38595535165成功。此工作流不会停止或自动恢复隧道。
- 为防止误把“文件已含参数”当“进程已启用参数”，后续任何Reality验收先核实**该启动PID**的命令行参数或可证明等价的正式启动回执。
- 只有在合法的本地交互式 Runtime Key 输入、原进程安全退出、唯一实例/回滚准备均满足后，才能受控启动带shim的正式客户端，再执行与基线同构的8次只读和不少于5次独立运行验收。
- 继续分开验证：①网络或单通道短暂中断后同PID自动恢复；②进程退出后的无人介入重建和MCP重新初始化。当前无已验收的无人值守合法凭据恢复路径，不得为测试强行终止生产进程。
- 遵守现有技能包的安全限制：此前受阻的DPAPI隐藏Supervisor方案不能换渠道绕过；不从进程环境/内存获取密钥。
