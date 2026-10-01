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
