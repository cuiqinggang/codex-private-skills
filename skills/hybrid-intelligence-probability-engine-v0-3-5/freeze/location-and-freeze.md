# 混合智能概率引擎 v0.3.5：定位与冻结记录

FREEZE_ID=HIPE-v0.3.5-FULLY-SEALED-20261006-R1
STATE=FULLY_SEALED
日期=2026-10-06T21:35:53.545199+08:00
标签=【页面名1｜任务名1｜序号1】

## 正式位置

正式源：`C:\Users\A\Documents\Codex\2026-09-29\5-hipe-v0-3-5-01\outputs\hipe-v0.3.5`
入口：`SKILL.md`；执行入口：`runtime/production.py`。
发布状态：`CURRENT_STATE.json` 中 VERSION=0.3.5，status=FROZEN_RELEASE，PRODUCTION_READY=YES，DONE=YES。
发布时间：2026-09-29 01:19:27（北京时间）。
封存目录：`C:\Users\A\Documents\Codex\2026-10-06\v0-3-5-x20\outputs\HIPE-v0.3.5-FROZEN-20261006`
长期知识条目：`C:\Users\A\.codex\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS\03_SKILL_ASSETS\HIPE-v0.3.5-Frozen-Location-20261006.md`

## 本次验证与成熟边界

原发布清单 13/13 SHA256 匹配；完整正式包 14 文件均纳入 SHA256-MANIFEST.json。
封存 ZIP 解包字节 14/14 匹配；封存后正式源哈希 14/14 匹配。
原有常用场景认证 21/21、CORE_FUNCTIONAL=PASS 是保留的历史发布证据。
本次未新增远端模型调用，未重新认证任意开放任务，也未作 30 轮性能认证。
本次冻结锁定版本和字节，不扩大原认证范围。

## 找不到的原因与已查范围

已确认共同私库：cuiqinggang/codex-private-skills。
2026-10-06 检查 main（0583c7b24744744d67d4eb4e3e46c7656f2dcb59）的 skills/ 与 workspaces/：没有 HIPE 正式入口。
全部 184 个远端分支中，相关 HIPE 分支最高命名版本为 v0.3.2；v0.3.0、v0.3.1 同样存在。
v0.3.2 分支 SKILL.md 已远端回读，版本确为 0.3.2。
代码搜索索引 is_code_search_indexed=false；搜索为空不能用来证明文件不存在。
提交关键词搜索“HIPE v0.3.5”无命中，不等于所有历史提交均无该文件。
本地知识脑 skills-index / reports-index 没有 HIPE 条目，正式技能安装根没有对应目录。
因此已确认的是：成熟 v0.3.5 正式产物仍在本地，已检查的共同库入口缺少该版本定位；
尚不能断言“从未上传”或“被删除”。不能把 v0.3.0 当最新本地版本。
本次没有发布或合并远端仓库；云端保存状态仍是 NOT_VERIFIED_FOR_V035。

## 永久冻结规则 / SOP

1. 搜索 HIPE、混合智能概率引擎、0.35、v0.3.5、简洁生产成熟版时，先读本条目与正式源 SKILL.md。
2. 使用前运行本封存目录的 `python -B verify_seal.py --source`；任何哈希变化都停止使用并报告。
3. 禁止原地编辑正式源或封存文件；禁止换模型、扩域、重造执行架构后仍称同一冻结版本。
4. 后续确需修改，返回 NEEDS_VERSIONED_UPGRADE，另建 v0.3.6 或用户指定的新版本，保留本基线。
5. 远端找到其他副本时先核对版本与完整清单，不用旧分支覆盖本源。
6. 不主动优化、不启动自动任务、不写 H/K；单次使用日志仍按原 SKILL 存各次 status.json。
7. 原源缺失返回 BLOCKED_C_SOURCE_MISSING；不得静默改用 ZIP 或历史盘。

此冻结是字节证据、交付快照和长期治理约束，不宣称具有管理员不可更改的文件系统锁。

## 失败复盘与下次复用

失败入口：先检查知识索引和版本位置，再查远端 main/相关分支；目录读取优先于不可用的代码搜索。
材料价值：避免版本降级、位置丢失与冻结资产原改，形成可执行 SOP 和完整性验证器。
最近使用记录：本记录及 SEAL-RECEIPT.json；日期 2026-10-06，动作 LOCATE_AND_SEAL，结果 PASS。
下次：定位知识条目 → 核验冻结 → 读原入口 → 在原认证范围内使用。

## AGENTS.md 规则补丁草案

HIPE v0.3.5 正式源以本记录路径为准。不得以共同库旧 v0.3.0 或 v0.3.2 替代。
每次使用前核对冻结清单。哈希变化停止并报告；修改必须 NEEDS_VERSIONED_UPGRADE。
本段只作为草案，未覆盖任何全局 AGENTS.md。

## 工具记录

CodeGraph usage:
- MCP available: 未查询（本轮为文件定位、哈希与封存，不分析或改动引擎代码）
- CLI available: 未查询（同上）
- .codegraph index present: 本工作区 NO；远端根列表无 .codegraph
- status checked before work: 工作区存在性已查
- callers/callees/impact checked where relevant: 不适用
- sync/refresh run after meaningful code changes: 不适用，未改动引擎代码
- if not used, reason: 仅治理与完整性验证

Knowledge Brain usage:
- INDEX checked: YES
- ROUTING_MAP checked: YES
- Relevant indexes checked: projects-index.md / reports-index.md / skills-index.md
- CodeGraph used where relevant: 不适用
- OpenHuman reference used where relevant: 不涉及记忆架构
- Sync run before/after: 前期只读；收尾仅显式路径 Hot Sync 与 Health Check，具体结果见长期写入回执
- If not used, reason: 已使用

【页面名1｜任务名1｜序号1】
