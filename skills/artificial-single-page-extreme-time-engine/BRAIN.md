# 《极限短时间执行大脑 2.1》

版本：2.1  
升级来源：2.0  
唯一标准：`T*=min(T_VALID)`

## 1. 大脑职责

执行大脑负责决定“哪里应该思考、哪里应该并行、哪里应该 Reality、哪里必须停止”。

核心不是把任务拆得最碎，而是：

```text
在 VALID 不变的前提下
让从合法 READY_STATE 到 FINAL_VALID 的串行关键路径最短
```

## 2. 四种运行模式

### A. 虚拟成熟模式
用于 Greenfield、性能收敛、结构设计。

允许：
- 连续攻击多个瓶颈；
- 多候选并行分析；
- 一次形成多处兼容修改；
- 删除伪串行；
- 预先计算条件分支；
- 使用成熟方案集群。

### B. Reality 认证模式
只验证已冻结方案。Reality 执行器不得边跑边重新设计。

### C. 局部修复模式
仅用于现实证据已经锁定的局部 bug。采用 Local Minimal Repair。

### D. 因果 A/B 模式
只有在“必须隔离变量才能判断”时使用。不得默认所有优化都进入该模式。

## 3. 先成熟、后执行

固定优先级：

```text
DISCOVER
→ COPY
→ ADAPT
→ COMPOSE
→ MATCH
→ VIRTUAL_MATURE
→ FREEZE
→ REALITY
→ VERIFY
→ TIME_OPTIMIZE
```

已知成熟问题禁止重新发明。

对于下载器类任务，成熟通用模式包括但不限于：
- 按真实媒体轨道分类，不按 URL 猜；
- 分离音视频并行/配对；
- staging；
- verifier；
- 原子提交；
- transient retry；
- exactly-once；
- 失败可观测性。

这些应优先在首个成熟方案中整体出现，而不是等每次现实失败后再逐项补丁。

## 4. 最大合法并行

对每个任务先画依赖图：

```text
真正依赖 → 串行
没有依赖 → 并行
仅仅因为代码写成顺序 → 不构成依赖
```

必须主动寻找：
- 独立候选探针并行；
- 独立下载并行；
- 独立 verifier 并行；
- 独立资料检索/方案判断并行；
- 条件分支预计算。

## 5. HIPE v0.3.5 作为全流程元决策能力

当前正式冻结能力不是旧 `jev-probability-engine-p0 v0.3.0`，而是：

```text
NAME=混合智能概率引擎 v0.3.5 — 简洁生产成熟版
PATH=skills/hybrid-intelligence-probability-engine-v0-3-5/
FREEZE_COMMIT=c6fe2878fd237e7a8120b3af8e75f93e3cd6a4d9
FREEZE_ID=HIPE-v0.3.5-FULLY-SEALED-20261006-R1
STATE=FULLY_SEALED
```

其中两项正式组件：

```text
Reality Solvability Gate v0.2.0
Comfort-Zone Forward Compiler v0.2.0
```

### 5.1 正确定位

HIPE 可以作为**几乎所有非平凡任务的元决策入口**，但不是要求每一步都调用 JEV。

正确含义：

```text
每个关键判断点都可以先结构化
→ 能 CODE 就 CODE
→ 有限 Choice + 明确状态 + 可验证 才 JEV
→ 开放生成 / 隐藏信息 / 定时重试 / 域不匹配 → GPT residual
```

因此：

```text
全流程可挂载 HIPE
≠ 全流程网络调用 JEV
```

### 5.2 固定任务入口

```text
TASK_ACCEPTED
→ Reality Solvability Gate
   ├─ INCOMPLETE_SPEC
   ├─ SOLUTION_SEARCH_REQUIRED
   ├─ INFEASIBLE_OR_CONTRADICTORY
   ├─ CERTIFIED_COMPILABLE
   ├─ MATURE_DIRECT
   ├─ MATURE_COMPOSABLE
   ├─ MATURE_EXPLORATORY
   └─ FRONTIER_UNKNOWN
→ 成熟方案检索/组合
→ Forward Compiler
   ├─ CODE
   ├─ JEV
   └─ GPT
→ 最大合法并行
→ Reality Executor
→ deterministic verifier
→ FINAL_VALID
```

### 5.3 最有价值的挂载点

优先用于：
- 任务是否规格完整；
- 是否现实可解；
- 直接成熟解 / 组合成熟解 / 成熟探索协议分类；
- 多候选路线优先级；
- 有限浏览器动作选择；
- 工具/执行器路由；
- Failure Class 分类；
- continue / defer / stop 判断；
- 多个独立语义判断的批量/并行决策。

不用于替代：
- hash、ffprobe、文件存在性；
- 精确数值阈值；
- 原子提交；
- 已冻结 deterministic action；
- 无法枚举答案的开放式设计；
- 页面没有暴露可选动作时的“猜动作”。

### 5.4 Browser / Web 任务原则

浏览器任务先把页面真实控件压成有限 action table，再让快速决策器选择；自由文本仍交给语言模型，最终结果由确定性 verifier 收口。

如果页面/工具没有暴露需要的动作，JEV 应 fail-fast 或回 GPT，不得幻觉补全隐藏动作。

## 6. 预期收益排序

每次 Reality 前，对候选优化至少判断：

- 预计可移除多少关键路径时间；
- 成功概率；
- 是否影响 VALID；
- 是否与其它优化兼容；
- 是否只是把等待从 A 阶段转移到 B 阶段；
- 是否小于当前现实抖动。

优先执行“高收益、低风险、可组合”的一组，而不是机械地只取当前最大单阶段一个点。

## 7. 不追逐噪声

`T*=min(T_VALID)` 仍是唯一记录标准。

但“下一轮是否值得改版本”必须看结构性证据。若两个正式结果只相差极小、且其它阶段存在明显现实抖动，不得把单次随机差异当成结构性优势继续派生大量版本。

R7=15,221.268ms 与 R9=15,184.665ms 仅差 36.603ms（约0.24%），可记录 R9 为最短观测，但不足以证明其整个结构稳定优于 R7。

## 8. 合法 READY_STATE

极限时间只从生产同构、预先冻结的合法 READY_STATE 开始。

一次性安装、模型下载、开发环境搭建不应强行混入每次生产运行；反过来，生产时真实必须发生的浏览器启动、网络等待、下载、验证不得偷偷移出计时。

## 9. 权威来源与落地位置

方法/技能/冻结包的权威来源优先级固定为：

```text
网络共同工作区 main / 固定 commit + 明确路径
→ 权威源

本地 C:\... 
→ 仅执行工作区 / 临时落地 / Reality 证据
→ 不是方法权威源
```

正式交接必须给出：
- REPO
- COMMIT 或 main 的明确版本身份
- ENGINE_PATH
- TASK_PATH

禁止先扫描整个 C 盘猜方法文件。

若网络共同工作区不可用，才允许本地 fallback，并必须标记 `SOURCE_FALLBACK=YES`。

## 10. Greenfield R1-R10 方法判定

本次低效率的主因不是单个 Python 性能问题，而是执行策略错误：

1. 成熟方案集群没有在 R1 前充分完成；
2. 虚拟成熟只做了一步就下 Reality；
3. Local Minimal Repair 被扩大成全局优化规则；
4. 页面边界被误读成微变量边界；
5. 单变量实验被误读成默认优化模式；
6. performance instrumentation 太晚；
7. 结构性并行没有优先评估；
8. 现实抖动下仍继续追逐极小 delta；
9. 网络共同工作区路径未写死，导致本机搜索与权限噪声。

本版全部纠正。


## 11. 任务级时间优先于局部漂亮数字

执行大脑必须先问：**当前被优化的“任务”到底是什么？**

如果用户要的是“最快做出成熟版本”，则不能只看最终产品单次运行时间。开发期间的搜索、页面切换、重复 Reality、冻结、返工、人工转发，都属于该建设任务从 TASK_ACCEPTED 到成熟 FINAL_VALID 的真实关键路径。

局部阶段时间只有在它属于当前冻结任务边界时才可作为优化依据，不能用一个越来越漂亮的子流程数字掩盖整个项目越来越慢。
