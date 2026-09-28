# 用户指定的技能保存与读取规则

本仓库 `cuiqinggang/codex-private-skills` 是用户于2026-09-08指定的个人技能包、命令包审核规则及可复用命令资料的优先持久保存和读取来源。

对 `absolute-time-fireworks-optimization` 项目，本仓库是 GPT、Codex 与其他执行智能体的唯一长期共同事实源、共同办公区和版本库：

`SHARED_WORKSPACE_REPOSITORY=cuiqinggang/codex-private-skills`

同类任务默认只读 `skills/absolute-time-fireworks-optimization/SKILL.md` 与 `references/FAST-PATH.md`。先固定 `TASK_COMPLETED == TRUE`，再最小化真实 `T_END_TO_END`；执行结构必须由四列分析产生，不预设阶段、节点或独立 SYSTEM-99（系统 99）层。需要案例时读取 CASE INDEX（案例索引），出现异常时才读 FAILURE INDEX（失败经验索引），审计时才读完整历史。NEW_BEST（新的最好成绩）、NEW_FAILURE（新的失败经验）、NEW_FAST_PATH（新的成熟最短路径）、METHOD_CHANGE（方法变化）、ROOT_CAUSE_FOUND（找到根因）、99_REOPEN（99 重新开启）与 NEW_99_FREEZE（新的 99 冻结）必须在 RESULT_READY（结果就绪）后同步本仓库。

自动化模式中，ChatGPT 网页端是 REASONING BRAIN（推理大脑），Codex 是 EXECUTOR（执行器），本仓库是 SHARED FACT SOURCE（共同事实源），成熟 `playwright-native-ai-browser` 是 DEDICATED BROWSER BRIDGE（专用浏览器桥梁）。它们是执行基础设施，不是新的方法层级；每轮只传递一个明确高价值动作。

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
| absolute-time-fireworks-optimization | [SKILL.md](skills/absolute-time-fireworks-optimization/SKILL.md) | 第一性原理四列法通用99收敛引擎 v2.0.0；以任务完成为单一边界、以端到端时间为唯一主指标 |

2026-09-08新增的验收案例根据用户回传报告整理，未冒充编写端Windows实测或原始本机技能全文。其他既有技能以仓库实际目录为准。

## 2026-09-28补充：完整任务包先入共同工作区，再发简短指针（强制默认）

本条适用于GPT向Codex及其他执行智能体交付任务；是传输与交付要求，不增加状态机、控制服务或用户操作步骤。

1. GPT完成虚拟成熟与冻结后，必须默认将完整命令正文、实际输入、必要冻结代码与资料、文件清单、任务关联、验收及返回合同放入本共同私库。用户只提供页面名称与任务要求；其余可生成资料由GPT准备。不得默认只给ChatGPT沙箱下载链接、要求用户搬ZIP，或另发00号会话定位探测。
2. GPT必须实际写入，再按固定提交回读核对文件内容、字节摘要及资料齐备。只有全部必要资料可读且核对通过，才能标记交付就绪并发布简短自然语言指针：同一行`【页面名｜任务名｜序号｜实】`，附仓库、固定提交、入口路径及必要摘要。指针不代替仓库中的完整正文。
3. 只有登录、权限、服务、网络或实际读写能力受限等有原始证据的阻断，才可使用简洁备用传输；如实区分仓库故障与调用工具限制，不能因省事绕开正常共同工作区，不能虚报整包上传成功。完整性与授权门不因换通道降低。
4. 补交同一冻结包只修复交付，不改业务正文、冻结摘要、包号和原时间线，不算第02包；仓库上传成功不等于执行者已收到。采用v5.5时，未核验真实收件仍为30，GPT核验后才进入40；核验确认不是新业务包。未知收件不盲目重发，真实结果审核通过前不宣布100。
5. 本条不自动升级技能内核、不更新正式current、不授权改代理、FlClash、系统设置或旧证据；不把目录不完整、缺少ZIP、无法核验或文字摘要声明写成通过。是否交付完整以任务冻结合同和实际证据为准。
