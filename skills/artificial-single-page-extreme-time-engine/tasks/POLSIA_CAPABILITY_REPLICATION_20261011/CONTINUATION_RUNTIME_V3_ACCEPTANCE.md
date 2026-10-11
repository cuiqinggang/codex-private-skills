# GPT CEO＋Codex Ultra 连续运行层 v3.0.0｜发布验收回执
TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011
RUNTIME_VERSION=3.0.0
DATE_LOCAL=2026-10-11
RESULT=PASS_READONLY_RELEASE_REGRESSION
DEPLOYMENT=PUBLISHED_AND_LOCAL_STAGED
WINDOWS_ACTIVE=NO;CURRENT_RUNNER=CONTINUE_EXISTING_CODEX.ps1;V2_CRLF_FIXED
BUSINESS_FINAL_VALID=NO
REAL_NEXT_NODE_AUTOCONTINUATION=NOT_YET_VERIFIED_FOR_V3

## 本机真实执行返回
回归命令：PowerShell 调用 `CONTINUATION_RUNTIME_V3_REGRESSION.ps1`，指定 `CONTINUATION_RUNNER_V3.ps1` 为目标。输出如下：
```json
{"Result":"PASS_READONLY","Version":"3.0.0","Parser":"PASS","LF":true,"CRLF":true,"WrongHashRejected":true,"FinalYesCRLF":true,"FinalNoRejected":true,"CurrentLocal":"PASS_READONLY_LOCAL_SHA","CodexStarted":0,"SchedulerMutated":false}
```
同时将本机正在运行的 `CONTINUE_EXISTING_CODEX.ps1` 和V3去除版本头并标准化换行后比较，返回：
```json
{"V3LogicIdenticalToLiveV2":true,"TaskActionUnchanged":true,"TaskState":4,"Release":"3.0.0","Activation":"STAGED_ONLY","NoCodexSpawnByTest":true}
```
TaskState=4为当次Windows查询枚举值，不将其解释为节点已经结束或母任务已完成。同期CODEX-006使用既有V2恢复机制执行，不影响当前自然节点。
## 签收界限
- PASS的是运行层新版本发布和只读回归；没有运行V3正式驱动业务节点，没有对计划任务动作实施切换或热替换。
- GOOD：正确哈希、LF/CRLF和完成YES/NO的读取校验可正常解析，V3脚本与现有修复版V2业务控制逻辑相同。
- BAD：未修复V2曾把成功完成的V005误报为CODEX_EXIT_WITHOUT_NEW_VERIFIED_FREEZE。
- FIRST_DELTA：原CRLF文本中行末 \r 导致匹配的严格行尾正则错误为False。已采用 \r?$ 处理，并保持路径、SHA、权限和Exactly-once硬门。
- ACTIVE需待自然安全节点：无进程与未知INFLIGHT，真实Freeze和官方GitHub读回，原版本备份/实际动作变更及后续跨节点回归，不能因发布文件自动认定完成。
