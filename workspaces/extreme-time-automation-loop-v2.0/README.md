# 极限短时间自动化闭环 v2.0

```ini
PROJECT=极限短时间自动化闭环
VERSION=v2.0
STATE=10
PHASE=Reality Contract + Mature End-to-End Solution Competition
VIRTUAL_MATURE=NO
PROJECT_FREEZE=NO
FINAL_VALID=NO
CONSTITUTION_VERSION=v0.3
CONSTITUTION_FREEZE_ID=ETAC-v0.3-FREEZE-R1
MATURE_SOLUTION_EXISTS=TRUE
NO_NEW_IMPLEMENTATION_ESCAPE=TRUE
OBJECTIVE=T*=min(T_VALID)
```

## 1. 项目目标

把用户过去亲自承担的复制、转发、提醒、换页、恢复上下文、普通故障纠偏、跨工具接力等“人肉胶水”尽量自动消除。

任务从现实合法起点自动推进到 `FINAL_VALID`，唯一目标：

```text
T* = min(T_VALID)
```

## 2. v2.0 的根本变化

v2.0 不再问：

> 如果成熟方案都不够，是否自己新增实现？

这个出口已经删除。

当前任务域固定前提：

```ini
MATURE_SOLUTION_EXISTS=TRUE
NO_NEW_IMPLEMENTATION_ESCAPE=TRUE
```

如果当前方案不够，不转入自研，而是继续：

```text
重新定义 Reality
→ 重新映射标准问题
→ 重新搜索成熟整解
→ 重新组合成熟能力
→ Reality 验证
```

## 3. 候选空间

只比较已经存在、可验证、可复用的成熟能力：

```text
完整成熟方案
→ 成熟方案 + 配置
→ 成熟方案 + 成熟接口
→ 成熟组件最小组合
```

不存在“新增实现”这一第五层。

历史自有 Skill、GPT、Codex、n8n、GitHub、状态机等仍可参与，但只作为已有成熟资产，不享有优先权。

## 4. 成熟方案采用后继续攻击

采用成熟方案不是结束。

只要 Reality 仍存在明显时间损失，就继续寻找有现实收益的点：

```text
瓶颈
→ 对完整 T_VALID 的贡献
→ 成熟替代/配置/接口/并行/缓存/恢复
→ 最小改变
→ 重测完整 T_VALID
→ 有收益则保留
```

没有完整端到端收益的局部优化不保留。

## 5. 故障处理

```ini
CHANGE_SCOPE=ROOT_CAUSE_SCOPE
```

连续结构性失败意味着成熟方案映射或组合错误，不继续补丁化，而是重新进入成熟解搜索与竞争。

## 6. 最小工作链

```text
REALITY CONTRACT
→ STANDARD PROBLEM MAPPING
→ MATURE END-TO-END SOLUTION SEARCH
→ WHOLE-SOLUTION COMPETITION
→ MINIMAL CONFIG / MATURE INTEGRATION
→ REALITY EXECUTION
→ FINAL VALIDATION
→ 继续攻击仍有收益的 T_VALID 瓶颈
```

## 7. 当前状态

```ini
STATE=10
VIRTUAL_MATURE=NO
PROJECT_FREEZE=NO
FINAL_VALID=NO
```

原因：Reality Contract 尚未完成，成熟端到端方案尚未完成系统竞争。

宪法 v0.3 已冻结，不等于项目 v2.0 已冻结。

## 8. 下一步

1. 完成 `REALITY_CONTRACT.md`；
2. 把所有“人肉胶水”映射成标准自动化问题；
3. 搜索多个成熟端到端整解；
4. 只在成熟解空间内竞争；
5. 选择最短有效路径进入 Reality；
6. Reality 后继续攻击完整 T_VALID 中仍有明确收益的瓶颈。
