---
name: first-principles-physical-limit-convergence
description: 整体闭环极限短时间引擎 v5.0.2。方法仍只有“虚→实”；v5.0.2 收紧虚拟成熟证据语义，禁止把“设计成熟”冒充“实现已成熟”。唯一目标 min(T_VALID)。
metadata:
  version: "5.0.2"
  display_name: "整体闭环极限短时间引擎"
---

# 整体闭环极限短时间引擎 v5.0.2

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
