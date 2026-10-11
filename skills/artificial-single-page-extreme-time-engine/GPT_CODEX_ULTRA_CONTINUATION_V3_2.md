# 《GPT CEO＋Codex Ultra 连续运行层》第3.2版｜已验证入口恢复与防复发
METHOD_VERSION=3.2.0
PUBLISHED_AT_LOCAL=2026-10-12
METHOD_SCOPE=GPT_CEO_TO_WINDOWS_NATIVE_SCHEDULER_TO_CODEX_ULTRA
IMPLEMENTATION_RUNTIME=3.1.0
BUSINESS_VERSION_IS_INDEPENDENT=YES
ENGINE_REF=ENGINE.md@28_UNCHANGED
TASK_CASE=POLSIA_CAPABILITY_REPLICATION_20261011
EVIDENCE=GPT_CODEX_ULTRA_CONTINUATION_V3_2_ACCEPTANCE.md
STATUS=RELEASED;STARTUP_REALITY_PASS;NODE_END_TO_END_PENDING

## 1. 唯一目标与原则
恢复或新增自然节点时，首选 **成熟的已验证启动入口**，不得因为一个局部报错重新注册Windows任务、新建桥接/调度器/恢复引擎、重跑旧节点或更改FlClash代理。GPT负责CEO决策；Windows Task Scheduler只触发；本地CONTINUE_EXISTING_CODEX.ps1负责合法性/Exactly-once；Codex CLI运行获批节点；GitHub保存权威合同、不可变Freeze、版本和CEO决策；本地保存程序、日志和实际媒体。
区分四个版本：METHOD_VERSION（本文件v3.2.0）、RUNTIME_VERSION（已部署v3.1.0）、ENGINE_VERSION（任务锁第28版）、BUSINESS_FREEZE（V006直到007真实完成）。不能因方法升级自动把业务V006改为V007。

## 2. 2026-10-11/12 连续故障复盘（GOOD/BAD/FIRST_DELTA）
A. **Freeze本机路径误判**：GitHub Freeze basename不能直接拼到本机根目录；真实Freeze路径来自本地MOTHER_CURRENT，必须将路径限定在工作区并校验SHA/manifest/正式指针。
B. **CRLF正则失败**：`(?m)^MANIFEST_SHA256=([A-Fa-f0-9]{64})$` 在CRLF末尾误判；兼容`\r?$`，保留错误SHA拒绝逻辑。同样覆盖FINAL_VALID=YES。
C. **无新Freeze误判**：2026-10-11 CODEX006正常exit0、V006已真实Freeze；下一轮因007仍为PROPOSED_ONLY却再次启动Codex，只读审查后exit0没有V007，旧runner错误写CODEX_EXIT_WITHOUT_NEW_VERIFIED_FREEZE。修复为启动前授权门；等待CEO决策≠执行失败。
D. **候选脚本语法错误**：v3.1.0最初由字符串替换误用特殊序列生成了断裂PowerShell源码（`\r?$logDir`），Parser报告13个派生错误。修复后Parser=0且授权/哈希只读回归通过；**任何发行文件必须先测试后升级指针、后切换live**。
E. **部署半完成**：旧脚本备份、v3.1.0正式live替换和故障INFLIGHT归档成功，但发布流程遗留MOTHER_PAUSE.flag，GitHub CEO已批准007而本机GPT_CEO_DISPOSITION_V006.md与NEXT_NODE_PROMPT.md仍未同步，所以Windows计划任务Ready却始终快速退出。真实首个失败点在**GitHub CEO→本地合同同步与解除临时暂停**，不是GPT API断连、Codex拒绝授权或Windows计划任务损坏。

## 3. 运行前只读决策门（按此顺序）
1. **精确取权威**：从GitHub官方Contents读取任务CURRENT、VERSION_CURRENT、对应Freeze和CEO_DISPOSITION，禁止先去C盘找方法；本地读取相应真实FREEZE/MANIFEST、NEXT_NODE_PROMPT与脚本。
2. **冻结/版本一致**：TASK_ID、Vnnn、FREEZE_ID、本地Freeze SHA、Manifest SHA及GitHub Blob原样对账；若UNKNOWN，不重发旧业务。
3. **执行实例与原计划任务**：查看`Polsia-Codex-Mother-Continue`真实action、状态、Codex PID、INFLIGHT和停止标记；同任务正在运行禁止再启动。不要因log暂时0字节认定失败，要结合原生session JSONL、最新文件和日志。
4. **授权与合同一致**：下一任务文本须包含明确`NEXT_DISPOSITION=CEO_APPROVED_CODEXnnn_...`，并与GitHub已读取的同一范围CEO决策一致。只在本机启动时看到批准，不等于GitHub真的授权；未经批准只报告`CEO_NEXT_SCOPE_DECISION_REQUIRED`，**不创建INFLIGHT、不启动Codex**。
5. **正常安全等待不等于停机失败**：MOTHER_NEEDS_GPT.flag或其它通知只是文件，不是GPT API；如无已实现的自主CEO触发，必须如实标为等待CEO接管，不宣称会自动通知、自动审批。

## 4. 最小现实恢复｜源头复用，不重建系统
- 原入口：REGISTER_NATIVE_CONTINUATION.ps1注册的Windows Task Scheduler `Polsia-Codex-Mother-Continue` → `C:\Program Files\PowerShell\7\pwsh.exe` → `C:\AI\Polsia-Codex-20261011\CONTINUE_EXISTING_CODEX.ps1` → 原Codex CLI exec。
- 准备：确认V006 DONE、GitHub CEO-D006批准007（`GPT_CEO_DISPOSITION_V006.md`）、无人执行、无不明INFLIGHT；不要重跑V001-V006。
- 通过已连接的官方Windows远程文件工具**直接写**本地CEO决策，并逐字节检验Git Blob SHA；用精确小范围编辑更新NEXT_NODE_PROMPT的批准行与正文，避免自研传输、重新注册计划任务或巨大脚本替换。
- 如升级live runner，先在无活动Codex时备份旧脚本，先Parser与只读回归PASS，再将同SHA的文件安装到原入口；Task Scheduler动作、触发器、代理不变。
- 运行层临时MOTHER_PAUSE.flag有严格清理义务：只有检查其值是本次受控迁移、已存在备份、脚本SHA一致、CEO授权已同步且没有活动进程/UNKNOWN后，将其**归档（不是覆盖或遗忘）**。任何阻塞保留暂停，报告真实状态。
- 通过**现有计划任务**仅触发一次，不直接发第二份Codex命令。验收真实PID（只有一个）、`gpt-6.1-sol/ultra`、新时间戳INFLIGHT、新原生日志增长、CODEX007新隔离目录文件。
- 完整业务恢复只有在CODEX007真实交付、独立审核、GitHub不可变V007 Freeze回读与下一节点安全自动接续后才为`END_TO_END_PASS`；本轮仅认定`STARTUP_RECOVERY_PASS`。

## 5. 防复发发布门（任何新版不可跳过）
A. 基线差分：GOOD旧版本备份；只改一处明确FIRST_DELTA，不修改无关功能。
B. 脚本安全：PowerShell Parser=0；LF/CRLF、正确/错误SHA、CEO批准/未批准、旧INFLIGHT、无重复进程测试PASS。JS生成源码必须用函数替换而不是误用`$'`特殊替换序列。
C. 分层交付：先GitHub新增版本文件+独立真实readback；再本机隔离副本验收；再安全节点备份部署；再核对原计划任务action；**最后才可更新正式版本指针**。
D. 验收门：至少区分`SCRIPT_TEST_PASS`、`AUTHORITY_SYNC_PASS`、`STARTUP_REALITY_PASS`、`NATURAL_FREEZE_PASS`和`CROSS_NODE_AUTOCONTINUE_PASS`，不能拿单一启动PID或R01样例冒充母任务VALID。
E. exactly-once：DONE不得重做，NOT_DONE受控执行，UNKNOWN先对账；任何被安全检查阻断的写入不得绕安全检查改走非授权渠道，保留冻结不宣称恢复。
F. 状态漂移：若已登录/活跃执行器，由当前自然节点继续，绝不因同步新方法停其进程；Checkpoint不计Vnnn，Freeze才计业务版本。
G. 结束动作：把原先临时标记/备份/运行合同逐一核对，**部署任务不可在暂停尚未清理、审批不同步时标记成功**。

## 6. 本次可审计现实基线与限制
2026-10-12 00:00:35 +08，原计划任务Ready、V006的Freeze/Manifest核验通过、无Codex进程、临时Pause存在且CEO文件尚未同步。随后采用Remote Desktop Commander官方read/write/edit接口，写入CEO-D006到Windows且`git hash-object`得到与GitHub相同Blob SHA：`947f35c51017183bcb29a65be7071bbe842af614`；本机NEXT节点变更为`CEO_APPROVED_CODEX007_OFFLINE_ONLY`；归档临时Pause后原计划任务在00:02:59只触发一次。00:03:13实测唯一Codex PID 16632，模型gpt-6.1-sol、effort ultra，计划任务Running、INFLIGHT新增，00:04:20日志已增长73,905字节，无NEEDS_GPT。业务V007事实冻结仍待执行完毕，不能提前声称成功。
上述方法是**已通过现实启动恢复**的成熟最小补丁；不是对72小时断电恢复或完整Polsia公司系统的认证。
