---
name: first-principles-physical-limit-convergence
description: 整体闭环极限短时间引擎 v5.2.3。唯一目标 T*=min(T_VALID)；顶层永久只有“虚→实”；最高级验收是“真实使用测试”：用正式使用同构的入口、路径、环境和用户可见输出全面验证冻结产品；低层测试负责组合覆盖、快速定位与防回归。
metadata:
  version: "5.2.3"
  display_name: "整体闭环极限短时间引擎"
  release_state: "VIRTUAL_MATURE_REAL_USAGE_TEST_READY"
---

# 整体闭环极限短时间引擎 v5.2.3

## CURRENT v5.2.3：执行分隔符单点兼容补丁

v5.2.2 的技能包级 Scope Gate 真实使用测试结果为 FAIL，且已确认是单点产品缺陷：实际接收命令包含完整执行正文，但 Markdown 在“执行：”行尾加入单个反斜杠，旧 Gate 只接受精确的“执行：+换行”，因此误报 `EXECUTION_BODY_MISSING`。

v5.2.3 只修这一点：
- 接受“执行：”后直接换行；
- 接受“执行：”后单个 Markdown 行尾反斜杠再换行；
- 双反斜杠继续拒绝；
- Header-only、缺正文继续拒绝。

明确不改：
- 父 Renderer；
- 数字时间规则；
- Freeze/Git Object 物化；
- T-star Markdown 等价规则；
- 技能包级跨业务 Scope 规则；
- 返回合同；
- DSE 业务逻辑。

GPT 侧逻辑回归：`8/8 PASS`。精确冻结 blob 的最终验证仍必须由下一轮真实使用测试完成。

当前 Freeze：
`ESTE-v5.2.3-SCOPE-MARKER-VIRTUAL-FREEZE-R1`

当前：
- `VIRTUAL_MATURE=YES`
- `SOLUTION_FROZEN=YES`
- `REAL_USAGE_TEST=READY_TO_DISPATCH`
- `FINAL_VALID=NO`
- `DONE=NO`

---

## CURRENT v5.2.2：技能包级 Reality Dispatch 范围门

v5.2.1 的历史 FINAL_VALID 被新的真实产品 Delta 重新打开。新证据来自 DSE 下游真实输出：任务已经标为 `实`，但只显示 Locator/时间/Timeline/Freeze 状态头，没有完整执行正文和返回合同。

这证明 v5.2.1 的现实验收范围只覆盖了核心 Renderer 自己，并没有证明“本技能包范围内任意业务进入实阶段时都一定受同一派发合同约束”。

v5.2.2 只修这一处范围缺口：

- 所有明确使用、继承或受本技能包治理的业务任务，只要用户可见输出出现 `【页面名｜任务名｜01-06｜实】`，自动进入技能包级 Scope Gate；
- 业务名称不是白名单，不需要 DSE/HIPE/H3 等分别写适配器；
- 所有业务统一使用 `runtime/scope_gate_v5_2_2.py::build_in_scope_real_dispatch`；
- 所有“实”阶段最终用户可见输出在发送前必须通过 `enforce_in_scope_final_output`；
- Header-only、自由手写半截 Reality Dispatch 一律 INVALID，不允许发送。

完整 Reality Dispatch 至少必须具备：
- REAL Locator；
- 数字时间锚；
- TIMELINE_ID / TIME_ORIGIN_UTC / DISPATCH_UTC；
- FREEZE_ID / FREEZE_REF / CONTRACT_REF；
- 非空“执行”正文；
- RESULT=PASS|FAIL|BLOCKED；
- RETURN_TO_GPT=YES；
- NO_FINAL_VALID_DONE=YES。

真实反例：用户提供的 DSE v1.0.3 Header-only 输出必须被 Scope Gate 拒绝。

当前精确 blob 低层回归：
- `6/6 PASS`
- Parent Renderer blob=`2a56e186ec94d912fa4d6b461657bdfd9c2fb068`
- Scope Gate blob=`c04af6af12c1f4d6555788b538b439dc97fd9ca5`
- Scope Test blob=`54882ccaac49d5af129bfcd04cd36e612668a196`
- Evidence=`docs/first-principles/v5.2.2/VIRTUAL-MATURITY-REPORT-R1.json`

当前 Freeze：
`ESTE-v5.2.2-SKILL-WIDE-SCOPE-GATE-VIRTUAL-FREEZE-R1`

当前：
- `VIRTUAL_MATURE=YES`
- `SOLUTION_FROZEN=YES`
- `REAL_USAGE_TEST=READY_TO_DISPATCH`
- `FINAL_VALID=NO`
- `DONE=NO`

---

## CURRENT v5.2.1：FINAL VALID

v5.2.1 不改变 v5.2.0 R4 已通过的整体设计与产品逻辑，只做版本收口和经验固化。

当前判定：
- `CORE_OVERALL=PASS`
- `R4_REAL_USAGE_TEST_EXECUTABLE_SCOPE=PASS`
- `PRODUCT_DEFECT_ESTABLISHED=NO`
- `FINAL_VALID=YES`
- `DONE=YES`

明确保持不变：
- Runtime / Renderer；
- 低层测试；
- 数字时间锚与 Timeline；
- Markdown T-star 语义等价规则；
- 简洁可见派发；
- 01–06 Locator；
- Git Object Bytes 冻结物化原则；
- “单点故障只做单点修复”原则。

R4 已实际证明：Freeze/Manifest 原始字节匹配、Git Object 无损物化、10/10 低层回归 PASS、接收原文 Validator PASS、Freeze→实 PASS、Locator/时间锚/简洁派发 PASS。

最终收口判定：R4 已提供足够的真实使用测试证据，不再为了形式完整重复跑一轮收尾测试。局部时间独立起点、额外宿主级来源证明、人工制造 EXTERNAL_BLOCK 均降为非阻断项；未来自然发生时再留证。v5.2.1 只有出现新的真实产品 Delta 或系统性架构问题才重新打开。

最终证书：
`docs/first-principles/v5.2.1/FINAL-VALID-CERTIFICATE.json`

经验文档：
`docs/first-principles/v5.2.1/REPAIR-LESSONS-R1-R4.md`

---

## CURRENT v5.2.0 权威状态

当前页面名称：

`整体闭环极限时间引擎 5.2版`

v5.2.0 是结构性升级，不是 v5.1.1 的补丁号延伸。v5.1.1 R2 的真实使用结果固定保留为历史失败证据：

- `REAL_RESULT=FAIL`
- `REAL_T_VALID_MS=175000`
- 数字时间锚用户可见：PASS
- 首次调用生产出口即因时间锚正则双重转义失败：FAIL
- 唯一生产 Renderer、禁止旁路、缺 Timeline 分支均未获得完整现实证明
- 未实际执行的低层检查曾被错误预报为 PASS；该行为在 v5.2.0 中明确禁止

### 最高级验收术语

从 v5.2.0 R3 起，最高级验收统一称：

`REAL_USAGE_TEST / 真实使用测试`

它仍然是测试；区别是必须使用正式使用同构的入口、路径、环境和用户可见输出，目标仍是全面验证产品真实有效状态，并尽量在交付到日常使用前暴露问题。

原因：正式生产任务本身就是最终观察场。软件缺陷允许在真实使用中被发现，但发现后本轮必须失败，立即回虚修复；修复完成后先做低层测试，再形成新 Freeze，再从新的正式入口重新真实使用。

低层的单元、回归、随机、Mutation、故障注入仍可称“测试”，但它们不得代替真实使用签发最终证书。

### 证据状态硬规则

每个尚未实际执行的检查初始只能是：

`NOT_RUN`

只有存在对应的实际执行证据，才能改为：

`PASS / FAIL / BLOCKED`

以下均不得推导 PASS：

- 代码文件已经存在；
- 测试脚本已经写好；
- GPT 静态阅读认为正确；
- 理论上应该通过；
- 上一版本曾通过相似检查。

### v5.2.0 当前虚拟成熟收口

- `FREEZE_ID=ESTE-v5.2.0-REAL-USAGE-VIRTUAL-FREEZE-R1`（历史 R1；真实使用 FAIL）
- 精确仓库 blob 低层回归：`6/6 PASS`
- 证据：`docs/first-principles/v5.2.0/VIRTUAL-MATURITY-REPORT-R1.json`
- `VIRTUAL_MATURE=YES`
- `SOLUTION_FROZEN=YES`
- `REAL_USAGE=READY_TO_DISPATCH`
- 此状态不得以总结结束；必须在同一用户可见回复继续发布带完整时间合同的 `实` 命令。

### v5.2.0 R2 真实使用失败回流与虚拟成熟

R1 真实使用固定保留：
- `REAL_RESULT=FAIL`
- `REAL_T_VALID_MS=541106`
- `EXECUTOR_ELAPSED_MS=351106`
- 根因：`VALIDATOR_OVERCONSTRAINT_TRANSPORT_EQUIVALENCE_FALSE_NEGATIVE`

判定：
- 数字时间锚、Timeline、可审计时间合同仍是必要硬门；
- Markdown 传输把 T-star 显示 token 加一层转义，不改变其语义，不应成为失败条件；
- R1 不得追认 PASS，因为 R1 冻结 Validator 在真实使用中确实失败；
- R2 只接受原形与单层 Markdown 转义两种等价表示，双层转义和 token 改名仍拒绝。

R2 精确 blob 低层回归：
- `8/8 PASS`
- Runtime blob=`b8693ce4cd5b96678ffba8cd7305cf9d0959c8f0`
- Test blob=`736f09a1970b1a07baf092928d81f6b485ddf3fa`
- Evidence=`docs/first-principles/v5.2.0/VIRTUAL-MATURITY-REPORT-R2.json`

当前：
- `FREEZE_ID=ESTE-v5.2.0-REAL-USAGE-VIRTUAL-FREEZE-R2`
- `VIRTUAL_MATURE=YES`
- `SOLUTION_FROZEN=YES`
- `REAL_USAGE=READY_TO_DISPATCH_R2`
- `FINAL_VALID=NO`
- `DONE=NO`

### v5.2.0 R3：真实使用测试 + 简洁控制面

R2 原始结果保留为 FAIL，但归因：
- `FAIL_SOURCE=TEST_HARNESS`
- `PRODUCT_DEFECT_ESTABLISHED=NO`
- 原因：Codex 临时编写的参数提取辅助脚本在调用冻结 Renderer 前 KeyError。
- 以后真实使用测试禁止现场编写临时辅助脚本；必要自动化必须在虚拟阶段预先实现并 Freeze。

真实使用测试的“全面”固定为：
- 覆盖冻结合同的全部关键功能、控制边界、用户可见行为；
- 覆盖 NORMAL / PRODUCT_DELTA / EXTERNAL_BLOCK 三类顶层旅程；
- 大量组合、随机、Mutation 等仍由低层测试承担，避免在最高层重复制造昂贵样本。

Codex 用户可见派发改为最小控制面：
- 保留 Locator、数字时间锚、Timeline、Freeze ID、Freeze Ref、Contract Ref、简短执行目标和返回合同；
- 完整 blob/hash 清单进入 Freeze Manifest；
- 长验收合同进入 Contract；
- 禁止在可见命令中重复展开机器字段。

R3 精确 blob 低层回归：
- `10/10 PASS`
- Runtime blob=`2a56e186ec94d912fa4d6b461657bdfd9c2fb068`
- Test blob=`6c97278955f38883b4de56153fa765789ce4f56b`
- Evidence=`docs/first-principles/v5.2.0/VIRTUAL-MATURITY-REPORT-R3.json`

当前：
- `FREEZE_ID=ESTE-v5.2.0-REAL-USAGE-TEST-VIRTUAL-FREEZE-R3`
- `VIRTUAL_MATURE=YES`
- `SOLUTION_FROZEN=YES`
- `REAL_USAGE_TEST=READY_TO_DISPATCH_R3`
- `FINAL_VALID=NO`
- `DONE=NO`

### v5.2.0 R4：单点故障只做单点修复

R3 真实使用测试结果保留：
- `RESULT=FAIL`
- `FAIL_SOURCE=TEST_HARNESS`
- `PRODUCT_DEFECT_ESTABLISHED=NO`
- 根因：Windows worktree 将 Git 中的 LF 自动物化为 CRLF；`git diff` 因换行归一化为空，但原始工作区 bytes 不等于 Freeze blob。

R4 只修这一点：
- Freeze 字节身份的权威源改为 `GIT_OBJECT_BYTES`；
- 精确字节执行时从 Git 对象数据库无损物化，不经过会改换行的 worktree；
- worktree 原始 bytes 不再作为跨平台 Freeze 身份证据；
- 禁止为了验收修改 `core.autocrlf`、Windows Git 设置或重新提交 CRLF 版本。

最小修改原则：
- `ISOLATED_FAILURE_REQUIRES_ISOLATED_FIX`
- 只有证据证明系统性/架构性根因时才允许扩大修改面；
- 否则所有无关已通过资产必须保持不变。

R4 虚拟成熟结论：
- `VIRTUAL_MATURE=YES`
- `SOLUTION_FROZEN=YES`
- `PRODUCT_ASSETS_CHANGED=NO`
- R3 已实际执行的 10/10 PASS 证据因 Runtime/Test blob 完全不变而继续适用于相同产品资产；
- R4 新增物化规则本身必须由下一轮真实使用测试验证，当前不提前写 PASS。
- `REAL_USAGE_TEST=READY_TO_DISPATCH_R4`

本轮明确不改：
- Runtime / Renderer；
- 低层测试逻辑；
- 时间锚与 Timeline；
- Markdown T-star 等价规则；
- 简洁派发；
- 01–06 Locator；
- 产品功能逻辑。

R3 产品 blob 继续保持：
- Runtime=`2a56e186ec94d912fa4d6b461657bdfd9c2fb068`
- Test=`6c97278955f38883b4de56153fa765789ce4f56b`

### v5.2.0 生产交接

唯一生产 Reality Dispatch Renderer：

`runtime/production_handoff_v5_2_0.py::build_real_dispatch`

合同：

`docs/first-principles/v5.2.0/REAL-USAGE-TEST-CONTRACT-R4.json`

低层回归：

`tests/test_production_handoff_v5_2_0.py`

当前状态：

- `phase=虚`
- `VIRTUAL_MATURE=YES`
- `LOW_LEVEL_REGRESSION=PASS (6/6 exact-blob execution)`
- `REAL_USAGE=READY_TO_DISPATCH`
- `FINAL_VALID=NO`
- `DONE=NO`

---

## HISTORICAL：v5.1.1 R2 权威状态与两项 Reality Delta 封堵（真实使用失败证据）

当前新增 Freeze：

`ESTE-v5.1.1-HANDOFF-TIME-R2`

当前状态：

- `VIRTUAL_MATURE=YES`
- `SOLUTION_FROZEN=YES`
- `REAL_STARTED=NO`（直到真实用户可见的 Reality Dispatch 发出）
- `REAL_USAGE_VALIDATION=PENDING`
- `FINAL_VALID=NO`
- `DONE=NO`

本轮只封堵两个已被正式使用证明存在的 Reality Delta：

1. **虚拟成熟后未自动进入实。** 旧 v5.0.8 Gate 只会在调用时校验候选文本，没有拥有正式发送出口；合同还明确标记 `host_response_auto_hook=REQUIRES_CALLER_BINDING`。因此“Gate 存在”不能机械保证用户可见回复会继续到 `REAL_DISPATCH`。
2. **Codex 实命令时间字段偶发遗漏。** 旧 Gate 只检查时间字段是否存在，却不负责生成 Reality Dispatch；自由手写命令可绕开 Gate，所以时间锚、`TIMELINE_ID`、`TIME_ORIGIN_UTC`、`DISPATCH_UTC` 不能保证每次出现。

R2 结构性修复：

- 唯一生产 Reality Dispatch 出口固定为：
  `runtime/production_handoff_v5_1_1.py::close_virtual_and_build_real_dispatch`
- 一旦 `VIRTUAL_MATURE=YES && SOLUTION_FROZEN=YES && REAL_STARTED=NO`，禁止以“总结/Freeze 完成/等待下一步”结束；下一用户可见控制输出必须是 `REAL_DISPATCH`。
- Renderer 自己生成 Locator、数字时间锚、Timeline、Freeze、Reality VALID、计时边界与返回合同，然后在返回前自校验；不再允许“先手写文本，再可选地调用 Validator”。
- 缺真实可审计 Timeline：`BLOCK`，禁止伪造时间。
- 手工/旁路 Codex Reality Dispatch：`INVALID_PRODUCTION_PATH`。
- PASS / FAIL / BLOCKED 全部固定 `RETURN_TO_GPT=YES`，Reality 执行器不得宣布 `FINAL_VALID/DONE`。

R2 合同：

`contracts/PRODUCTION-HANDOFF-v5.1.1-R2.json`

R2 回归：

`tests/test_production_handoff_v5_1_1.py`

低层回归只能证明实现可工作，不能签发真实用户旅程证书。v5.1.1 是否真正封堵，仍必须由本次正常正式用户旅程证明。

---

## HISTORICAL：v5.1.1 冻结规则

当前页面名称：

`整体闭环极限时间引擎 5.1.1版`

当前版本：

`5.1.1`

前代 v5.0.8 / v5.0.9 / v5.1.0 只作为历史演化与 Reality Delta 证据，不再作为当前版本。

### 0.1 测试第一性原理

测试的唯一目的：在正式交付前，以最短有效时间发现“用户正式使用时会失败”的问题。

当前最高级测试原则固定为：

1. **正式怎么用，测试就怎么测。**
2. **测试对象是用户真正看到和得到的结果，不是内部状态或实现。**
3. **测试器只观察，不帮助系统补步骤、补字段、推进状态或调用正式运行不会自己调用的逻辑。**
4. **真实使用发现的错误：记录 → 找根因 → 修复 → 下沉为低层回归测试 → 重新完整真实任务。**

形式化要求：

`TEST_ENTRY == PRODUCTION_ENTRY`

`TEST_PATH == PRODUCTION_PATH`

`TEST_OUTPUT == USER_VISIBLE_PRODUCTION_OUTPUT`

任一不成立：

`TEST_IS_NOT_RELEASE_EVIDENCE`

### 0.2 最高级验收：真实用户旅程

最高级验收采用少量、完整、与正式使用同构的真实任务，不允许以测试专用入口替代。

最低覆盖三类真实旅程：

- 正常：`虚 → 实 → PASS → FINAL_VALID`
- 差异：`虚 → 实 → FAIL → 回虚`
- 阻断：`虚 → 实 → BLOCKED → RETURN_TO_GPT`

测试必须从用户正常自然语言任务开始，完整经过真实 GPT 输出、真实时间显示、真实 Freeze、真实 Codex CHAT 自然语言派发、真实返回和 GPT 最终收口。

只要途中需要人工提醒系统“补时间、补 Locator、补 Timeline、继续进入实、修正 RETURN_TO_GPT”等，整轮真实用户旅程即判 FAIL。

### 0.3 低层测试的正确角色

单元测试、状态矩阵、随机测试、Mutation、故障注入、组件集成测试全部保留，但只用于：

- 快速定位错误；
- 提前发现已知错误；
- 防止现实失败复发；
- 缩短真实用户旅程失败后的修复时间。

它们不能单独签发：

- `REAL_CERTIFIED=YES`
- `LIVE_E2E_ENFORCED=YES`
- `FINAL_VALID=YES`
- `DONE=YES`

真实用户旅程是最终裁决对象。

### 0.4 现实失败回流

当真实用户旅程发现错误：

`真实失败 → Reality Delta → 根因 → 修复 → 低层回归 → 新 Freeze → 从 TASK_ACCEPTED 重新完整真实任务`

禁止在正在验收的同一轮任务中现场补丁后继续算 PASS。

### 0.5 当前状态

`RULE_FROZEN=YES`

`REAL_USAGE_VALIDATION=PENDING`

`SEVEN_STAR_CERTIFIED=NO`

`FINAL_VALID=NO`

`DONE=NO`

v5.1.1 是否有效，只允许由下一次正式使用方式的真实用户旅程证明，不预先宣布“七星”。

---

## 1. 唯一目标

唯一优化目标永久只有：

`T* = min(T_VALID)`

其中：
- 正确性、安全、质量、完整性、任务要求、证据要求决定结果是否进入 `VALID` 集合；
- 只有进入 `VALID` 集合的现实结果，才允许按 `T_VALID` 比较快慢；
- 不再引入“时间+质量+成本+安全”的第二评分轴。

顶层 `T_VALID` 固定为：

`T_CLOSED_LOOP_VALID`

即从 `TASK_ACCEPTED` 到 `FINAL_VALID` 的整体闭环有效时间。

---

## 2. 顶层状态机

顶层永久只有两步：

`虚 -> 实`

### 虚
负责：
- 设计；
- 成熟方案吸收；
- 实现物化；
- GPT 独立验证；
- 故障注入；
- 等价性验证；
- Freeze；
- Reality Capsule；
- 时间收口。

### 实
只执行已经冻结的 Reality。

现实失败只能：

`Reality Delta -> STOP -> 回虚 -> 吸收差异 -> 新 Freeze -> 再实`

禁止在当前 Freeze 下现场修改、现场修复、原地重试或换路线。

---

## 3. Reality 的最终判定规则

### 3.1 现实有效性优先

现实结果先判断：

`REAL_VALID = YES / NO`

现实有效的基本要求由当前任务冻结合同决定，例如：
- 语义/功能检查全部通过；
- 冻结资产一致；
- Reality 前置物化通过；
- 必要安全与证据门通过。

### 3.2 虚拟性能预测不是现实硬门

虚拟阶段得到的性能预测、估算值、跨环境换算值，只能作为：
- 优化目标；
- 假设；
- Reality 前的参考锚；
- Reality Delta 对照值。

除非时间本身是外部任务明确规定的硬约束，否则：

`REAL_T > VIRTUAL_PREDICTION`

不得自动推出：

`REAL_VALID = NO`

Reality 的职责是让现实修正虚拟模型，不是让虚拟预测否定现实。

### 3.3 现实 T* 的最终来源

最终性能锚必须来自现实有效结果：

`REAL_T* = min(REAL_VALID_T)`

如果存在多个现实有效候选：
- 保证任务语义等价；
- 使用冻结的同一测量协议；
- 比较现实有效候选的实际测量结果；
- 最短有效现实时间成为最终 `T*`。

---

## 4. 最终优化收口规则

当首次 Reality 已经证明：
- 功能正确；
- 现实可执行；
- 但仍存在明确、低成本、可证明的性能浪费；

允许：

`一次明确优化 -> 一个新 Freeze -> 一次最终 Reality`

禁止无限追求虚拟预测值。

最终 Reality 推荐：
- 保留现实有效基线作为候选 A；
- 加入语义等价优化版作为候选 B；
- 每个候选先预热，再进行固定次数正式现实测量；
- 所有正式样本必须满足任务有效性；
- 优化版无效时只淘汰优化版，不否定有效基线；
- 所有现实有效候选中，最短实际时间成为最终 `T*`；
- 最终 Reality 完成后必须收口，不进入无休止优化循环。

v5.0.8 最终 Reality 使用：

`warmup=1000`

`samples=1000`

并记录：
- MIN
- P50
- P95
- MAX

唯一排序指标仍然是有效样本中的最短现实时间；P50/P95/MAX 用于诊断稳定性，不构成第二优化目标。

---

## 5. HISTORICAL：v5.0.8 最终现实认证结果（历史证据，非 v5.1.1 当前状态）

最终冻结：

`ESTE-v5.0.8-REALITY-FIRST-FINAL-CLOSEOUT-VIRTUAL-FREEZE-R4`

Freeze 一致性：

`31/31 PASS`

两个候选均通过现实有效性：

### R3 基线
- VALID：1000/1000
- MIN：0.0074 ms
- P50：0.0077 ms
- P95：0.0093 ms
- MAX：0.6865 ms

### R4 优化版
- VALID：1000/1000
- MIN：0.0027 ms
- P50：0.0028 ms
- P95：0.0030 ms
- MAX：52.2077 ms

最终赢家：

`R4_OPTIMIZED`

最终现实认证：

`CERTIFIED_REAL_T_STAR_MS = 0.0027 ms`

即：

`2.7 微秒`

历史虚拟预测：

`0.01136838145574825 ms`

只保留为历史预测证据：

`HISTORICAL_PREDICTION_IS_GATE = NO`

---

## 6. HISTORICAL：v5.0.8 整体闭环最终时间（历史证据）

v5.0.8 历史正式 Timeline：

`ESTE-v5.0.7-NUMERIC-TIME-ANCHOR-01`

最终：

`FINAL_CLOSED_LOOP_T_VALID_MS = 9983551.271 ms`

即：

`02:46:23.551271`

v5.0.8 历史最终状态：

`FINAL_VALID = YES`

`REAL_CERTIFIED = YES`

`DONE = YES`

---

## 7. 时间连续性

每个任务首次进入建立且以后不可更换：
- `TIMELINE_ID`
- `TIME_ORIGIN_UTC`

所有虚/实转换只向同一账本追加事件。

关键控制边界必须显式携带数值时间：
- TASK_ACCEPTED
- DECISION_COMMIT
- VIRTUAL_MATURITY_TIME_CLOSEOUT
- FREEZE_COMMIT
- REAL_DISPATCH
- EXECUTOR_RETURN_PASS
- EXECUTOR_RETURN_FAIL
- EXECUTOR_RETURN_BLOCKED
- RETURN_TO_VIRTUAL
- FINAL_VALID

规则固定：

`ALWAYS COUNT + PRINT AT CONTROL BOUNDARY`

禁止：
- N/A
- NA
- NULL
- MISSING
- Infinity
- NaN
- 空值

状态词不能代替时间数字。

---

## 8. Freeze 与 Reality 资产规则

正常权威源：

`REMOTE_SHARED_REPO_DIRECT`

Reality 必须按冻结的：
- repository
- branch/commit
- path
- blob

读取权威资产。

共同私库正常时禁止：
- 下载包中转；
- 让用户重新找本地位置；
- 无目的扫描本地磁盘；
- 现场切备用路径。

Freeze 后任何冻结资产变化，旧 Freeze 不再代表新资产。

认证过的 Freeze 必须保持不可变；后续文档/发布说明更新不得改写历史 Reality 证据。

---

## 9. Reality 物化规则

可执行 Reality Capsule 使用无损物化路径。

v5.0.8 最终采用：
- Git 原生对象字节；
- Python subprocess 参数数组；
- `shell=False`；
- `text=False`；
- 原始 bytes；
- 精确 Git blob 校验；
- ASCII-only；
- `compile(bytes)`；
- fresh namespace exec；
- callable 检查。

禁止依赖：
- btoa
- atob
- Buffer
- JavaScript Base64 转码
- PowerShell 文本管道重新编码冻结源码

前置物化属于 Reality 前置门，不混入核心证书计时。

---

## 10. 执行器与固定约束

执行适配器：
- CODEX -> CHAT
- PLAYWRIGHT -> NATIVE_BROWSER
- REASONIX -> UI_AGENT
- LOCAL_FROZEN -> FROZEN_RUNNER

对 Codex：
- 只发送 Codex CHAT 自然语言任务；
- 禁止 PowerShell/Shell/`codex exec` 作为用户派发模式；
- Locator 固定使用：
  `【页面名｜任务名｜序号｜虚/实】`
- 同一连续 Reality 任务序号最多 01–06；
- 第 6 次仍未完成必须 STOP -> 回虚；
- 结构性 Reality Delta 可提前回虚，不必机械耗尽 6 次。

禁止修改：
- FlClash
- Windows 代理
- 系统网络设置

---

## 11. 真实回复执行绑定与结束门

v5.0.8 的状态机、时间信封和校验器只有在**真实回复结束前被调用**时才构成有效控制。

必须区分两种认证：

- `COMPONENT_CERTIFIED`：状态机/校验器在显式调用时行为正确；
- `LIVE_E2E_ENFORCED`：真实 GPT/Codex 使用流程确实经过这些门并产生要求的控制交换。

组件测试通过不得自动推出真实端到端执行约束已经生效。

### 虚拟成熟后的强制结束门

一旦同时满足：

`VIRTUAL_MATURE=PASS`

`SOLUTION_FROZEN=YES`

`REAL_STARTED=NO`

则当前回复**不得以总结、状态说明或 Freeze 结论结束**。

必须继续完成：

`VIRTUAL_MATURITY_TIME_CLOSEOUT -> FREEZE_COMMIT -> FREEZE_TO_REAL -> REAL_DISPATCH`

并在同一回复中输出可直接交给目标执行器的 Reality Dispatch。

Reality Dispatch 至少必须显式包含：

1. `【页面名｜任务名｜序号｜实】`
2. `【时间锚｜整体已用=<数字>ms｜本次已用=<数字>ms｜T*=<数字>ms】`
3. `TIMELINE_ID`
4. `TIME_ORIGIN_UTC`
5. `DISPATCH_UTC`
6. `FREEZE_ID`
7. 冻结资产/路径/版本
8. Reality VALID 条件
9. Reality 计时边界
10. PASS / FAIL / BLOCKED 返回合同
11. `RETURN_TO_GPT=YES`

如果真实可审计的 `TIMELINE_ID / TIME_ORIGIN_UTC` 从未建立：

- 必须 BLOCK；
- 不得伪造整体已用时间；
- 先建立或恢复可审计 Timeline，再允许 REAL_DISPATCH。

### 控制权规则

Reality 执行器不得自行宣布整个任务 `FINAL_VALID/DONE`。

无论 PASS / FAIL / BLOCKED，现实执行结束后均必须：

`RETURN_TO_GPT=YES`

由 GPT 验证时间连续性、Reality 结果和最终收口。

### 机械回归门

权威实现：
- `contracts/FINAL-RESPONSE-ENFORCEMENT-v5.0.8.json`
- `runtime/final_response_gate_v5_0_8.py`
- `tests/test_final_response_gate_v5_0_8.py`

DSE v1.0.3 的真实失效回复已经作为回归反例：
- 有 REAL Locator，但没有数值时间信封；
- 没有 TIMELINE_ID / TIME_ORIGIN_UTC / DISPATCH_UTC；
- 成功路径写成 `RETURN_TO_GPT=NO`。

该反例必须被结束门拒绝。

> 注意：纯 Skill 文本和 Python 校验器本身不能证明宿主 ChatGPT/Codex 一定调用该 gate。最终 `LIVE_E2E_ENFORCED=YES` 只能由新的真实使用测试证明。

---

## 12. HISTORICAL：v5.0.8 最终权威证据

最终 Reality 报告：

`docs/first-principles/v5.0.8/FINAL-REALITY-REPORT-R4.json`

最终证书：

`docs/first-principles/v5.0.8/FINAL-VALID-CERTIFICATE.json`

最终 Reality Freeze：

`docs/first-principles/v5.0.8/FREEZE-MANIFEST-R4.json`

认证分支保持不可变：

`codex/first-principles-physical-limit-convergence-v5.0.8-r4-virtual-freeze`

以下规则与证据仅对 v5.0.8 历史认证成立，不代表 v5.1.1 当前已 FINAL/DONE。v5.0.8 历史发布规则以本节证据为准；更早 v5.0.2/v5.0.3/v5.0.5/v5.0.7/v5.0.8 R2/R3 文件保留为演化与 Reality Delta 证据，不得覆盖历史认证。v5.1.1 当前状态以 docs/first-principles/v5.1.1/CURRENT_STATE.json 为最高状态权威。
