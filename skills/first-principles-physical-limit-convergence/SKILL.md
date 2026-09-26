---
name: first-principles-physical-limit-convergence
description: 整体闭环极限短时间引擎 v5.0.8。保持原状态机；时间连续性在所有关键控制边界必须显式携带数值快照。
metadata:
  version: "5.0.8"
  display_name: "整体闭环极限短时间引擎"
---

# 整体闭环极限短时间引擎 v5.0.8


## v5.0.8 当前权威规则：控制边界显性时间连续性

v5.0.8 不改变原“虚→实”状态机，也不要求每个内部小动作刷时间。

新增硬门：
凡发生以下任一情况，都属于 CONTROL_BOUNDARY（控制边界）：
- 关键方案定案；
- 虚拟成熟收口；
- Freeze 提交；
- GPT -> Codex 派发；
- Codex -> GPT 返回；
- REAL FAIL / BLOCKED 回虚；
- FINAL_VALID。

每一个 CONTROL_BOUNDARY 必须显式携带同一 Timeline 的数值时间快照。
最小必须有：
`T_CLOSED_LOOP_ELAPSED_MS`
`T_BOUNDARY_SEGMENT_ELAPSED_MS`

若该边界已经存在冻结极限，还必须有：
`T_STAR_MS`

Reality 返回：
- PASS：必须有整体累计、本次尝试、冻结 T*、现实 T_VALID；
- FAIL/BLOCKED：也必须有整体累计、本次尝试、冻结 T*；
- 若证书根本未启动，可写证书计时 `0.000ms（未启动）`，但本次尝试耗时不能消失。

派发有时间、回报无时间，或回报有时间、派发无时间，均判：
`BOUNDARY_TIME_PROOF_MISSING -> ANCHOR_CONTINUITY_FAIL`。

详细合同：
- `contracts/CONTROL-BOUNDARY-TIME-v5.0.8.json`

## v5.0.8 Reality 可执行载荷物化规则

v5.0.7 Reality 暴露的 `UnicodeEncodeError` 已作为 Reality Delta 吸收。

人类可读文档可以继续使用中文；真正送入 Python 的冻结 Reality Capsule 必须为 ASCII-only 可执行源码。

进入 Reality 计时前必须依次机械通过：
`远程精确 blob 读取 -> blob 回读一致 -> source.isascii() -> compile -> fresh namespace exec -> run_reality_certificate callable`。

这些都属于 Reality 前置物化门，不计入证书 `T_VALID_REAL`。

只有前置物化 PASS 后：
- 紧接 `run_reality_certificate()` 前记录 `T_VALID_START`；
- 全部证书项 PASS 返回后立即记录 `T_VALID_END`。

若编码/物化失败：
- 不得修改当前 Freeze；
- 不得原地重试；
- 必须以 FAIL/BLOCKED 数值时间信封返回；
- Reality Delta -> STOP -> 回虚。

权威合同：
- `contracts/REALITY-PAYLOAD-MATERIALIZATION-v5.0.8.json`
- `tests/test_reality_materialization_v5_0_8.py`
- `docs/first-principles/v5.0.8/REAL-CAPSULE-SOURCE-R2.py`

## v5.0.7 当前权威规则：数值时间锚

v5.0.7 不改变 v5.0.5 已冻结的原状态机，不改变共同私库直读主路径。

关键控制节点的时间锚必须首先是有限数值：
- `T_CLOSED_LOOP_ELAPSED_MS`：整体闭环累计实际时间；
- `T_STAGE_ELAPSED_MS`：当前阶段累计实际时间；
- `T_STAGE_STAR_MS`：当前阶段冻结的极限有效时间。

状态词只能解释数值，不能代替数值。以下均非法：
`N/A / NA / NULL / MISSING / Infinity / NaN / 空值`。

REAL_DISPATCH 首屏必须至少显示：
`闭环已用=<数值>ms｜本段已用=<数值>ms｜T*=<数值>ms`。

如果任一必需数值缺失或不是有限数值：
`TIME_ANCHOR_VALUE_MISSING_OR_INVALID -> ANCHOR_CONTINUITY_FAIL -> BLOCK`。

详细权威合同：
- `contracts/NUMERIC-TIME-ANCHOR-v5.0.7.json`
- `runtime/state_machine_v5_0_7_overlay.py`
- `tests/test_state_machine_v5_0_7_overlay.py`
- `docs/first-principles/v5.0.7/VIRTUAL-FREEZE.md`

## v5.0.5 当前权威规则：原状态机不可被时间规范改写

v5.0.5 继承并锁死 v4.7.x → v5.0.3 已形成的状态机动作：
`虚 -> 完整虚拟成熟 -> Freeze -> FREEZE_TO_REAL -> 实`；
`REAL_PASS -> DONE`；
`REAL_FAIL -> Reality Delta -> STOP -> 回虚 -> 新 Freeze -> 再实`。

时间总控只是状态机内部 guard（守卫）：
- 可以阻断缺失时间锚、非法 N/A/NULL/MISSING、未完成时间收口等非法状态；
- 不得改变状态顺序、执行器角色、Freeze 消耗规则、01-06 规则或 Reality FAIL 回虚动作；
- 不得新增第三阶段。

### 正常权威源路径固定为共同私库直读

当共同私库网络、权限、仓库均正常：
`REMOTE_SHARED_REPO_DIRECT` 是唯一正常路径。

禁止把以下动作重新插入正常闭环：
- 让用户下载冻结包；
- 让用户重新确认下载位置；
- 为 Reality 无目的扫描本地磁盘；
- 先下载再交给 Codex。

Reality 直接按冻结的 `REPOSITORY / BRANCH / PATH / BLOB` 读取。

只有 `NETWORK_UNAVAILABLE / AUTH_UNAVAILABLE / REPOSITORY_UNAVAILABLE` 才允许：
`STOP -> REMOTE_REPO_UNAVAILABLE -> Reality Delta -> RETURN_TO_GPT`。

备用下载/本地/内联只能回到“虚”后形成新的显式 Freeze；禁止在当前 REAL 中现场切换。

### 时间总控继续生效

`T*=min(T_VALID)` 永远在线，顶层 `T_VALID=T_CLOSED_LOOP_VALID`。
任何进入闭环的时间段都必须有时间锚；`N/A / NULL / MISSING` 为非法。
时间从 `PENDING/SOLVING` 连续演化到 `VIRTUAL_FROZEN/REAL_CERTIFIED`。
虚拟成熟必须先完成时间收口。

详细权威合同：
- `contracts/STATE-MACHINE-v5.0.5.json`
- `contracts/TIME-MASTER-CONTROL-v5.0.5.json`
- `runtime/state_machine_v5_0_5_overlay.py`
- `tests/test_state_machine_v5_0_5_overlay.py`
- `docs/first-principles/v5.0.5/VIRTUAL-FREEZE.md`

## 唯一目标
所有有效门通过后，只优化：`T* = min(T_VALID)`。

## 顶层方法永久只有两步
### 虚
设计、物化实现、GPT 独立执行验证、故障注入、验证器攻击、时间竞争、Freeze、Reality Capsule 全部属于“虚”。

### 实
只执行冻结 Reality Capsule，记录真实开始/结束/T_VALID_REAL 并运行冻结 verifier。
失败只能：`Reality Delta -> STOP -> 回虚 -> 新 Freeze`。

不增加第三阶段，不新增顶层 Implementation Closure Gate。

## v5.0.2 核心修正
`设计存在 != 实现存在`。
`VIRTUAL_COMPLETE=YES` 必须同时成立：`SPEC_COMPLETE AND IMPLEMENTATION_COMPLETE AND GPT_VERIFICATION_PASS AND FREEZE_COMPLETE`。

`EXECUTION_CHAIN_CLOSED=PASS` 不再接受自由布尔声明；必须由实现证据机械推出：行为已实现、位置可定位、异常分类已实现、retry/recovery/fallback 已实现、路径可执行、失败分支已故障注入、verifier 可区分错误实现、Reality Capsule 包含真实实现；并且 implementation-map / fault-injection / verifier 三类不可变证据哈希非空。

## 唯一转换
`虚 --完整成熟+冻结证据PASS--> 实`
`实 --PASS--> DONE`
`实 --FAIL+Reality Delta--> 虚`

Codex 只做目标环境认证，不负责发现“函数没写”。

## 执行适配器
- CODEX -> CHAT
- PLAYWRIGHT -> NATIVE_BROWSER
- REASONIX -> UI_AGENT
- LOCAL_FROZEN -> FROZEN_RUNNER

CODEX 的 EXEC / PowerShell / Shell 发送方式直接阻断。

## 权威实现
- `contracts/STATE-MACHINE-v5.0.2.json`
- `runtime/state_machine_v5_0_2.py`
- `tests/test_state_machine_v5_0_2.py`
- `docs/first-principles/v5.0.2/REAL-CAPSULE-SOURCE.py`

v5.0.0 保留为演化证据，不作为 v5.0.2 运行时权威。


## 冻结源解析规则
冻结资产的“可执行”不等于必须预先复制进目标工作目录。

允许的首选权威源包括共同私有 GitHub 仓库。进入“实”前，派发合同必须明确冻结：
- `REPOSITORY_URL / REPOSITORY_FULL_NAME`
- `BRANCH`（或更强的不可变 commit/blob）
- 完整 `PATH`
- 期望 `BLOB_SHA`；必要时再加内容 `SHA-256`

现实执行器必须先按冻结远程定位读取权威源。只要网络、登录权限和仓库访问正常，就直接读取，不要求先在当前工作区或 C 盘存在副本，也不得无目的扫描本地磁盘。

只有远程源因 `NETWORK_UNAVAILABLE / AUTH_UNAVAILABLE / REPOSITORY_UNAVAILABLE` 确实不可达时，才允许：
`STOP -> REMOTE_REPO_UNAVAILABLE -> Reality Delta -> 回虚`

本地/内联副本只是“虚”阶段可以预先冻结的兜底方案，不是远程仓库正常可用时的默认前置条件。


## 冻结一致性与执行物化
同一 Reality 尝试只能有一个完整权威 Freeze。冻结后若任何被引用资产发生变化，旧 Manifest 自动失去当前尝试的权威资格；不得用新的 handoff 清单叠加引用一个已经含旧 blob 的基清单，必须重新生成完整 Freeze。

`EXECUTION_CHAIN_CLOSED=PASS` 还必须机械证明：
- `FREEZE_MANIFEST_CONSISTENT=PASS`：完整 Manifest 中每个当前冻结资产的 blob 与发布后回读完全一致；
- `PAYLOAD_MATERIALIZATION_VERIFIED=PASS`：GPT 已按未来 Reality 的同一路径验证“远程全文读取 → 同一 Python namespace 执行 → run_verifier 存在且可调用”。

只核对远程文件元数据、只拿到文件名/blob、或在未执行源码的空 namespace 中寻找 `run_verifier`，均不得声明虚拟成熟。


## 虚全量证明与实最小证书
同一不可变 Reality Capsule 的正确性证明分工固定为：
- 虚阶段：对确切冻结 blob 做完整状态空间/故障路径验证，形成全量 verifier 证据；
- 实阶段：先严格核对完整 Freeze、blob、SHA-256 和全量证明收据；只有这些全部一致，才允许运行最小目标环境兼容性证书。

Reality 不需要重复执行已经由“确切同一 blob + 不可变哈希”绑定的全部穷举用例。Reality Certificate 只验证目标解释器/运行环境中：正向转换、关键单故障阻断、证据哈希阻断、适配器策略、REAL PASS/FAIL、定位渲染和源码物化仍成立。

这不改变 VALID 定义；如果 blob、Manifest 或全量证明证据任一不一致，最小证书没有资格运行。

Reality 的 `T_VALID_REAL` 应测最小目标环境证书本身；全量穷举时间属于虚拟成熟的一次性证明成本，不重复计入每次 Reality 认证。


## 时间锚定硬合同（v5.0.3）
`T*=min(T_VALID)` 不是说明文字，而是每个任务的唯一控制锚。

虚阶段可以在尚未成熟时显示 `T*=PENDING`；但一旦声明 `VIRTUAL_COMPLETE=YES`，必须已经冻结：
- `T_STAR_MS`
- `T_VALID_START`
- `T_VALID_END`
- `T_STAR_SOURCE`

缺任意一项，禁止 `虚 -> 实`。

所有 Reality/Codex 派发第一屏必须由状态机机械渲染时间锚，不允许模型自由省略。固定最小格式：

`【页面名｜任务名｜NN-NN｜实】 极限锚MM:SS.mmm｜T*=X.XXXXXXms`

紧随其后必须出现：

`T_STAR_MS=...`
`T_VALID_START=...`
`T_VALID_END=...`
`T_STAR_SOURCE=...`

REAL PASS 只能使用该冻结状态中的同一个 `T_STAR_MS` 判断：
`T_VALID_REAL_MS <= T_STAR_MS`。

REAL FAIL 返回虚后，活动时间锚必须清空；下一次 Reality 必须重新虚拟成熟并生成新的 T*，禁止沿用旧任务/旧尝试的时间锚。


## 连续时间状态（v5.0.3）
时间不是每个命令包临时贴上的标签，而是整个任务从进入引擎到最终有效完成的一条连续状态链。

每个任务首次进入时建立且以后不可更换：
- `TIMELINE_ID`
- `TIME_ORIGIN_UTC`

以后所有虚/实转换只允许向同一账本追加：
- `TIME_EVENT_SEQ`
- `TIME_EVENTS[]`

典型连续链：
`TASK_ORIGIN -> FREEZE_TO_REAL -> REAL_START -> REAL_FAIL -> 新Freeze -> REAL_START -> REAL_PASS`

REAL FAIL 返回虚时：
- 不得新建时间轴；
- 不得删除旧 T* / T_VALID / 失败事件；
- 不得重置 `TIMELINE_ID / TIME_ORIGIN_UTC`；
- 只把“当前活动 T*”变为 `PENDING`，防止旧 Freeze 的 T* 被下一次 Reality 偷用。

新的虚拟成熟完成后，在同一时间轴追加新的 Freeze 事件并生成新的活动 T*。

REAL PASS 后：
- 把真实 `T_VALID_REAL_MS` 追加到同一账本；
- `T_STAR_STATUS=REAL_CERTIFIED`；
- `BEST_CERTIFIED_T_VALID_MS=min(历史已认证值, 本次T_VALID_REAL_MS)`。

`BEST_CERTIFIED_T_VALID_MS`、事件序列和过程时间记录只是同一唯一目标 `T*=min(T_VALID)` 的状态证据，不构成第二优化目标。

所有 Reality 派发都必须显示同一时间轴的当前快照：
`TIMELINE_ID / TIME_ORIGIN_UTC / TIME_EVENT_SEQ / T_STAR_STATUS / T_STAR_MS / T_VALID_START / T_VALID_END / T_STAR_SOURCE / BEST_CERTIFIED_T_VALID_MS`。


## 唯一锚定物的强制生效规则（v5.0.3）
为什么只有一个锚定物：

1. 正确性、安全、质量、成本、依赖等只决定结果是否进入 `VALID` 集合；
2. 进入 `VALID` 后，所有候选只允许按 `T_VALID` 比较；
3. 因此系统唯一排名目标固定为 `T*=min(T_VALID)`；
4. `T_RESOLVE / T_TRANSFER / T_VERIFY` 等只是同一 `T_VALID` 的时间分解，用来定位瓶颈，不是并列目标；
5. 若允许第二个独立评分轴，就无法再机械判定“整体闭环极限短时间”，因此违反本引擎定义。

从 v5.0.3 起，`T*=min(T_VALID)` 必须存在于**每一个 EngineState**，不是可选说明文字。

状态演化固定为：
- 任务刚进入：`UNIQUE_ANCHOR=T*=min(T_VALID)`，`ANCHOR_STATE=PENDING`；
- 虚拟成熟冻结：同一时间轴变为 `ANCHOR_STATE=VIRTUAL_FROZEN`，出现数值 `ACTIVE_T_STAR_MS`；
- Reality FAIL：同一 `TIMELINE_ID` 继续，历史事件不删，活动 T* 回到 `PENDING`；
- 新 Freeze：在同一时间轴追加新的活动 T*；
- Reality PASS：追加真实 `T_VALID_REAL_MS`，状态变为 `REAL_CERTIFIED`，并更新 `BEST_CERTIFIED_T_VALID_MS=min(历史,本次)`。

任何“要执行的步骤”在执行前必须经过唯一时间控制门，并显示：

`ACTION`
`UNIQUE_ANCHOR=T*=min(T_VALID)`
`TIMELINE_ID`
`TIME_ORIGIN_UTC`
`TIME_EVENT_SEQ`
`ANCHOR_STATE`
`ACTIVE_T_STAR_MS`
`BEST_CERTIFIED_T_VALID_MS`
`T_VALID_START`
`T_VALID_END`
`T_STAR_SOURCE`

即使尚未得到数值 T*，也必须明确显示 `PENDING`，不能把锚定物省略。

以后所有 Locator 首行也必须直接显示：
`锚定物=T*=min(T_VALID)｜状态=...｜当前T*=...｜现实最优=...`

没有这份连续时间状态快照的动作，没有执行资格。
