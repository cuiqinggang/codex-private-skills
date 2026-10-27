# 共同工作区资产索引

更新时间：2026-10-01  
仓库：`cuiqinggang/codex-private-skills`  
默认分支：`main`

## 当前最高优先级入口

- **极限短时间自动化闭环 v2.0（CURRENT）**：`workspaces/extreme-time-automation-loop-v2.0/README.md`
- **v2.0 当前接续**：`workspaces/extreme-time-automation-loop-v2.0/SUMMARY.md`
- **v2.0 Reality Contract（DRAFT）**：`workspaces/extreme-time-automation-loop-v2.0/REALITY_CONTRACT.md`
- **极限短时间智能体宪法 v0.3（FROZEN）**：`skills/extreme-time-agent-constitution/SKILL.md`
- **宪法规范正文**：`skills/extreme-time-agent-constitution/CONSTITUTION.md`
- **Freeze ID**：`ETAC-v0.3-FREEZE-R1`

## 当前核心原则

```ini
OBJECTIVE=T*=min(T_VALID)
MATURE_SOLUTION_EXISTS=TRUE
NO_NEW_IMPLEMENTATION_ESCAPE=TRUE
CHANGE_SCOPE=ROOT_CAUSE_SCOPE
```

## 历史入口

- `workspaces/extreme-time-automation-loop-v1.2/`：SUPERSEDED
- `workspaces/jarvis-v1/`：SUPERSEDED
- `skills/jarvis-long-term-super-assistant-core/`：HISTORICAL
- `skills/extreme-time-agent-constitution/` 的 v0.2 Freeze：已由 v0.3 替代，历史记录保留在 CHANGELOG。

## 目录职责

- `skills/`：正式或历史技能包；
- `workspaces/`：长期项目工作区、阶段成果与现实证据；
- `docs/`：命令包、源清单、项目文档；
- `AGENTS.md`：仓库级读取与保存规则。

## 查找规则

1. 当前“极限短时间自动化闭环”一律先读 v2.0；
2. 找多个版本时按 CURRENT / SUPERSEDED / HISTORICAL 区分；
3. main 没找到时继续搜索相关 `codex/*` 分支；
4. 只有聊天历史提到、远端未找到时标记为 `HISTORICAL_REFERENCE_ONLY`；
5. 任何“已保存/已发布”必须远端回读确认。


<!-- HIPE-V035-FULLY-SEALED-20261006-R1 START -->
## 混合智能概率引擎 v0.3.5 — 简洁生产成熟版（FULLY_SEALED）

- 正式网上入口：[HIPE v0.3.5](https://github.com/cuiqinggang/codex-private-skills/tree/main/skills/hybrid-intelligence-probability-engine-v0-3-5)
- 读取入口：`skills/hybrid-intelligence-probability-engine-v0-3-5/SKILL.md`。
- 位置与冻结规则：`skills/hybrid-intelligence-probability-engine-v0-3-5/README.md`。
- Freeze ID：`HIPE-v0.3.5-FULLY-SEALED-20261006-R1`。
- 冻结 ZIP 与完整清单：对应目录 `freeze/`；原正式包 14 文件按原字节保存。
- 本地正式源：`C:\Users\A\Documents\Codex\2026-09-29\5-hipe-v0-3-5-01\outputs\hipe-v0.3.5`。
- 本地封存目录：`C:\Users\A\Documents\Codex\2026-10-06\v0-3-5-x20\outputs\HIPE-v0.3.5-FROZEN-20261006`。
- 触发：HIPE、混合智能概率引擎、0.35、v0.3.5、简洁生产成熟版。
- 禁止以旧 v0.3.0 / v0.3.2 覆盖本冻结基线；后续改动须另建版本并标 NEEDS_VERSIONED_UPGRADE。
- 本次为资产保存，不扩大原 21/21 常用场景认证范围，不重跑远端模型认证。
<!-- HIPE-V035-FULLY-SEALED-20261006-R1 END -->

## ECC 默认版本锁定（2026-10-15）

- 用户指定当前默认正式版本：**ECC V3.1.1**；“ECC”“ECC最新版”“ECC 3.11”均指此版本。V2.1.0只作历史基线，禁止作为默认版本或读取失败时的替代品。
- 统一入口：`skills/artificial-single-page-extreme-time-engine/ECC_V3_1_1_NETWORK_AUTHORITY.md`。
- 正式源码：`cuiqinggang/ecc-v3.1.1`，tag `v3.1.1`，固定提交 `b9e651bc6c6751bff43db30b80d9cab983a7c412`。
- 发布：https://github.com/cuiqinggang/ecc-v3.1.1/releases/tag/v3.1.1
- 正文：https://github.com/cuiqinggang/ecc-v3.1.1/blob/b9e651bc6c6751bff43db30b80d9cab983a7c412/README.md
- README标题“V3.1”和发布包名“ecc-v3.1”属于该发布的原始命名，不能据此降级为V2.1.0。
- 已安装或云端目录若返回 `ecc-four-role-loop-orchestration V2.1.0`，必须标记历史副本并转读上述入口；不得把旧正文改个版本号冒充新版。新版不可读取时报告版本读取阻塞，不静默回退。
- 只在用户明确查询历史或旧任务锁定旧版本时读取V2.1.0；不删除旧冻结，不自动迁移正在运行的任务。后续升级须明确更新此默认指针。
- 本次核实发布、tag提交和README来源，不宣称本机部署、性能、长任务或恢复测试已通过。

## 经验大脑V1接入（2026-10-27）
当前任务涉及V4.2、复杂工程、旧解法、重复故障或接续时，先读共同工作区`MEMORY.md`→`skills/reuse-experience-brain/SKILL.md`→相关经验卡片，再按当前用户合同继续原专业技能。V4.2入口为`skills/ai-organization-v4-2/SKILL.md`，步骤2已绑定此依赖。不要只加载技能而漏掉匹配旧经验。
原执行大脑第25版、旧日报、原技能/Freeze原位继承，完整范围见`skills/reuse-experience-brain/references/INHERITANCE.md`。当前用户任务不因旧入口中的历史项目状态而自动转成另一项目。
有效经验写回共享包，原始证据保留原处；沿用现有21点复盘，写后远端回读。未读记忆不得称已应用；实际读取不等于已证明完整T_VALID提速。平台未加载本入口的页面不因此获得自动注入。
