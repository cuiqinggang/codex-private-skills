---
name: gpt-ceo-codex-ultra-continuation
description: 复用已配置Windows原生计划任务与Codex Ultra，在GPT CEO授权后按自然节点持续执行、精确冻结、失败对账和恢复。涉及自动接续、NEEDS GPT、旧版本卡住、授权不同步、升级脚本或暂停标记时使用。
---

# GPT CEO＋Codex Ultra 连续运行层｜v3.2.0

**唯一权威索引**：`cuiqinggang/codex-private-skills/main` 的
`skills/artificial-single-page-extreme-time-engine/GPT_CODEX_ULTRA_CONTINUATION_INDEX.md`。

**正式方法正文**：
`skills/artificial-single-page-extreme-time-engine/GPT_CODEX_ULTRA_CONTINUATION_V3_2.md`。

**实际发布验收**：
`skills/artificial-single-page-extreme-time-engine/GPT_CODEX_ULTRA_CONTINUATION_V3_2_ACCEPTANCE.md`。

## 接管入口
从GitHub读取上述索引和本任务`CURRENT.md`、`VERSION_CURRENT.md`、最后`Freeze`、CEO决策；再按授权设备官方连接器读取现有Windows计划任务`Polsia-Codex-Mother-Continue`、本地`MOTHER_CURRENT.md`、`NEXT_NODE_PROMPT.md`、真实日志与Manifest SHA。**不能从零造运行/持久化系统，不可为了自检重复Codex旧节点。**

## 必须先满足的现实门
- CPU进程与计划任务事实确认，无第二个同工作区Codex实例，DONE/NOT_DONE/UNKNOWN必须严格区分。
- 下一自然节点`NEXT_DISPOSITION=CEO_APPROVED_...`与对应真实GitHub CEO决策一致；建议而未获批时只进入CEO复核，不启动无意义的Codex。
- GitHub CEO批准→Windows本地决策文件→NEXT合同，是**三个分别验收的交接点**，任何一项不同步都不能声称“已恢复”。
- 迁移期`MOTHER_PAUSE.flag`不是永久停机规则。必须在真正安全门通过后归档，否则报告Blocked而非假称部署完成。
- 脚本语法检查、LF/CRLF兼容、路径/SHA指针、错误SHA拒绝、Exactly-once只读测试通过后，才能在无进程的自然节点更换live。
- 正常只读核验不产生新Freeze，不能等同执行失败；但绝不可为消除错误放松Freeze完成条件。
- 真实启动验收至少包含原生计划任务、唯一新Codex PID、原生会话或日志进展、新INFLIGHT及最终业务文件；完整自然节点结束和自动进入下一节点必须另行验证。

## 本轮已证实修复
2026-10-12，通过官方连接器核对本地CEO-D006 Git blob和GitHub一致，将下一任务改为CODEX007限定离线获批，归档旧迁移Pause后，使用原计划任务只触发一次：本机唯一Codex PID=16632，模型gpt-6.1-sol、ultra，新日志持续增长。V006仍为最近已验业务Freeze；不可提前宣称V007或完整Polsia FINAL_VALID。

## 版本隔离
技能包方法=`v3.2.0`；当前运行脚本=`v3.1.0`；Polsia固定引擎=`第28版`；母任务Freeze独立Vnnn。新方法发布不等于修改运行脚本或业务版本。旧版证据和备份一律保留。

**必须先完整读取正式方法正文再执行涉及迁移/恢复的现实操作。**
