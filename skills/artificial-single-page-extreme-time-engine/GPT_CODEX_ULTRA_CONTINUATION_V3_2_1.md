# GPT CEO＋Codex Ultra 连续运行层 v3.2.1｜审批已存在但本地合同未同步修正
METHOD_VERSION=3.2.1
INHERITS=GPT_CODEX_ULTRA_CONTINUATION_V3_2.md
ACTIVE_RUNTIME=3.1.0_UNCHANGED
ENGINE=ENGINE.md@28_UNCHANGED
TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011
RELEASE_STATUS=REAL_STARTUP_VERIFIED;END_TO_END_PENDING
RELEASE_DATE_LOCAL=2026-10-12
EVIDENCE=GPT_CODEX_ULTRA_CONTINUATION_V3_2_1_REALITY.md

## 本次事故：系统没有崩溃，但业务不可推进就是停机故障
GOOD：V007已经事实冻结，Freeze SHA=B6EB232DC1F96B1138792FD50FAC759893290581380C3681D305B669D6FB742A；Manifest SHA=A30F24B05485ED03FC5C67CED22E914A5E0659275FC540C59C28A03675EF94D5；官方GitHub和本地指针一致，Codex旧节点exit0；Windows原生计划任务Ready，脚本语法正常、无INFLIGHT。
BAD：GitHub新审批`GPT_CEO_DISPOSITION_V007.md`与`CEO_APPROVED_CODEX008_FULL_COVERAGE.md`已经保存，本地文件及Git Blob也一致，但真正被Windows runner读取的`NEXT_NODE_PROMPT.md`仍是旧CODEX008_OFFLINE_DELIVERY_CLOSEOUT的`PROPOSED_ONLY`。每次Task Scheduler触发就写`MOTHER_NEEDS_GPT.flag`并exit0，不启动Codex。
FIRST_DELTA：**决策文件≠执行合同**。GitHub CEO批准→本地正式批准文件→本地NEXT_NODE_PROMPT启动输入→旧等待flag归档是四个不同步骤；前两步完成不意味着后两步完成。
修复：读回已核实的CEO合同，先备份旧NEXT提示词，直接用已批准的正式`CEO_APPROVED_CODEX008_FULL_COVERAGE.md`全文替换本地`NEXT_NODE_PROMPT.md`；通过`git hash-object`核对与GitHub blob一致，准确校验NODE_ID与`NEXT_DISPOSITION=CEO_APPROVED_CODEX008_OFFLINE_ONLY`；只有无存活同任务Codex、无未知INFLIGHT、V007哈希正确，才归档旧`CEO_NEXT_SCOPE_DECISION_REQUIRED`标记。最后调用**原计划任务**一次，而不是直接启动第二Codex或新建调度。
REALITY：2026-10-12 00:56:53 +08原计划任务成功触发；00:57:05返回唯一Codex PID41664，模型入口沿用`gpt-6.1-sol`和`model_reasoning_effort=ultra`；00:57:25日志`Codex-20261012-005654.log`增长为4764字节，无NEEDS_GPT、无PAUSE、INFLIGHT已建立，V007未重做。

## 固化防复发（在第3.2版基础上新增）
1. 任一CEO批准写入成功时，必须将GitHub官方审批文件、Windows本地审批文件、以及**Windows实际启动输入**分别校验。特别是`NEXT_NODE_PROMPT.md`的内容必须与最终授权合同同一任务/节点/范围/版本，且明确`CEO_APPROVED`；不同步不算授权传递成功。
2. **不再留旧`PROPOSED_ONLY`启动提示词**：老提案只保存备份。不同方向的CODEX008提案不能通过仅修改状态词来批准，必须用批准的完整合同替换，避免执行错误业务。
3. `MOTHER_NEEDS_GPT.flag`不是GPT调用器，不能自行把GPT拉来审批；发生`CEO_NEXT_SCOPE_DECISION_REQUIRED`必须由已授权GPT CEO接手，不能假装自主恢复或取消实际审批。
4. 清理标记仅限经真实事实核验后的本次**特定已解决等待**，保留归档，不为启动而无差别删除暂停/INFLIGHT/真实故障。
5. 原计划任务、代理、Codex CLI入口、引擎合同、冻结业务文件均保持不变；小故障只改最小状态差分，不重造系统。
6. 执行恢复至少两级证明：`STARTUP_PASS`（唯一PID+新日志+INFLIGHT）；`NATURAL_NODE_PASS`（真实业务/独立验收/Freeze+GitHub回读）；`AUTOCONTINUE_PASS`（下一合法节点无需重复手工转交）。当前只认`STARTUP_PASS`，不将V008或全公司FINAL_VALID提前改成YES。
7. 后续若每个自然节点都因新批准要求停住，属于**CEO接管尚无自动触发机制的连续性缺口**；可评估官方现成通知/任务连接器，但不能未经批准放宽CEO授权，也不能声明已经无人值守。

## 版本分离
本方法修订为v3.2.1。Windows正式执行脚本仍v3.1.0，引擎28，业务Freeze仍V007（截至00:57实测）。新方法发行不能更改业务指针。
