# 用户指定的技能保存与读取规则

本仓库 `cuiqinggang/codex-private-skills` 是用户指定的个人技能包、项目资料和跨智能体共同工作区。

## 当前重点项目入口（2026-10-01）

当前正式项目：

- **极限短时间自动化闭环 v2.0**
- 项目：`workspaces/extreme-time-automation-loop-v2.0/README.md`
- 当前接续：`workspaces/extreme-time-automation-loop-v2.0/SUMMARY.md`
- Reality Contract：`workspaces/extreme-time-automation-loop-v2.0/REALITY_CONTRACT.md`

当前普适宪法：

- `skills/extreme-time-agent-constitution/SKILL.md`
- `skills/extreme-time-agent-constitution/CONSTITUTION.md`
- VERSION=`v0.3`
- FREEZE_ID=`ETAC-v0.3-FREEZE-R1`

核心当前规则：

```ini
OBJECTIVE=T*=min(T_VALID)
MATURE_SOLUTION_EXISTS=TRUE
NO_NEW_IMPLEMENTATION_ESCAPE=TRUE
CHANGE_SCOPE=ROOT_CAUSE_SCOPE
```

含义：
- 不保留“新增实现 / 自研 Runtime”作为成熟方案搜索失败后的出口；
- 当前未找到成熟解时继续重定义、重映射、重检索；
- 只在现有成熟方案、成熟配置、成熟接口和成熟组件最小组合中竞争；
- 采用成熟方案后继续攻击对完整 T_VALID 有明确收益的瓶颈。

项目当前仍为 `STATE=10 / VIRTUAL_MATURE=NO / PROJECT_FREEZE=NO`。  
**宪法 v0.3 Freeze 不等于项目 v2.0 Freeze。**

历史入口：
- `workspaces/extreme-time-automation-loop-v1.2/`：SUPERSEDED
- `workspaces/jarvis-v1/`：SUPERSEDED
- `skills/jarvis-long-term-super-assistant-core/`：HISTORICAL

## 执行规则

- 用户要求保存、更新或查找个人技能时，优先检查本仓库现有内容，复用既有技能，不重复建立同名包。
- 技能置于 `skills/<skill-name>/`，以 `SKILL.md` 为入口。
- 变更前读取当前版本；保存后必须远端回读核对。
- main 未找到时继续检查相关 `codex/*` 分支，不得仅凭历史聊天宣称已保存。
- 不上传密钥、Token、Cookie、SSH 私钥或无关私人文件。
- 不擅自改变仓库可见性，不 force push。
- 仓库存储不等于所有智能体自动安装或加载；接手智能体应读取本文件及对应 SKILL / CURRENT / FREEZE / RESULT。

## 共同工作区统一入口

跨智能体接手、技能包查找、工作区恢复时，统一先读取：

- `00_START_HERE/COMMON-ENTRY.md`
- `skills/shared-workspace-skill-index/SKILL.md`
- `skills/shared-workspace-skill-index/INDEX.md`

具体项目以其自身文件为准。

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
