# 长期记忆超级虚拟人 v0.7.0｜完整保存基线（未冻结）

```ini
VERSION=0.7.0
STATE=SAVED_NOT_FROZEN
FINAL_VERSION=NO
PROJECT_FINAL_VALID=NO
PARENT_FROZEN_VERSION=0.6.0
PARENT_FROZEN_BASELINE=V060-FIRST-PRINCIPLES-FAULT-METHOD-R1
DATE=2026-10-04
NEXT_ACTION=OPEN_TRUE_NEW_CHAT_AND_RUN_V070_REALITY_BACKLOG
```

## 1. 本文件用途

这是 2026-10-04 从 v0.4.5 持续演进到 v0.7.0 后的**完整保存点**。

它不是最终冻结版本，不代表所有新增能力已经完成 Reality。它的作用是让后续真正 New chat 可以直接从 v0.7.0 已保存状态开始，不再依赖当前长页面。

后续规则：
- 新页面以本文件 + `FROZEN_NODE_MINIMAL_CONTEXT_EXECUTION.md` + 必要证据为起点；
- 不重放当前长聊天；
- 先补未完成 Reality；
- 根据 Reality 修改 v0.7；
- 只有测试和收敛完成后，才允许把 v0.7 改为 FROZEN。

## 2. v0.7.0 当前核心方法

唯一优化目标：

```text
T* = min(T_VALID)
```

v0.7 新增“冻结节点·动态短上下文执行”：

1. 长任务不等于长上下文；
2. 基本执行单元是“最小完整可独立验收节点”，不是最小动作；
3. Node Freeze 与 Version Freeze 分离；
4. 节点完成后先保存有效状态，再决定继续当前页或真正 New chat；
5. 换页不是固定动作，而是动态比较完整 T_VALID；
6. 固定字数/轮数阈值只保留为 fallback guard；
7. 新页继承有效结论，不继承完整历史噪声；
8. 完成且失去价值的旧页面原则上关闭，避免 CPU/RAM/browser renderer 等资源占用；
9. 短节点天然提高可并行度，但只在依赖独立、无写冲突、无资源冲突、可合并且实际更快时并行；
10. 多智能体不是硬架构；
11. ECC V3.1 是按需专业长流程工具，不是 v0.7 强制运行层；
12. Codex、Runner、Reasonix、GPT直接工具都是候选执行面，按 VALID 前提下完整 T_VALID 选择；
13. 四角色独立审计不是 v0.7 全局硬要求，按风险与验证需要启用；
14. v0.6 第一性原理故障分析继续作为故障唯一分析方法。

权威方法文档：
`FROZEN_NODE_MINIMAL_CONTEXT_EXECUTION.md`

## 3. v0.6 继承的冻结原则

v0.6.0 已冻结，v0.7 不静默改写：

```text
FIRST_PRINCIPLES_FAULT_ANALYSIS_AND_MINIMAL_REPAIR
第一性原理 → 因果链 → 第一个不成立点 → 最小修复 → Reality
```

重建不是方法，只能是局部断点实例失效时的一种动作。

## 4. 已完成 / 已有 Reality 支撑

### A. v0.4.5 Clean CEO Lifecycle
状态：REALITY PASS

- 单空白 ChatGPT New chat 基线；
- CEO-1 → 最小 checkpoint → true New chat CEO-2；
- 禁止 Branch；
- A/B 子任务原结果接管、不重做；
- 完成页关闭；
- 最终恢复 1 个空白页；
- R18 T_VALID=51,454 ms；
- R19 T_VALID=54,246 ms；
- 当前该合同历史观测 T*=51,454 ms。

### B. 会话连续性 / 卡死恢复
状态：已有多项 Reality PASS

- true New chat + minimal handoff；
- exactly-once；
- global writer lease；
- 安全卡死故障注入；
- stop old turn → checkpoint → new chat → ACK；
- branch=false；
- second browser=false。

### C. v0.5 Goal Loop
状态：受控 Windows / 文件 / runtime 场景 PASS

- Goal Loop 确定性测试 12/12；
- 连续性 25/25；
- writer lease 6/6；
- 独立进程/文件场景 4/4；
- 实际 runtime inbox 5/5；
- 覆盖自动返修、异常后 reconcile、去重、无进展停止、STOP；
- Windows 备路 GitHub Runner 实际命令复验 PASS。

### D. v0.6 第一性原理故障方法
状态：方法冻结；部分现实案例有直接证据

9223 Reality：
- 旧启动壳存在但 Chrome 主进程缺失；
- executable / shared-mcp profile 保留；
- 只恢复 Chrome 主进程断点；
- 9223 LISTEN PASS；
- /json/version PASS；
- ChatGPT target PASS；
- Attach-Only runtime PASS；
- true New chat → GPT ACK PASS；
- submissionCount=1；
- branchUsed=false；
- newBrowserLaunched=false。

其他支持案例：
- Windows/GPT 本地连接桥历史恢复经验；
- Hermes 升级后登录问题由权威正确凭据恢复（用户现场确认）。

## 5. 未完成 / 尚未 Reality 闭环

以下项目不得在新页面被误认为已完成：

### P0：v0.7 核心性能 Reality
1. 同构任务：继续当前页 vs Node Freeze + true New chat 的完整 T_VALID 对比；
2. 找出节点多大时换页开始真正更快；
3. 测试“多个简单相近节点留在同页”与“过早切页”的重理解成本；
4. 验证语义边界触发是否优于固定字数/轮数触发。

### P0：并行 / 多智能体 Reality
5. 同一独立任务集：串行 vs 2 路并行 vs 4 路或设备可承受并行度；
6. 测 CPU / RAM / 浏览器页面数量 / API吞吐对完整 T_VALID 的影响；
7. 找最大有效并行度，不追求最大 Agent 数；
8. 验证并行节点各自 Reality 后的合并 Gate；
9. 验证共享写状态下的冲突阻断。

### P0：页面资源生命周期
10. 实测旧页面数量增加对新页面响应与整体机器负载的影响；
11. 验证“节点冻结→关闭无价值页面→新页”完整链；
12. 自动判断页面是否仍有 pending/observation/recovery value；
13. 最终空闲态是否稳定恢复 1 个空白 New chat 页。

### P1：v0.5/v0.6 自动故障闭环
14. v0.5 Goal Loop 的真实 GPT/网页故障自动发现→自动恢复→继续业务→验收；
15. v0.6 第一性原理方法的自动触发：不明确故障是否能自动进入因果链分析，而不是末端试错；
16. 专用浏览器“Chrome主进程死亡/CDP失效”故障注入后，是否能自动定位并只修断点；
17. 修复时不能破坏“唯一专用浏览器/禁止重复 launch”保护。

### P1：动态调度实现
18. 当前 v0.7 是方法合同，尚无完整自动 Frozen Node scheduler；
19. 尚未自动估计 continue / rotate / serial / parallel 哪个 T_VALID 更低；
20. 尚未把节点冻结、页面轮换、并行调度、页面回收完整接入唯一 runtime；
21. 尚未对动态调度器做故障注入、去重、恢复和 exactly-once Reality。

### P2：ECC / 执行器组合优化
22. ECC V3.1 + Frozen Node 的真实长流程对比尚未完成；
23. 需要验证何种任务启用 ECC 才比直接节点流程更快；
24. Codex / Runner / GPT / Reasonix 的执行器路由尚未形成 v0.7 的统一 Reality 性能表；
25. 四角色审计仅保留为按需策略，尚未测其在不同风险/复杂度上的净 T_VALID 收益。

## 6. v0.7 新页面执行顺序建议

新页面不要一次把 25 项全做成一个大任务。

按 v0.7 自己的方法执行：

```text
Node 1：换页 T_VALID Benchmark
→ Freeze

Node 2：并行度 Benchmark
→ Freeze

Node 3：页面资源/关闭 Benchmark
→ Freeze

Node 4：自动故障恢复 Reality
→ Freeze

Node 5：动态 scheduler 接线
→ Freeze

Node 6：ECC / 执行器路由对比
→ Freeze

汇总
→ 决定 v0.7 最终合同
→ 完整回归
→ 再冻结 v0.7
```

能并行的 Node 可以从同一父冻结状态并行执行，但不得制造共享写冲突。

## 7. 新聊天最小接管包

新聊天只需要：

```text
项目：长期记忆超级虚拟人
当前版本：v0.7.0
状态：SAVED_NOT_FROZEN / NOT_FINAL
父冻结版本：v0.6.0
权威文档：V070_SAVED_BASELINE.md
方法文档：FROZEN_NODE_MINIMAL_CONTEXT_EXECUTION.md
目标：按 TEST_BACKLOG 从最优先 Reality 开始，逐节点测试、冻结结果，最终收敛并冻结 v0.7
禁止：把 v0.7 当前方法假定为全部 Reality PASS；禁止重放旧聊天；禁止一次打包所有未测项成长任务
```

## 8. 保存结论

v0.7.0 当前是“完整保存的工作版本”，不是最终版本。

```ini
V070_SAVED=YES
V070_FROZEN=NO
V070_FINAL=NO
V070_REALITY_COMPLETE=NO
SAFE_TO_START_NEW_CHAT=YES
OLD_LONG_CHAT_REQUIRED_FOR_CONTINUATION=NO
```
