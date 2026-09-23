# JEV 舒适区导向正向拆解器 v0.1.0

## 作用

把原始任务按照已经冻结的 JEV 商业舒适区规则直接向前编译，而不是先随意拆解、再反向重构。

## 两层结构

### 第一层：高智能语义编译

从原始任务中形成标准节点，并为每个节点给出可审计事实：

- 是否可由确定性算法唯一完成；
- 是否有确定性执行器；
- 状态/证据/约束能否完全显式化；
- 输出是否能无损收敛为有限 Choice；
- Choice 是否可映射到已认证动作本体；
- 是否存在确定性 verifier；
- 是否仍需要开放文本生成；
- 是否仍依赖未提供的隐藏信息；
- 是否需要 timed retry；
- 转换是否保持原任务语义。

语义编译器只负责提出标准化事实，不直接决定最终路由。

### 第二层：确定性路由门

确定性代码根据上述事实唯一决定：

1. CODE 优先：
   - semantic_preserved=true
   - deterministic_exact=true
   - deterministic_executor_available=true

2. 否则进入 JEV，必须同时：
   - semantic_preserved=true
   - explicit_or_extractable_state=true
   - finite_or_enumerable_choice=true
   - certified_action_ontology=true
   - deterministic_verifier=true
   - requires_open_generation=false
   - unresolved_hidden_information=false
   - timed_retry_required=false

3. 其他全部进入 GPT residual。

## JEV 舒适区

当前生产舒适区仍保守限制为已经有现实证据同构的 Choice 形状：

显式状态
+ 有限动作
+ 固定动作本体
+ 确定性 verifier
+ 无 timed retry
+ 无开放生成
+ 无未解决隐藏信息

Noul、Score、开放动作空间、自由生成等不因为接口存在就自动晋级。

## 正向转换顺序

只允许一次有界正向编译：

1. 提取确定性子任务 → CODE；
2. 将上下文中的已知事实显式化为 state/evidence/constraints；
3. 若结果本质是有限决策，枚举有限 Choice；
4. 映射到已认证动作本体；
5. 建立/绑定 deterministic verifier；
6. 通过硬门 → JEV；
7. 任一硬门不能证明 → GPT residual；
8. STOP。

禁止 JEV ↔ GPT 循环重拆。

## STOP 规则

运行时不为了提高 JEV 占比无限拆分。

以下任一成立立即停止继续拆：
- 语义无损无法证明；
- 状态不能完全显式化；
- 动作空间不能有限化；
- verifier 不能确定性建立；
- 仍需要开放生成；
- 仍依赖隐藏信息；
- 需要 timed retry；
- 新增拆分会增加新的串行屏障，而没有已认证时间模型证明净收益为正。

## 成熟门

本组件只有形式规则通过，不等于通用语义拆解已经现实认证。

必须分别报告：
- FORMAL_RULE_SPACE
- SEMANTIC_BENCHMARK
- REAL_COMPILER_T_VALID

禁止混写。
