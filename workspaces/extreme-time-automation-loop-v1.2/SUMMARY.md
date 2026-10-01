# 极限短时间自动化闭环 v1.2｜当前接续摘要

## 当前正式状态

```ini
PAGE_NAME=极限短时间自动化闭环 v1.2
PROJECT_VERSION=v1.2
STATE=10
VIRTUAL_MATURE=NO
PROJECT_FREEZE=NO
CONSTITUTION_VERSION=v0.2
CONSTITUTION_FREEZE=YES
CONSTITUTION_FREEZE_ID=ETAC-v0.2-FREEZE-R1
```

## 当前唯一目标

```text
T* = min(T_VALID)
```

只有一条从现实合法起点到 FINAL_VALID 的端到端现实时间轴。

## v1.2 的核心变化

1. 项目不再以“建设自己的 JARVIS/自动化系统”为默认方向。
2. 先定义现实合同，再搜索世界已有完整成熟整解。
3. 完整成熟产品优先于自有 Skill、组件拼装和新开发。
4. `MATURE_SOLUTION_EXISTS=TRUE` 是当前任务域默认工作假设。
5. 故障先整体归因，`CHANGE_SCOPE=ROOT_CAUSE_SCOPE`。
6. 状态机、时间头、定位格式、GPT/Codex/n8n/GitHub 均只是实现候选。
7. 长期 Memory、Adapter Framework、新 Agent、额外 Verifier 均默认不建，除非 Reality Contract 证明必要。

## 当前最小架构

```text
Reality Contract
→ 标准问题映射
→ 成熟端到端方案搜索
→ 完整方案竞争
→ 最小配置/集成
→ Reality
→ FINAL_VALID
```

## 当前不应做

- 不继续完善旧 JARVIS 架构；
- 不默认 GPT+Codex+n8n+GitHub 必须保留；
- 不默认 `10→20→30→40→100` 不可替代；
- 不造 Adapter / Agent / Memory 系统；
- 不在未归因时直接修局部故障；
- 不因已有自有 Skill 而优先使用自有 Skill。

## 当前下一步

只做两件事：

1. 完成 `REALITY_CONTRACT.md`；
2. 基于合同建立“成熟端到端整解候选池”，与自建 v1.2 公平竞争。

若成熟整解更优，可以直接放弃自建 Runtime。
