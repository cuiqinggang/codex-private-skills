# 《GPT CEO＋Codex Ultra 连续运行层》第3版（v3.0.0）
RUNTIME_ID=GPT_CODEX_ULTRA_CONTINUATION
VERSION=3.0.0
TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011
RELEASE_DATE=2026-10-11
RELEASE_STATUS=PUBLISHED_STAGED_NOT_YET_WINDOWS_ACTIVE
RELEASE_SOURCE=CONTINUATION_RUNNER_V3.ps1
RELEASE_TEST=CONTINUATION_RUNTIME_V3_REGRESSION.ps1
RELEASE_POINTER=CONTINUATION_RUNTIME_CURRENT.md
PREVIOUS_SOURCE=CONTINUATION_RUNNER_V2.ps1
METHOD_REF=ENGINE.md@28
CONTROLLER=GPT_CEO
EXECUTOR=Codex_Ultra
BUSINESS_FINAL_VALID=NO

## 1. 此版本到底升级了什么
此为 **GPT CEO/Windows原生任务/Codex Ultra执行器的连续运行层版本**，与业务自然节点 V005/V006 的 Freeze、引擎第28版、三人行第1版完全独立。保留成熟 Windows Task Scheduler 和 Codex CLI 作为已有执行底座，不新增自研调度、数据库、状态机、锁、恢复引擎或第二 Codex。GitHub 为方法与任务权威源，本地为实测运行源。

v3.0.0 复刻最后确认可靠的 V2 修复逻辑，只增加明确版本头和治理/回归协议，**无热替换行为、无参数或外部副作用变化**。不因发布新版本宣称下一自然节点跨节点回归已完成。

## 2. 已验证的重复失败 GOOD/BAD/FIRST_DELTA
- GOOD：CODEX-005 exit0，业务 ZIP/非作者审查通过；GitHub 的 V005 Freeze、CURRENT、VERSION_CURRENT 独立回读一致；本地Freeze及Manifest路径和SHA真实一致。
- BAD：旧Windows Runner 报 `CODEX_EXIT_WITHOUT_NEW_VERIFIED_FREEZE`，错误创建 `MOTHER_NEEDS_GPT.flag`，造成正常母任务自动接续停止。
- FIRST_DELTA：`Get-Content -Raw` 读取 CRLF 文本，`(?m)^MANIFEST_SHA256=([A-Fa-f0-9]{64})$` 错误返回False；该文本包含 `\r\n`，行末 `$` 前有 `\r`。
- FIX：`(?m)^MANIFEST_SHA256=([A-Fa-f0-9]{64})\r?$`；`MOTHER_FINAL_VALID=YES` 同样兼容 `\r?$`。原先远端Freeze basename拼接本地根目录的错误已经在V2被修复，V3继续保留本机真实路径/清单校验。
- 原故障相关历史 GitHub 补丁：`1e4e22dd6468c7ed455f6c0983cc84da575354b9`；GPT CEO V005事实核验及恢复决策：`GPT_CEO_DISPOSITION_V005.md`；其GitHub源回读确认 `8fb16fc05940b94729351ee23370b4c16f687b92`。

## 3. 修复后的校验合同
已存在的合法节点正常完成时，必须检验：Codex `CODEX_EXIT=0`；本地 `MOTHER_CURRENT.md` 实际更新且版本递增；本机母任务版本、GitHub对应版本指针与正式 `FREEZE_ID` 一致；Freeze是工作区内合法真实路径，含对应ID；Manifest是实际本地文件且SHA256等于当前母任务记录；文件 CRLF/LF 均能识别。若不一致，保存实际失败而非盲目启动下一实例。
若执行中、有 `INFLIGHT` 而结果未知、外部动作UNKNOWN、或明确权限/安全阻塞，保留证据进入 GPT CEO 复核。不得通过忽略校验/强删标志/换通道绕过。
自然节点业务结束只递增业务Freeze Vnnn；发布运行层 v3.0.0 **不能**伪造新业务节点、10/10整公司认证或FINAL_VALID。

## 4. 发布、部署、回退（三个不同状态）
1. `PUBLISHED`：官方GitHub存在V3脚本、此发行说明、回归脚本，逐文件readback一致。
2. `STAGED`：Windows只把V3脚本和测试副本放到新的版本目录，不修改当前计划任务动作，保证当前CODEX-006继续由已加载的V2脚本执行。
3. `ACTIVE`：仅在当前节点自然结束、Freeze及GitHub回读完成、无Polsia Codex执行进程/INFLIGHT且计划任务Ready时，备份live runner后在控制的安全窗口切换任务动作或本机live副本，再读回哈希、用只读回归脚本确认无差分；若发生未知状态绝不自动重复执行。必须单独记录激活时间、旧/新SHA和Task Scheduler动作，随后真实验证下一个跨节点启动。**未获取这些证据之前不得把PUBLISHED/STAGED冒充ACTIVE。**
4. 回退只能基于备份与官方记录，在相同无活动进程/非UNKNOWN安全门通过时执行；不得回滚已完成的业务Freeze，也不得重新派发已有业务。

## 5. 现实验收边界
无副作用测试：PowerShell语法、LF/CRLF、正确/错误SHA、YES终止标记、实际冻结只读比对和V2→V3行为相同核验；不触发Codex、不碰生产环境。
现实跨节点回归：由未来真实合法节点 exit0→事实Freeze和远端回读→自动清INFLIGHT→原任务正常转下一节点，才可记录 `CONTINUATION_END_TO_END=PASS`。72h观察和断电冷恢复尚需单独现实认证。
