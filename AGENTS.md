# 用户指定的技能保存与读取规则

本仓库 `cuiqinggang/codex-private-skills` 是用户于2026-09-08指定的个人技能包、命令包审核规则及可复用命令资料的优先持久保存和读取来源。

对 `absolute-time-fireworks-optimization` 项目，本仓库是 GPT、Codex 与其他执行智能体的唯一长期共同事实源、共同办公区和版本库：

`SHARED_WORKSPACE_REPOSITORY=cuiqinggang/codex-private-skills`

同类任务先读 `skills/absolute-time-fireworks-optimization/SKILL.md`、`references/CURRENT-STATE.md` 与 `references/FAST-PATH.md`；异常时才读 FAILURE INDEX（失败经验索引），审计时才读完整历史。NEW_BEST（新的最好成绩）、NEW_FAILURE（新的失败经验）、NEW_FAST_PATH（新的成熟最短路径）、METHOD_CHANGE（方法变化）、ROOT_CAUSE_FOUND（找到根因）、99_REOPEN（99 重新开启）与 NEW_99_FREEZE（新的 99 冻结）必须在 RESULT_READY（结果就绪）后同步本仓库。

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
| powershell-reliability-guard | [SKILL.md](skills/powershell-reliability-guard/SKILL.md) | Windows命令包事前防错、PowerShell 5.1/7兼容、编码/路径/退出码检查 |
| absolute-time-fireworks-optimization | [SKILL.md](skills/absolute-time-fireworks-optimization/SKILL.md) | 第一性原理四列法极限时间宏观迭代；烟花项目验证成功路径 |

2026-09-08新增的验收案例根据用户回传报告整理，未冒充编写端Windows实测或原始本机技能全文。其他既有技能以仓库实际目录为准。
