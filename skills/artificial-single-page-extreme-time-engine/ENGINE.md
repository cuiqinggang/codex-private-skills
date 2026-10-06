# 《人工单页面极限短时间引擎 第8版》

版本：第8版  
升级来源：《人工单页面极限短时间引擎 第7版》  
状态：CURRENT  
唯一标准：`T*=min(T_VALID)`

## 1. 第8版为什么必须升级

第7版解决了“单点串行 Reality”问题；第8版进一步把已经冻结成熟的 HIPE v0.3.5 正式纳入主流程。

本版核心变化不是增加一个可选工具，而是把任务处理方式改为：

```text
先判断现实可解性
→ 先找成熟能力
→ 递归正向编译
→ 能 CODE 的全部 CODE
→ 有限语义 Choice 才 JEV
→ 只有不可压缩残差才 GPT
→ 独立节点最大合法并行
→ 整包虚拟成熟
→ Freeze
→ Reality
→ deterministic verifier
```

## 2. 总流程

```text
TASK_ACCEPTED
→ 冻结任务边界 / VALID / 时间边界
→ Reality Solvability Gate v0.2.0
→ 成熟方案集群 DISCOVER / COPY / ADAPT / COMPOSE / MATCH
→ Recursive Forward Compile（递归正向编译）
   ├─ CODE
   ├─ JEV
   └─ GPT residual
→ GPT residual 产生新状态/候选后重新进入 Recursive Forward Compile
→ 建立真实依赖图
→ 最大合法并行
→ 连续虚拟攻击直到收益收敛
→ FREEZE_BUNDLE
→ 一次正式 Reality
→ independent verifier
→ FINAL_VALID
→ T_VALID / T*
```

Reality 是冻结方案认证器，不是探索器。

## 3. HIPE Always-On 的正确含义

对所有非平凡任务，默认都可以经过 HIPE 的“结构化编译层”。

但是：

```text
HIPE_ALWAYS_ON = YES
JEV_ALWAYS_CALL = NO
```

原因：

- Reality Solvability Gate 与 Forward Compiler 本身是本地确定性逻辑，可低成本普遍使用；
- 能由 CODE 精确完成的判断，调用网络模型反而变慢；
- JEV 只在“需要语义智能、但答案空间有限并可验证”时才比 GPT 更有价值；
- GPT 保留给无法预先枚举的问题空间、隐藏信息和开放生成。

所以最大化 HIPE，不是最大化模型调用次数，而是最大化**被编译到最快合法执行形态的任务比例**。

## 4. Recursive Forward Compile

每个节点都重复以下规则，直到不能再压缩：

```text
NODE
→ deterministic exact? → CODE
→ else finite/enumerable semantic choice + verifier? → JEV
→ else → GPT residual
```

GPT residual 不直接长期占据后续流程。

GPT 一旦：
- 补齐规格；
- 发现成熟方案；
- 生成有限候选；
- 明确 action ontology；
- 明确 verifier；

立即把新节点重新送回编译器，尽可能继续下降到 CODE/JEV。

因此第8版不是：

```text
GPT → 一直 GPT → Reality
```

而是：

```text
GPT只解决不可压缩部分
→ 重新编译
→ 尽快退出GPT关键路径
```

## 5. CODE / JEV / GPT 优先级

固定优先级：

```text
CODE > JEV > GPT
```

### CODE
用于：
- 算术、阈值、时间比较；
- 文件/目录/哈希；
- schema；
- ffprobe；
- URL 解析；
- 原子提交；
- exactly-once；
- 已知 selector / 已知 API；
- 状态机迁移；
- 可机械验证的动作。

### JEV
用于满足全部必要条件的 bounded semantic decision：
- 状态明确或可提取；
- Choice 有限/可枚举；
- 动作集合已认证；
- 有 deterministic verifier；
- 不需要开放文本生成；
- 不依赖未解决隐藏信息；
- 不依赖 timed retry。

### GPT residual
用于：
- 需求/规格不完整；
- 新问题空间构造；
- 第一性原理重构；
- 开放方案生成；
- 隐藏信息发现；
- 无法枚举动作；
- 复杂异常链；
- JEV 低置信/域外回退。

## 6. 概率武器最大化规则

### 6.1 Batch before serial
同一状态下互相独立的多个 Choice / Score / Noul：
- 默认合并到同一个 Jev Decisions API 请求；
- 禁止无依赖时一问一请求串行。

### 6.2 Precompute conditional policy
如果后续动作只依赖有限前驱结果：
- 允许虚拟层预计算各分支 policy；
- receipt 到达后 CODE 只选择已冻结分支；
- 禁止重新调用大模型解释同一状态。

### 6.3 No repeated interpretation
同一事实状态已经结构化后：
- 不让 GPT/JEV 重复读取长正文；
- 状态快照、候选表、控件表使用确定性结构传递。

### 6.4 Confidence escalation
JEV 的概率用于路由不确定性，不直接替代 verifier。
低于本任务经 Reality 认证的阈值时：
```text
JEV → GPT residual / REVIEW
```
阈值不得凭空固定为通用常数。

## 7. Browser / Web 极限快路径

浏览器任务优先：

```text
CODE 获取页面/协议状态
→ CODE 构造真实可执行 action table
→ 只有出现多个语义候选时才 JEV Choice
→ CODE 执行动作
→ 增量更新状态
→ 必要时再次 JEV/CODE
→ deterministic verifier
```

禁止默认：

```text
截图/DOM全部交GPT
→ GPT重新解释整页
→ GPT生成selector
→ 点击
→ 再完整解释整页
```

若只有一个确定合法动作，直接 CODE，不调用 JEV。

若页面没有暴露必要动作：
- JEV 不猜；
- 回 GPT residual / 工具发现层。

## 8. 成熟方案集群优先级

默认：

```text
WORLD_SOLVED=YES
```

先找：
1. 成熟直接解；
2. 成熟组件闭合解；
3. 成熟探索/测量协议。

如果已经有成熟直接能力：
- 优先调用/复制/适配；
- 禁止重新研发等价系统。

如果一个现成程序/API/技能包能直接完成用户的 FINAL_VALID：
- 它比“自己重新写一个更漂亮的实现”优先级更高。

## 9. 连续虚拟成熟

单个任务页面内部允许循环：

```text
瓶颈
→ 解法集
→ 可解性
→ 编译
→ 依赖图
→ 并行
→ 组合
→ 关键路径重算
→ 下一瓶颈
```

直到：
- 高收益、低风险候选已组合；
- 继续攻击的预期关键路径收益低于复杂度/现实抖动；
- 或必须 Reality 才能消除关键不确定性。

不得每找到一个点就立即 Reality。

## 10. Reality 与轮数

对一个已虚拟成熟的 Freeze：

```text
DEFAULT_FORMAL_REALITY = 1
```

用于验证“新方法本身是否稳定”的系列任务：

```text
TARGET_REALITY_ROUNDS=3..4
HARD_MAX_REALITY_ROUNDS=5
```

- 若首轮已经稳定 FINAL_VALID，可提前停止；
- 不为了凑次数而运行；
- 第5轮仍不收敛：MANDATORY_POSTMORTEM=YES；
- 不允许重新出现十轮微版本链。

## 11. 性能剖面首轮预埋

第一次正式实现就预埋关键阶段计时：
- 输入；
- 搜索/路由；
- model barriers；
- 浏览器/网络；
- 下载/执行；
- verifier；
- 提交；
- 未分类胶水。

不得专门浪费一轮 Reality 只为加计时。

## 12. 时间边界

必须先冻结“当前任务是什么”。

若任务是“做出一个能完成目标的现实能力”：
```text
TASK_ACCEPTED → 首个成熟 FINAL_VALID
```
为建设任务 T_VALID。

若任务是“用户生产执行一次”：
```text
合法 READY_STATE → 本次 FINAL_VALID
```
为生产子任务 T_VALID。

不能用漂亮的生产子任务时间掩盖建设任务的巨大流程浪费。

## 13. 权威来源

正式方法/冻结包：
```text
网络共同工作区固定 commit + 明确路径
```
优先。

C盘：
- 执行缓存；
- 临时产物；
- 必要运行时；
- 网络共同工作区失败时 fallback。

禁止扫描整个 C 盘猜正式方法来源。

## 14. Integer Version Policy

从本版起，本方法族升级只使用整数版本：

```text
第8版 → 第9版 → 第10版
执行大脑 第3版 → 第4版
```

不再新建 8.1 / 8.2 / 3.1 等小数版本。

小修如果不改变方法语义：
- 只更新同版文档/冻结记录；
- 不为了文字修订制造版本号。

只有方法语义发生真实升级才升下一个整数。

## 15. 核心冻结

```text
最便宜的可靠智能优先
CODE能解决，不上模型
JEV能解决，不上GPT
GPT解决完，立即重新编译
独立节点，最大合法并行
成熟方案，优先复制组合
Reality，只验证成熟Freeze
```

第8版目标：让“智能”尽可能退出串行关键路径，只在确实需要它的位置出现。
