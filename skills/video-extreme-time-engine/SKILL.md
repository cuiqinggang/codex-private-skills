---
name: video-extreme-time-engine
description: 视频极限短时间引擎。用于在固定 VALID 规格下，把视频生成任务从可用结果持续收敛到最短真实 T_VALID；强调 GPT 虚拟成熟、Freeze、Reality 执行、阶段计时、warm path、轻量 verifier、单闭环 runner 和 Reality 反哺。首个正式案例为 H3-P1。
---

# 视频极限短时间引擎 V1.0（整数版）

版本：1.0.0。发布日期：2026-10-16。此为本技能主版本；三人行V2、历史制作V2/V3是独立方法/模式编号，不随本次升级变更。

## V1.0 成果与时间口径
先读 [H3成果、230秒纠错与后续优化](references/H3_TIME_ACCOUNTING_V1.md)。保存Star7受保护FP16路径的本轮实测：首次469.167秒、同条件热态172.128秒。它们是生成计时，不是完整T_VALID或物理下界；跨场景质量尚未通过。
撤销旧约230秒“物理极限”说法：那是跨运行拼接的旧路径估算，应与热态口径说明，禁止改称首次生成下界来解释172秒的新成绩。
继续优化先按完整任务计算净收益；阶段快2倍不等于整体快2倍。保留原基线，冻结后再实际验证。


## 整体攻击迭代规则（用户2026-10-16纠正）
继续提速时读取 [全节点成熟方案比较与整体融合](references/H3_WHOLE_ROUTE_R5.md)。以172.128秒R4热态及469.167秒首次成果为保底，不退回零起点。
覆盖每个潜在收益节点，比较适用成熟候选、兼容性、质量与资源副作用，再形成最多三套完整组合；反复攻击和刷新整套方案，冻结后才做一次预先定义的现实验收批次。禁止将单节点收益估算充当整体虚拟成熟，禁止优化一点生成一次。
新候选只有同输入、同质量、同计时边界的完整实测更好才晋级；不保证未测试候选必然更快，不删除原成果。R5已完成固定版本准入、冻结及一次首次/热态实际批次，见 [R5实际结果](references/H3_R5_REALITY_RESULT.md)。首次490.504秒慢于R4，热态49.707秒有性能收益，但音画数值有差异、显存上升，尚未完整同质量认证，不全局晋级；保留R4默认及全部证据。不要重做准入或重复生成来恢复进度。

## 本地 H3 实测优先入口（2026-10-16升级）
用户要求本地MiniMax H3生成、恢复原来200～300秒流程或诊断GPU低利用率时，先读取 [本地已验证基线与差分恢复](references/H3_LOCAL_GOOD_BASELINE_V1.md)，并使用 [原成功工作流合同](assets/h3-kitchen-warm-good-20261016.json) 做逐字段对照。
这次升级保存可复用的实际成功方案、缓存前提和失败证据；不代表原片同画质400秒已通过。用户已明确本地时，本入口优先于历史V3候选中的云端首选排序；不自动迁移云端。
按用户指定《三人行》V2 C002执行，Windows桥V7以C通道为入口、A暂停。模型加载方式默认沿用已实测dynamic；streaming仅是中断候选，不得当成验证成功的优化。
先建立GOOD/BAD/FIRST_DELTA；必须区分同条件热生成、新条件生成、完整冷启动，以及生成秒数与含质量验收的T_VALID。不以无进度事件单独证明死锁。
保留旧H3-P1、V2与V3历史，各自验收结论互不继承。

## 目标

唯一优化目标：

```
T* = min(T_VALID)
```

前提是任务保持同一 `VALID_SPEC`。质量、正确性、音画对应、展示可用性等只决定候选是否进入 VALID 集合，不与时间并列评分。

本技能继承 `first-principles-physical-limit-convergence-v5.6.5` 的状态机和时间语义。

## 状态机

```
10 虚准备
→ 20 虚冻结
→ 30 虚实交接
→ 40 Reality执行/审核
→ 100 GPT最终完成
```

Reality Executor 最高合法状态为 40。只有 GPT Final Reviewer 可以 40→100。

## 两类时间

- `T_FLOW`：本轮实际流程耗时。
- `T_VALID`：被冻结业务任务从正式开始到最后一个必要 VALID 条件 PASS 的真实时间。
- `T*`：同一 VALID 规格下最短的已认证 `T_VALID`。

禁止用局部阶段时间、`T_FLOW`、估计值或失败候选冒充 `T_VALID/T*`。

## 核心工作法

### 1. 固定 VALID
先冻结任务必须满足的有效条件，例如：
- 视频主体/动作；
- 语音内容；
- 音画同步；
- 最低展示质量；
- verifier 要求。

不得为了缩短时间偷偷改变 VALID。

### 2. GPT 连续虚拟攻击
GPT 在 Reality 前连续攻击当前最大收益点：

```
找最大瓶颈
→ 假设消除
→ 重算整体时间结构
→ 再找最大瓶颈
→ 继续
```

直到继续攻击的长期预期收益不值得新增复杂度、维护成本或 VALID 风险。

### 3. Freeze 后再 Reality
Codex/Reality 只执行冻结方案，不负责探索“下一步怎么优化”。

Reality 若遇到具体实现失败：
```
返回 GPT
→ 局部最小修复
→ 新 Freeze
→ 再 Reality
```

### 4. 优先攻击顺序

默认优先级：

1. 非必要编排空耗；
2. 冷启动 / 模型重复加载 / conditioning 重算；
3. verifier 重复加载、重复 decode、串行等待；
4. 不必要输出长度/帧数；
5. steps；
6. resolution；
7. 更深 sampler / 算子 / 模型路径。

越往后 VALID 风险越高，必须由 Reality 证据决定是否继续。

## 推荐架构

对高重复视频任务优先采用：

```
SINGLE_LOCAL_CLOSED_LOOP_RUNNER
+ WARM_MODEL_STATE
+ SAFE_CONDITIONING_REUSE
+ NEW_SAMPLER_EXECUTION
+ BOUNDED_OUTPUT_PUBLICATION_WAIT
+ SINGLE_DECODE
+ SINGLE_UNPROMPTED_ASR
+ PARALLEL_NONDEPENDENT_VERIFIERS
+ VALID_END_BEFORE_REPORT_PACKAGING
```

### 单闭环 runner
生成完成后直接取得本次 output，继续 decode / save / verify。不要让人工或智能体在阶段之间重新观察后才触发下一步。

### Warm path
正常生产态允许安全复用：
- 已运行服务；
- 已驻留模型；
- 固定 workflow；
- 匹配的 conditioning；
- 静态节点缓存。

但必须保证新的 sampler 真正执行，不能直接复用旧最终 latent 或旧视频。

### 输出发布竞态
如果生成完成后 history/output 尚未发布：
- 同一 prompt_id 短轮询；
- 条件满足立即继续；
- 有界超时；
- 不因 `{}` 直接 KeyError；
- 不自动二次生成。

### Verifier
VALID 标准不减，但避免：
- 重复 decode；
- 同一音频重复 ASR；
- 同一帧重复抽取；
- 不必要串行；
- 报告/ZIP/哈希/知识库检查拖长 T_VALID。

`T_VALID_END` 必须停在最后一个必要 VALID verifier PASS 的时刻。

## Seed 规则

如果任务是固定内容生成，而 Reality 已证明某 seed 在同一模型/参数下稳定得到 VALID，则允许 Freeze 该 seed。

目的不是证明所有随机 seed 都稳定，而是减少随机失败和重试。

固定 seed 不代表允许复用旧最终输出；必须有新 prompt_id、新 sampler 执行和新 output。

## 收敛判断

当：
- 大型编排空耗已消失；
- warm path 已 Reality 证明；
- verifier 已轻量化；
- 剩余主要是不可控运行波动或需高风险改参；
- 继续攻击预期收益 <= 复杂度 + 维护成本 + VALID 风险；

则允许停止主动攻击，冻结当前正式 `T*`。

后续正常使用若自然产生更短、同 VALID 的完整 `T_VALID`，再被动更新 `T*`。

## 首个正式 Reality 案例

见：
- [FREEZE.md](FREEZE.md)
- [CASE-H3-P1.md](CASE-H3-P1.md)

H3-P1 已将正式 `T*` 从 653921.787ms 收敛到 288281.990ms，累计改善约 55.915%，约 2.268x 加速。

## 边界

- 不把不同 VALID 规格直接比较。
- 不把失败候选的阶段和当成 T*。
- 不因追求理论极限无限测试。
- 不让 Reality Executor 自行改变 Freeze。
- 不把“测试更快”凌驾于“结果有效”。


## Codex+H3 视频制作 V2.0：全帧源图连续制作（2026-10-12）

本技能包新增独立的全帧真实源图模式。其正式规范见 [CODEX_H3_V2_FULL_FRAME.md](CODEX_H3_V2_FULL_FRAME.md)。本模式废止8张稀疏源图覆盖56帧作为正式生产验收的路线，要求每帧均由Codex调用真实生图/编辑模型独立生成，并逐帧检验，再由FFmpeg无插帧编码；H3为可选对照组件。V2.0为方法升级，Reality Test 02尚未通过，不继承H3-P1的VALID或T*。
