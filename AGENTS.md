# 用户指定的技能保存与读取规则

本仓库 `cuiqinggang/codex-private-skills` 是用户于2026-09-08指定的个人技能包、命令包审核规则及可复用命令资料的优先持久保存和读取来源。

对 `absolute-time-fireworks-optimization` 项目，本仓库是 GPT、Codex 与其他执行智能体的唯一长期共同事实源、共同办公区和版本库：

`SHARED_WORKSPACE_REPOSITORY=cuiqinggang/codex-private-skills`

同类任务默认只读 `skills/absolute-time-fireworks-optimization/SKILL.md` 与 `references/FAST-PATH.md`。先固定 `TASK_COMPLETED == TRUE`，再最小化真实 `T_END_TO_END`；执行结构必须由四列分析产生，不预设阶段、节点或独立 SYSTEM-99（系统 99）层。需要案例时读取 CASE INDEX（案例索引），出现异常时才读 FAILURE INDEX（失败经验索引），审计时才读完整历史。NEW_BEST（新的最好成绩）、NEW_FAILURE（新的失败经验）、NEW_FAST_PATH（新的成熟最短路径）、METHOD_CHANGE（方法变化）、ROOT_CAUSE_FOUND（找到根因）、99_REOPEN（99 重新开启）与 NEW_99_FREEZE（新的 99 冻结）必须在 RESULT_READY（结果就绪）后同步本仓库。

自动化模式中，ChatGPT 网页端是 REASONING BRAIN（推理大脑），Codex 是 EXECUTOR（执行器），本仓库是 SHARED FACT SOURCE（共同事实源），成熟 `playwright-native-ai-browser` 是 DEDICATED BROWSER BRIDGE（专用浏览器桥梁）。它们是执行基础设施，不是新的方法层级；每轮只传递一个明确高价值动作。

## 当前重点项目入口（2026-10-01）

对“极限短时间自动化闭环”项目，当前正式入口已经升级为：

- 项目：`workspaces/extreme-time-automation-loop-v1.2/README.md`
- 当前接续：`workspaces/extreme-time-automation-loop-v1.2/SUMMARY.md`
- Reality Contract：`workspaces/extreme-time-automation-loop-v1.2/REALITY_CONTRACT.md`
- 普适宪法：`skills/extreme-time-agent-constitution/SKILL.md`
- 宪法正文：`skills/extreme-time-agent-constitution/CONSTITUTION.md`
- 宪法冻结：`ETAC-v0.2-FREEZE-R1`

当前项目版本为 **极限短时间自动化闭环 v1.2**，项目仍处于 `STATE=10`，未 Virtual Mature、未 Project Freeze。  
**极限短时间智能体宪法 v0.2 已冻结，但宪法 Freeze 不等于项目 Freeze。**

原 `workspaces/jarvis-v1/` 与 `skills/jarvis-long-term-super-assistant-core/` 为历史来源，不再作为本项目当前定义。

## 执行规则

- 用户要求保存、更新或查找个人技能时，优先检查本仓库的现有内容和目录结构，复用既有技能，不重复建立同名包。
- 技能置于 `skills/<skill-name>/`，以 `SKILL.md` 为入口；保留其所引用的脚本、参考材料和必要资源。只保存与任务有关的文件。
- 命令包审核类技能也适用此规则；未迁入的技能不得宣称已经在仓库中。
- 编写Windows PowerShell命令包前读取 `skills/powershell-reliability-guard/SKILL.md`，并按需读取其中的5.1验收案例。该技能已包含用户要求的事前参考规则。
- 变更前读取当前版本和相关指令；不盲目覆盖远端新内容。保存后回读核对，并向用户提供明确的GitHub文件链接。
- 网络、权限或服务错误仍可能发生；不得因用户偏好本仓库而虚报保存成功。保留待保存成果，并明确报告真实状态。
- 不上传密钥、认证正文、浏览器登录数据或无关私人文件。本仓库保持私有，不擅自改变可见性。
- 仓库存储不等于所有智能体自动安装或加载；接手智能体应先读取本文件及对应SKILL.md。使用环境另有强制技能安装流程时仍须遵循，不能以本文件绕过。

## 已保存技能索引

| 技能 | 入口 | 用途 |
|---|---|---|
| extreme-time-agent-constitution | [SKILL.md](skills/extreme-time-agent-constitution/SKILL.md) | 极限短时间智能体宪法 v0.2；跨实现的普适推理规则 |
| powershell-reliability-guard | [SKILL.md](skills/powershell-reliability-guard/SKILL.md) | Windows命令包事前防错、PowerShell 5.1/7兼容、编码/路径/退出码检查 |
| absolute-time-fireworks-optimization | [SKILL.md](skills/absolute-time-fireworks-optimization/SKILL.md) | 第一性原理四列法通用99收敛引擎 v2.0.0；以任务完成为单一边界、以端到端时间为唯一主指标 |

2026-09-08新增的验收案例根据用户回传报告整理，未冒充编写端Windows实测或原始本机技能全文。其他既有技能以仓库实际目录为准。

## 共同工作区统一入口

跨智能体接手、技能包查找、工作区恢复时，统一先读取：

- `00_START_HERE/COMMON-ENTRY.md`
- `skills/shared-workspace-skill-index/SKILL.md`
- `skills/shared-workspace-skill-index/INDEX.md`

其中总索引只负责定位资产；具体项目仍以其自身 `SKILL.md`、CURRENT、FREEZE、RESULT 等远端文件为准。main 未找到时继续检查相关 `codex/*` 分支，不得仅凭历史聊天宣称仓库已保存。
