# GPT CEO＋Codex Ultra 连续运行层方法 v3.2.2｜双门启动恢复差分
METHOD_VERSION=3.2.2
INHERITS=GPT_CODEX_ULTRA_CONTINUATION_V3_2_1.md
ACTIVE_RUNTIME_VERSION=3.1.0_UNCHANGED
ENGINE_VERSION=28_UNCHANGED
BUSINESS_LAST_VERIFIED_FREEZE=V007
TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011
RELEASE_DATE_LOCAL=2026-10-12
REALITY=CODEX008_STARTUP_PASS;BUSINESS_FREEZE_PENDING

## 本次同一自然节点发生两次真实阻断，必须分开
### A. 批准没有抵达真正的启动输入
GOOD：GitHub `GPT_CEO_DISPOSITION_V007.md`和`CEO_APPROVED_CODEX008_FULL_COVERAGE.md`已审批、在Windows本地存在且SHA吻合；原Windows任务Ready、无Codex进程、V007真实Freeze和Manifest验证正确。
BAD：Windows `NEXT_NODE_PROMPT.md`仍包含旧`PROPOSED_ONLY`，runner写`MOTHER_NEEDS_GPT.flag`并退出，周期触发却不能推进。
FIRST_DELTA：审批文件 ≠ 实际启动合同。
FIX：备份原`NEXT_NODE_PROMPT.md`，用官方GitHub可核对的完整正式合同原文写入，`git hash-object`确认一致，归档已证实属于CEO审批等待的标记，然后仅由原`Polsia-Codex-Mother-Continue`触发一次。00:57:05 +08 看到Codex PID41664启动。

### B. 启动后被任务定位门立即拒绝
GOOD：CODEX008范围和审批正确；原新Codex日志确认为gpt-6.1-sol/ultra，旧V007不变。
BAD：Codex因收到的合同没有`【页面名｜任务名｜序号】`标签，返回`LOCATOR_GATE=BLOCKED` / `ACTION=STOP`、要求补齐标签。Codex exit0但没有V008、新文件；runner正确保留`CODEX_EXIT_ZERO_WITHOUT_NEW_VERIFIED_FREEZE`与INFLIGHT供GPT对账。
FIRST_DELTA：批准的完整业务合同未包含当前Codex全局定位门的必填标签，导致`EXIT=0`被误理解为有效完成。
FIX：从合法来源读取原批准合同，制作仅增加定位元数据的`CEO_APPROVED_CODEX008_FULL_COVERAGE_LOCATOR_FIX.md`，保留原合同全部业务内容和权限不变；文件开头加精确三字段定位`【Polsia执行页｜POLSIA_CAPABILITY_REPLICATION_20261011｜CODEX-008】`，末尾另附四字段项目标识。GitHub新Blob=`8ce0b1a313101ca201cc432af2bffa58c057e984`；Windows的`NEXT_NODE_PROMPT.md`按官方文件精确写入并`git hash-object`核相同。确认首次STOP无业务文件、无进程、V007冻结和SHA未变，再归档前一轮两个标记；经原计划任务00:01启动，01:01:02 +08 唯一新Codex PID43416、新INFLIGHT、新日志，前一轮进程未重启/复用。

## 防再犯：任何新自然节点事先做“双门合同验收”
1. 授权门：CEO决策已保存且与本机授权文件、`NEXT_NODE_PROMPT`三方TASK_ID/NODE_ID/FREEZE_ID/业务限制一致；`NEXT_DISPOSITION=CEO_APPROVED_...`。
2. 定位门：读取实际Codex全局定位格式要求，提示词必须同时明确`【页面名｜任务名｜序号】`的精确当前标识；项目若采用四字段也保留兼容标识。缺任何一门**先修合同再启动Codex**，不靠实际启动试错。
3. 原启动链不变：Task Scheduler→`CONTINUE_EXISTING_CODEX.ps1`→原`codex.cmd exec`；不注册第二调度，不改网络代理/浏览器，不发任何外部真实业务。
4. 同任务Exactly-once：本地最后Freeze+Manifest及GitHub版本一致；NO_UNKNOWN_INFLIGHT；只在日志明确是定位门止步、业务输出未写且无存活进程时归档失败标记；其它UNKNOWN不盲重跑。
5. 成功等级分开：`STARTED`=PID+INFLIGHT；`EXECUTING`=日志持续与真实工具业务证据；`NATURAL_FREEZE_PASS`=V008事实Freeze+非作者验收+GitHub精确回读；`CONTINUOUS_PASS`=安全自动进入下一获批节点。**退出码0不是业务成功证明**。
6. 别把`MOTHER_NEEDS_GPT.flag`当真正能自行唤起GPT的连接；没有独立已测试CEO接管触发时，仍须CEO授权流程。不能为避免停住而绕开审批。
7. 版本隔离：方法v3.2.2；当前Windows执行脚本v3.1.0；任务ENGINE28；实际业务Freeze V007。在业务V008真实冻结前不改其版本指针。

## 真实记录
00:55 V007 LOCAL Freeze SHA`B6EB232DC1F96B1138792FD50FAC759893290581380C3681D305B669D6FB742A`，Manifest SHA`A30F24B05485ED03FC5C67CED22E914A5E0659275FC540C59C28A03675EF94D5`。
00:56:53 原调度首次触发启动PID41664；00:57:31 Codex因LOCATOR_GATE=BLOCKED stop，退出0且未产生业务节点。
00:59:57 确认进程0、旧V007不变、CODEX008目录不存在，已准确对账。
01:00:26 本地修正后的提示词Git Blob与GitHub完全相同，CEO批准和三字段定位均存在；归档上轮故障标记。
01:00:49 再由原调度触发；01:01:02 实测唯一PID43416，01:01:44同一PID运行且新日志增长87566字节，INFLIGHT存在、NEEDS_GPT不存在。
截至01:01:44，尚未有V008自然节点Freeze证据，不可提前称全部修复长稳PASS。
