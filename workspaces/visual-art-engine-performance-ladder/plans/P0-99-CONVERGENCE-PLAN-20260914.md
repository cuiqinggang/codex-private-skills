# P0 99分迭代收敛总计划

英文标识：`P0 99 Convergence Plan`

项目：`visual-art-engine-performance-ladder`（通用高性能视觉作品生成引擎）

阶段：`P0 ComfyUI Control`（P0 ComfyUI 控制层）

固定任务合同：`P0-CONTROL-V1`

固定节点链：`LoadImage -> SaveImage`（读取图片 → 保存图片）

方法：`mature-replication-four-column` V4.0（第一性原理四列法 V4.0）

当前工作版本：`1.0.1_LOCAL_PATCH`（本地快速迭代补丁）

---

# 一、固定共同办公区与交接规则

GitHub 私有仓库：

`https://github.com/cuiqinggang/codex-private-skills`

共同办公区：

`https://github.com/cuiqinggang/codex-private-skills/tree/main/workspaces/visual-art-engine-performance-ladder`

P0 每一轮真实实验结果统一写入：

`workspaces/visual-art-engine-performance-ladder/stages/P0/<RUN_ID>/`

P0 的 ChatGPT 审核与99分推进计划统一写入：

`workspaces/visual-art-engine-performance-ladder/reviews/`

`workspaces/visual-art-engine-performance-ladder/plans/`

固定要求：

1. Codex 每完成一轮需要 ChatGPT 审核的真实测试，必须把报告、关键 JSON、关键原始事件、测试脚本差异和状态摘要同步到上述 GitHub 共同办公区。
2. 仅报告本机 `C:\...` 路径不算完整交接。
3. 用户之后只需告诉 ChatGPT“最新 P0 结果已上传”或给出 commit SHA，ChatGPT 直接从共同办公区读取。
4. 快速迭代期间，每个小实验不要求都发布正式 skill 版本；但是需要 ChatGPT 审核的真实运行证据必须同步到共同办公区。
5. 到达阶段 `99 -> FREEZE`（阶段99分并冻结）时，再统一做正式技能版本、本地正式安装和 GitHub 稳定版本同步。

---

# 二、P0 当前四项纵向基线

## ① 当前实测时间（CURRENT）

当前正式中位总时间：`32.55975 ms`

最快一次：`27.2659 ms`

P95 尾部时间：`58.1779 ms`

当前分段中位时间：

- 请求提交（`REQUEST`）：`5.55075 ms`，约17.05%；
- 队列等待/调度（`QUEUE`）：`4.71925 ms`，约14.49%；
- 节点执行（`EXECUTE`）：`3.4891 ms`，约10.72%；
- 结果确认（`RESULT`）：`16.99775 ms`，约52.20%；
- 保存（`SAVE`）：当前没有独立隔离，包含在执行阶段内。

正式记录：

`T_CURRENT = 32.55975 ms`

## ② 外部成熟前沿（EXTERNAL FRONTIER）

当前成熟路径已经明确：

- 本机原生 ComfyUI API；
- `/prompt`（提交任务）；
- WebSocket `/ws`（实时执行事件）；
- `/history/{prompt_id}`（任务历史和结果）；
- `/queue`（队列状态）。

完全同合同公开端到端数字：尚未发现。

邻近现实数量级：简单 ComfyUI 工作流已经处于几十毫秒级，只作现实参照，不直接作为本合同正式成绩。

## ③ 第一性原理物理时间（FIRST-PRINCIPLES PHYSICAL TIME / T_PHY）

严格已知事实：

`T_PHY <= 27.2659 ms`

第一版工作区间：

`T_PHY_WORKING_RANGE_V0.1 = 10–20 ms`

当前相对物理时间工作区间的待解释/待压缩差距约：

`12.56–22.56 ms`

当前最大未知：`RESULT`（结果确认）16.99775 ms 内部到底有多少是真正不可避免时间，多少是客户端检测/轮询/事件边界造成的时间。

## ④ 迭代收敛（ITERATIVE CONVERGENCE）

状态：已解除锁定。

固定原则：

- 固定任务合同不能缩水；
- 一轮只修改一个主要变量；
- 每轮固定 3 次预热 + 20 次正式测量；
- 失败样本不能删除或补跑替换；
- 每轮都必须与上一正式保留基线做对比；
- 达不到保留门槛立即回滚；
- Codex 不自行宣布99分，由 ChatGPT做四列法审核后决定。

当前：

`P0_99 = NO`

---

# 三、每一轮从“开始”到“交接”的固定生命周期

以后 P0 所有迭代都必须完整走以下 14 步。

## 第1步：读取基线（Baseline Read，读取上一轮正式基线）

必须读取：

- `P0-CONTROL-V1` 固定任务合同；
- 上一轮正式保留的 `T_CURRENT`；
- Median（中位数）、P95（95%尾部时间）、MIN（最快）、MAX（最慢）；
- REQUEST / QUEUE / EXECUTE / RESULT 分段；
- 当前 `T_PHY` 工作区间；
- 已经失败并回滚的方案；
- 当前环境和脚本哈希。

禁止直接从记忆或旧终端输出开始实验。

## 第2步：提出单一假设（Hypothesis，单一原因假设）

一轮只允许提出一个主要假设。

例：

“RESULT 约17ms中可能包含客户端固定轮询间隔，导致结果已经可用但 runner 晚发现。”

必须写清楚：

- 怀疑哪一段；
- 证据是什么；
- 为什么可能影响总时间；
- 如果假设成立，预计最多能减少多少时间。

## 第3步：估计收益上限（Gain Ceiling，理论最大收益）

在做实验前先算：

`理论最大收益 <= 当前该分段总时间`

例如 RESULT 只有约17ms，则这一条路径即使完全消失也不可能带来大于17ms的收益。

目的是避免在只有0.1ms潜力的地方花大量时间。

## 第4步：设计单变量实验（Single-Variable Design）

固定：

- 同一个输入图；
- 同样 256×256；
- 同样 `LoadImage -> SaveImage`；
- 同样输出有效性要求；
- 同样 API_READY；
- 同样串行执行。

只改变一个变量。

## 第5步：运行前预检（Readiness Check）

必须确认：

- ComfyUI API_READY；
- 队列为空；
- 没有其他任务；
- 固定合同未改变；
- 系统栈没有变化；
- 测试脚本只包含计划中的单一变量变化。

## 第6步：3次预热（Warmup 3）

3/3 必须有效。

预热只用于稳定运行状态，不进入正式成绩。

## 第7步：20次正式测量（Measured 20）

要求：

- 串行；
- 20 次固定；
- 失败不补跑；
- 不删除慢样本；
- 每个 Prompt ID 唯一；
- 每次输出可追踪到本轮。

## 第8步：结果有效性门禁（Result Validity Gate）

必须确认：

- 20/20 有效；
- history/结果完成；
- 输出文件属于对应 prompt；
- PNG 有效；
- 256×256；
- 可完整解码；
- SHA-256 已记录；
- 固定合同没有缩水。

不满足则该轮：

`TIME = INVALID_RESULT`（时间成绩无效）。

## 第9步：A/B 对比（A/B Compare，新旧基线对比）

至少比较：

- Median（中位总时间）；
- P95（尾部时间）；
- MIN；
- MAX；
- REQUEST；
- QUEUE；
- EXECUTE；
- RESULT；
- 失败率；
- 合同一致性。

## 第10步：保留或回滚（Keep / Rollback）

初始保留门槛：

- Median 稳定改善 ≥5%，且 P95 不明显恶化；或
- P95 稳定改善 ≥20%，且 Median 退化 ≤2%。

否则默认回滚。

非常小、不可稳定复现的收益不进入成熟基线。

## 第11步：同步更新四项（Four-Item Update）

每轮不能只更新 CURRENT。

必须同时审核：

1. 当前实测时间（CURRENT）是否刷新；
2. 外部成熟前沿（EXTERNAL FRONTIER）是否增加新证据；
3. 第一性原理物理时间（T_PHY）是否可以收窄；
4. 迭代收敛（ITERATIVE CONVERGENCE）下一优先级是否变化。

## 第12步：记录经验（Lesson Record）

每轮必须留下：

`假设 -> 修改 -> 测量 -> 结果 -> 保留/回滚 -> 原因`

失败方案同样必须记录，避免以后重复走弯路。

## 第13步：同步共同办公区（Shared Handoff）

写入：

`https://github.com/cuiqinggang/codex-private-skills/tree/main/workspaces/visual-art-engine-performance-ladder`

具体运行目录：

`workspaces/visual-art-engine-performance-ladder/stages/P0/<RUN_ID>/`

至少上传：

- `REPORT.md`（本轮中文主报告）；
- `timing-summary.json`（计时汇总）；
- `measured-runs.json`（20次正式数据）；
- `warmup-runs.json`（3次预热）；
- `raw-events`（必要的原始事件）；
- `benchmark-contract-snapshot.md`（固定任务快照）；
- 本轮实际测试脚本或差异；
- `environment-before/after`（必要环境摘要）；
- 输出有效性和 SHA-256 摘要。

同时更新 `LATEST.md`（最新运行入口）。

## 第14步：ChatGPT 审核与下一轮授权（ChatGPT Audit）

Codex 只回报：

- commit SHA；
- RUN_ID；
- GitHub 相对路径；
- 核心数字。

ChatGPT 从共同办公区直接读取完整证据，完成四列法审核，再决定：

- 保留；
- 回滚；
- 下一单变量；
- 是否收窄 T_PHY；
- 是否达到99；
- 是否冻结。

---

# 四、P0 候选优化路径——按理论收益和风险排序

## R1 结果确认路径（RESULT）——第一优先级

当前中位：`16.99775 ms`，约52.20%。

### R1-A：先做“结果确认分解”，不修改功能

必须把 RESULT 拆成：

1. `execution success event`（执行成功事件）时间；
2. `task_done / history visible`（任务真正完成 / history 可见）时间；
3. `output visible`（输出文件可见）时间；
4. `client detected ready`（客户端发现完成）时间。

目的：先知道17ms到底花在哪里。

### R1-B：固定等待 / 轮询检查

检查：

- 是否存在 `sleep`（固定暂停）；
- 是否存在较大的 `polling interval`（轮询间隔）；
- 是否在结果已可用后仍等待下一个轮询周期。

如果存在，第一单变量实验只减少/取消这个人为等待，不改变成功标准。

### R1-C：WebSocket触发 + 单次即时确认

如果 runner 目前循环轮询 history：

测试在可靠的完成事件到达后立即进行一次 history/result 确认，而不是持续轮询。

不能使用过早事件降低完成标准。

### R1-D：连接是否重复重建

检查 WebSocket 是否每轮新建。

若是，测试持久 WebSocket 连接；若已持久，则跳过。

### R1-E：验证工作是否被错误计入总时间

确认 PNG 解码、SHA-256、尺寸验证等是否在 `T_END_TO_END` 结束以后进行。

若这些只是“证明结果有效”的后验验证，而不是“结果真正可用”定义的一部分，不应误计为结果到达延迟；但不能取消验证本身。

R1 理论最大收益上限：不超过约17ms。

R1 完成条件：

- RESULT 被可靠拆分；
- 所有明显客户端人为等待被逐项验证；
- 没有剩余高收益低风险 RESULT 方案；
- 新基线稳定。

---

## R2 请求提交路径（REQUEST）——第二优先级

当前中位：`5.55075 ms`。

### R2-A：HTTP连接复用

检查每轮是否新建 HTTP 连接。

若是，测试 `persistent HTTP session`（持久 HTTP 会话/连接复用）。

若已复用，记录 `ALREADY_OPTIMAL_FOR_THIS_VARIABLE`（此变量已处于成熟状态），跳过。

### R2-B：请求体重复构建

检查 benchmark runner 是否在每轮做无必要的大量 JSON 读取、文件读取或转换。

允许把与固定 workload 无关的静态准备工作移到正式计时以前，但不能把 ComfyUI 必须完成的工作移出计时。

### R2-C：客户端库额外层

如果请求通过多层 wrapper（封装层），比较原生、成熟的本地客户端调用路径；只有在不改变任务语义时才允许测试。

R2 理论最大收益上限：不超过约5.55ms。

---

## R3 队列等待/调度路径（QUEUE）——第三优先级

当前中位：`4.71925 ms`。

### R3-A：计时边界确认

确认 EXECUTION_START 是否来自真实 `execution_start` / 对应可靠服务器事件，而不是客户端下一次 polling 才发现。

### R3-B：客户端事件处理延迟

检查 WebSocket 接收后是否有额外排队、sleep 或同步阻塞。

### R3-C：空队列调度基线

保持队列绝对为空，重复测量服务器从 queue ack 到实际执行开始的最低稳定时间。

### R3-D：不得先修改核心 ComfyUI 队列

除非前面的测量已经证明队列核心本身是主要剩余损失，否则不修改 ComfyUI queue 实现。

R3 理论最大收益上限：不超过约4.72ms。

---

## R4 节点执行与保存路径（EXECUTE / SAVE）——第四优先级

当前中位：`3.4891 ms`。

因为它现在只占约10.72%，不是首要目标。

### R4-A：先把保存时间单独隔离

必须把：

- LoadImage 读取/解码；
- SaveImage PNG 编码/写盘；

尽可能分别计时。

先测，不先改。

### R4-B：确认缓存语义

LoadImage 可能有缓存/文件哈希语义。必须确认每轮 workload 是否仍然符合 Contract，不能因为缓存让实际工作量偷偷减少。

### R4-C：保存路径/文件系统

只允许在固定输出语义下测试明显低风险变量，例如同一磁盘的合理路径差异；不能改成不保存文件来换时间。

### R4-D：PNG压缩参数

只有 Contract 明确允许、且输出语义不改变时才可测试；否则不碰。

R4 理论最大收益上限：不超过约3.49ms。

---

## R5 尾部抖动与稳定性（JITTER / P95）

当前：

`P95 / Median ≈ 1.787`

说明尾部波动明显。

在 Median 已经下降以后，必须专门处理：

- Python事件循环抖动；
- Windows调度；
- ComfyUI-Manager后台缓存刷新；
- 其他后台任务；
- 磁盘瞬时延迟；
- 首轮/偶发连接开销。

但禁止为了降低 P95 做危险系统改动、超频或全局栈替换。

目标不是只追最快一次，而是稳定的低时间。

---

## R6 测量工具自身开销（INSTRUMENTATION）

这一条贯穿所有路径。

必须区分：

- 被测系统真实时间；
- 测试程序自己的记录/JSON写盘/日志打印/哈希计算时间。

原则：

**测量工具不能成为被测对象的一大部分。**

但不能为了数字好看，把真正属于 REQUEST→RESULT_READY 必需的步骤偷偷移出去。

---

## R7 外部成熟前沿继续收窄（EXTERNAL FRONTIER REFINEMENT）

每轮如发现更可比公开数据，记录：

- 工作流；
- 分辨率；
- 节点链；
- 是否 API_READY；
- 是内部执行时间还是端到端时间；
- 硬件/软件条件。

只有足够可比的数据才能升级成 `T_EXTERNAL_EXACT`（精确外部成熟时间）。

不可比数据只保留为邻近证据。

---

## R8 第一性原理物理时间持续收窄（T_PHY REFINEMENT）

每完成一个大时间块的拆分，就重新计算：

`T_PHY_WORKING_RANGE`

如果证明某段17ms里有10ms是人为轮询，那么物理时间区间必须相应下调；如果证明其中大部分是服务器必需 persistence（持久化）时间，则区间相应收紧。

T_PHY 不是一次写死。

---

# 五、P0 99分推进关卡

## 关卡 G0：当前起点

`T_CURRENT = 32.55975 ms`

`T_PHY_WORKING_RANGE = 10–20 ms`

`P0_99 = NO`

## 关卡 G1：RESULT 主路径完成

要求：

- RESULT 已拆分；
- 明显人为等待已处理；
- RESULT 主要低风险变量已系统测试；
- 建立新的正式保留基线。

## 关卡 G2：REQUEST 主路径完成

要求：

- 连接复用/请求准备等高收益变量已验证；
- 新基线再次更新。

## 关卡 G3：QUEUE 主路径完成

要求：

- 计时边界和客户端事件延迟已排除；
- 没有明显低风险高收益队列变量遗留。

## 关卡 G4：EXECUTE/SAVE 完成

要求：

- Load 与 Save 真实组成已经明确；
- 不通过删工作量伪造优化；
- 节点路径没有明显成熟低风险高收益空间。

## 关卡 G5：P95稳定性收敛

要求：

- P95 尾部波动显著改善或已有充分证据证明剩余波动主要是系统不可控噪声；
- Median 与 P95 都可重复。

## 关卡 G6：T_PHY 收窄

要求：

- 第一版10–20ms区间经过实验更新；
- 剩余 `PHYSICAL_GAP` 有清晰解释；
- 每个主要时间块都知道其必要/可优化属性。

## 关卡 G7：99分候选

只有同时满足：

1. 当前固定任务20/20有效；
2. 当前最好结果至少多轮可复现；
3. RESULT、REQUEST、QUEUE、EXECUTE/SAVE 主要高收益路径都已系统测试；
4. 已知成熟低风险方案没有明显未尝试项；
5. 外部证据没有证明一个可直接复现、明显更快的同合同路径仍未测试；
6. `PHYSICAL_GAP` 已经显著缩小，剩余差距可解释；
7. 再做低风险方法难以取得显著稳定收益；
8. 没有通过缩水 workload、降低成功标准、危险系统修改换成绩；
9. P95 没有严重恶化；
10. 所有保留/回滚过程都有完整证据。

才允许提交：

`P0_99_CANDIDATE = YES`

然后由 ChatGPT 做最终四列法审核。

## 关卡 G8：99分冻结（99 -> FREEZE）

ChatGPT 审核通过后：

- `P0 = 99`；
- `P0 = FREEZE`（P0阶段冻结）；
- 保存最佳 Contract、时间、脚本、环境、哈希、T_PHY、外部前沿、失败方案；
- 形成稳定里程碑版本；
- 正式同步本地 skill 与 GitHub 稳定版本；
- P1 才允许解锁。

---

# 六、第一轮具体实验顺序

当前不要同时测试所有路径。

正式顺序：

### 实验 E1：RESULT 纯分解实验

只增加更细粒度时间戳，不改变结果确认逻辑。

目标：把16.99775ms拆开。

该实验本身不作为性能新纪录，主要用于定位。

### 实验 E2：RESULT 第一高价值单变量

由 E1 证据决定。

优先顺序：

1. 固定 sleep / polling interval；
2. 结果已ready但客户端晚发现；
3. WebSocket/history触发方式；
4. 连接重建；
5. 验证工作误计入总时间。

一次只做其中一个。

### E3及以后

只有 E2 完成并经 ChatGPT 审核以后，再授权下一单变量。

禁止 Codex 一口气自动跑完 R1-R8；否则无法知道每个收益来源。

---

# 七、每轮 GitHub 报告固定中文结构

每一轮 `REPORT.md` 固定包含：

1. 本轮目的；
2. 上一基线；
3. 单一假设；
4. 为什么选择它；
5. 预计最大收益；
6. 实际只修改了什么；
7. 什么明确没有修改；
8. 3次预热结果；
9. 20次正式结果；
10. Median / P95 / MIN / MAX；
11. REQUEST / QUEUE / EXECUTE / RESULT；
12. 输出有效性；
13. 与上一基线相比改善/退化百分比；
14. 保留或回滚；
15. 当前四项纵向状态；
16. T_PHY 是否收窄；
17. 新增经验；
18. 失败经验；
19. 下一步候选；
20. Git commit 与共同办公区路径。

所有英文技术字段必须同时带简洁中文说明。

---

# 八、当前正式下一步

当前不是直接宣布99。

当前授权的第一动作应为：

`E1 = RESULT_PATH_DECOMPOSITION`

中文：

**结果确认路径的纯分解实验。**

它只负责把当前约17ms的 RESULT 拆清楚，不先做优化。

E1证据同步到共同办公区后，由 ChatGPT 选择第一个真正的单变量优化实验 E2。

当前状态：

`P0_CONVERGENCE_PLAN = READY`

`P0_99 = NO`

`NEXT = E1_RESULT_PATH_DECOMPOSITION`
