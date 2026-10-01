# 极限短时间自动化闭环 v1.2

```ini
PROJECT=极限短时间自动化闭环
VERSION=v1.2
STATE=10
PHASE=Reality Contract + Mature End-to-End Solution Competition
VIRTUAL_MATURE=NO
PROJECT_FREEZE=NO
FINAL_VALID=NO
CONSTITUTION=extreme-time-agent-constitution v0.2
CONSTITUTION_FREEZE_ID=ETAC-v0.2-FREEZE-R1
```

## 1. 项目目标

不是制造新的超级助手、Codex、Manus 或重型多智能体平台。

目标只有一个：

> 用户提出现实目标后，把原本由用户承担的复制、转发、提醒、换页、恢复上下文、普通故障纠偏、跨工具接力等“人肉胶水”尽量自动消除，使任务从现实合法起点自动推进到 FINAL_VALID，并使完整 `T_VALID` 尽可能短。

唯一优化目标：

```text
T* = min(T_VALID)
```

## 2. v1.2 与 v1.1 的根本变化

v1.1 已经开始摆脱 JARVIS，但仍带有“建设自己的自动化闭环实现”的惯性。

v1.2 进一步收敛为：

> **先定义 Reality Contract，再让世界现有成熟端到端方案与当前自建候选公平竞争。**

因此 v1.2 不预设必须保留：
- GPT + Codex；
- n8n；
- GitHub；
- 自有状态机；
- 自有长期 Memory；
- 自有 Adapter；
- 自有 Verifier；
- 自有 Agent 编排。

只要一个成熟整解能以更少结构达到相同或更高 VALID，并降低完整 T_VALID，就直接采用。

## 3. v1.2 最小工作链

```text
REALITY CONTRACT
→ STANDARD PROBLEM MAPPING
→ MATURE END-TO-END SOLUTION SEARCH
→ WHOLE-SOLUTION COMPETITION
→ MINIMAL CONFIG / INTEGRATION
→ REALITY EXECUTION
→ FINAL VALIDATION
→ 只持久化继续运行真正需要的状态/证据
```

任何额外层都必须证明自己不可删除。

## 4. 单一时间模型

从本轮现实合法起点开始：

```ini
FLOW_START=STATE@REAL_TIMESTAMP
```

到 `FINAL_VALID` 为止，以下全部计入同一 `T_FLOW`：
- 搜索；
- 分析；
- 配置；
- 等待；
- 执行；
- 失败；
- 恢复；
- 换页面 / Session；
- 重试；
- 验收。

`T_VALID` 只在真正 VALID 后产生。

局部耗时可以用于诊断，但不是第二优化目标。

## 5. 当前有效判断

### 已确认
- 单一端到端时间轴；
- 成熟完整方案优先；
- 自有资产无优先权；
- 先整体归因，再决定修改范围；
- 连续结构性失败必须重新映射成熟方案；
- 完整长期记忆系统不是当前首要目标；
- 状态管理、任务身份和必要证据持久化是现实问题，但实现形式尚未固定。

### 仍未确认
- 最终是否需要自建 v1.2 Runtime；
- `10→20→30→40→100` 是否继续保留；
- GPT/Codex/n8n/GitHub 是否进入最终主链；
- 是否需要任何新的 Adapter / Agent / Memory；
- 哪个成熟完整产品或平台最接近 Reality Contract。

## 6. 当前状态

仍为：

```ini
STATE=10
VIRTUAL_MATURE=NO
PROJECT_FREEZE=NO
```

原因：Reality Contract 尚未完整冻结，成熟端到端方案尚未完成系统搜索和竞争。

**宪法 v0.2 已冻结，不代表项目 v1.2 已冻结。**

## 7. 下一步唯一主线

1. 写完整 Reality Contract；
2. 把每个“人肉胶水”需求映射为标准自动化问题；
3. 搜索多个成熟端到端方案；
4. 先比较完整方案，再考虑组件拼装；
5. 把当前自建方案当普通候选；
6. 统一用 VALID + 端到端 `T_VALID` 比较；
7. 决定直接采用成熟整解、极薄配置、最小成熟组合，还是确有必要继续自建。

详细接续见 `SUMMARY.md`。
