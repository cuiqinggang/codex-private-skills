# GPT直连Windows双路执行桥 v0.3.4｜Remote 免费额度运营 V1.0 现实验收

DATE=2026-10-13
SKILL=skills/extreme-time-automation-bridge/SKILL.md
POLICY=skills/extreme-time-automation-bridge/REMOTE_DCR_QUOTA_OPERATIONS_V1.md
SCRIPT=skills/extreme-time-automation-bridge/bootstrap/Invoke-Remote-Quota-Route-Gate.ps1
VERSION=0.3.4
RULE_STATUS=ACTIVE_IN_SKILL
PREFLIGHT_SCRIPT=PASS
REMOTE_SERVICE_CALLS_DURING_TEST=0
AUTO_INTERCEPTOR=NOT_INSTALLED
REBOOT_PERSISTENCE=NOT_TESTED
FINAL_SCOPE=ROUTING_POLICY_SCRIPT_ONLY

## 实际测试方式
1. 在既有 Windows 电脑 DESKTOP-4A1EGTM，经用户自建 `mcp__GPT_Windows_MCP_Bridge__start_process` 启动原 Windows PowerShell。
2. 通过 Windows 本地已获授权的 `gh api`，从私有 GitHub 权威仓库读取**刚提交的现行**路由脚本正文并 Base64 解码到 Windows TEMP 临时文件。
3. 原生 Windows PowerShell Parser 解析通过；调用本机 PowerShell 7 `pwsh -NoProfile -File` 逐个运行临时文件，验证返回 JSON 的 `selected_route`；错误即停止。
4. 逐一核验完毕，测试临时文件在 finally 中删除；未接触真实 Remote Desktop Commander 托管命令、未修改生产代理/隧道/Runner/用户浏览器。
5. 第 1 轮 10/10 PASS；发现“单次预估将跨过 8000 紧急预留线”的边界风险后最小修复（`predicted > 8000` 即触发紧急授权），重新执行扩展套件。

## 第 2 轮正式覆盖（15/15）
| 场景 | 预期 | 真实返回 |
|---|---|---|
| R 额度耗尽，A/B 可用 | A，阻断 R | PASS |
| A 可用的普通交互 | A | PASS |
| 长任务且 B 有适当业务通道 | B | PASS |
| A/B 不适用，R 已用 6000 | R + Yellow 提醒 | PASS |
| R 已用 7999，预计 1 次 | R（到8000为止） | PASS |
| R 已用 7999，预计 2 次 | BLOCKED | PASS |
| 同上，经用户明确紧急授权 | R | PASS |
| R 已用 8000，无授权 | BLOCKED | PASS |
| R 已用 8000，有明确紧急授权 | R | PASS |
| R 已用 9500，无授权 | BLOCKED | PASS |
| R 已用 9500，有明确紧急授权且余额充足 | R | PASS |
| R 已用 10000 | BLOCKED | PASS |
| 官方用量未知且 A/B 不可用 | BLOCKED | PASS |
| A 不可用而 B 可用，R 耗尽 | B | PASS |
| 用户错误要求 R 而 A 可用 | A + R_WOULD_WASTE_QUOTA 警告 | PASS |

真实标志：`VALIDATION_FINAL=15/15;NO_REMOTE_CALLS=TRUE`。
使用 `mcp__GPT_Windows_MCP_Bridge__read_process_output` 再次独立回读该 Windows 执行进程，`Process completed with exit code 0 (runtime: 19.51s)`。

## 此次改动确切达到的边界
- **已实现**：原 SKILL.md 第一屏必读；正式操作附则；双路旧页面覆盖优先级；纯判路辅助脚本；预算阈值与预估跨线保护；已验证的提醒输出；变更日志。
- **未实现**：在 OpenAI/ChatGPT 或 Remote Desktop Commander 平台部署不可绕过的自动工具调用拦截器、跨会话自动加载、自动获取准确官方剩余额度、真实用量账本、自动月度清零、开机恢复及 7/30 天实际运营效果。
- 未来每次载入该技能包的任务，必须在 Remote 官方调用**之前**进行本规则判路并发出提醒；如果其他页面未加载该技能包，此静态仓库文件**不会**魔法般介入。任何自动执行器接入需另做最小授权部署与独立验收。
- 2026-10-13 Remote 的 `who_am_i` 原始回执 `remote_calls_left_pct=0`，因此当天 `R=QUOTA_BLOCKED`；这一事实与本地 MCP 统计的 8733 总调用无直接对应。
