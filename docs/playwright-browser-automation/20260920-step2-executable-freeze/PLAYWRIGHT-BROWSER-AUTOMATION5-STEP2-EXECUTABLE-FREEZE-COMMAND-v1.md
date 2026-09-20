【playwright浏览器自动化5｜STEP2可执行冻结补全｜1】

# Playwright 浏览器自动化5 — STEP 2 可执行冻结补全命令 v1

CURRENT_STEP=2
STEP_NAME=VIRTUAL_99
METHOD_VERSION=3.1.4
TASK_ID=PLAYWRIGHT-BROWSER-AUTOMATION5-STEP2-EXECUTABLE-FREEZE-v1
ONLY_OBJECTIVE=T_VALID
OBJECTIVE=T_STAR=min(T_VALID)

## 0. 方法定位

这不是第 4 步，不是新核心，不是新的解决路线。

本任务严格属于：

STEP 2 = VIRTUAL_99
CORE_3 = 高智能虚拟成熟

触发原因：

上一轮 STEP 2 已经完成：
- 路线设计；
- T_PHY 边界；
- finalist 选择；
- STEP 3 验证合同；
- STEP 3 命令。

但当前回传没有充分证明：

F1 / F2 / F3 已经全部成为
“可直接现实执行、无需 STEP 3 临场设计或临场实现”的冻结实现。

因此上一轮状态重新解释为：

VIRTUAL_DESIGN_FREEZE=PASS
EXECUTABLE_FREEZE=UNPROVEN
VIRTUAL_99_CLOSEOUT=INCOMPLETE

本轮只补齐 STEP 2 的“可执行冻结”。

在本轮完成前：

NEXT_ALLOWED_STEP=2_VIRTUAL_99
STEP3_AUTHORIZATION=REVOKED_TEMPORARILY

禁止运行 STEP 3。

## 1. 方法权威

读取并服从：

仓库=cuiqinggang/codex-private-skills
分支=codex/first-principles-physical-limit-convergence-v3.1.4
文件=skills/first-principles-physical-limit-convergence/SKILL.md
VERSION=3.1.4

若冲突：

SKILL_GATE=BLOCKED
ACTION=STOP

## 2. 已冻结输入，不得重新设计

保留上一轮已经冻结的：

TASK_FAMILIES=
A_DETERMINISTIC
B_FINITE_CLOSED_SEMANTIC
C_REPEATED_SOLVED_WORKFLOW
D_OPEN_COMPLEX_REASONING
E_RECOVERY_CHANGED_REALITY

FINALISTS=
F1_PLAYWRIGHT_NATIVE_DIRECT_PERSISTENT
F2_PLAYWRIGHT_COMPILED_REPLAY
F3_PERSISTENT_CDP_BATCHED_HELPER

辅助能力：
ONE_JEV_TYPED_DECISION
ONE_OPEN_AGENT_PLAN
ON_DEMAND_RECOVERY

已淘汰：
SEQUENTIAL_MULTI_PROCESS_CLI
ALWAYS_ON_JEV_ENSEMBLE
ALWAYS_ON_GPT_ROUTER
ALWAYS_ON_VERIFIER_OR_FALLBACK
AGENT_BROWSER_PRESENT_ONLY
BROWSERGYM_WEBARENA_PRODUCTION_RUNTIME
STAGEHAND_OBSERVE_EVERY_REPEAT
UNVERIFIED_9222_PRODUCTION_BACKBONE

不得新增 F4/F5。
不得改变 F1/F2/F3 的角色。
不得重新做成熟方案搜索。
不得重新跑 STEP 1。

## 3. Codex 的角色

Codex 本轮不是方案设计者。

Codex 只做：

IMPLEMENT
PACKAGE
STATIC_VERIFY
SIMULATE
FREEZE

Codex 不得自行：
- 新增路线；
- 更换浏览器；
- 更换模型；
- 增加 fallback；
- 增加 verifier 层；
- 改 winner rule；
- 依据个人判断重新设计架构。

如果冻结设计无法实现：

EXECUTABLE_FREEZE=BLOCKED
REALITY_OR_DESIGN_DELTA=<exact issue>
ACTION=STOP

不得自行解决成另一套方案。

## 4. 工作区与隔离

使用上一轮 STEP 2 本地工作区：

C:\Users\A\playwright-browser-automation5-step2-work

确认本地冻结提交：

23d08619757d6e1c33784b925c804bd5162e63d5

禁止修改：
C:\AI\Playwright-Native-AI-Browser 的生产状态；
用户共享 Profile；
FlClash；
代理；
Windows 网络；
现有登录态；
v3.1.4 母技能。

允许在 STEP 2 工作区新建隔离候选实现和测试文件。

REAL_BROWSER_RUNS=0
REAL_SITE_RUNS=0
REAL_JEV_REQUESTS=0
REAL_OPEN_AGENT_REQUESTS=0

## 5. 统一候选执行接口

F1/F2/F3 必须暴露同一冻结执行合同。

逻辑接口至少包含：

route_id
task_family
task_spec
run_condition = COLD | WARM | RECONNECT
profile_mode = ISOLATED | FORMAL_SHARED_PROFILE
timing_boundary
artifact_dir
result_path

统一结果必须至少包含：

route_id
task_id
valid
status
t_valid_ms
component_times
model_calls
browser_protocol_calls_if_observable
recovery_triggered
error
artifacts
contract_version

STEP 3 不允许因为不同路线接口不同而临时写 glue code。

本轮必须把 glue/adapters 预先做完。

## 6. F1 冻结实现

F1 = PLAYWRIGHT_NATIVE_DIRECT_PERSISTENT

要求：

1. 复用现役 Playwright Native 已有成熟模块，不重写浏览器；
2. 建立隔离 adapter/runner；
3. 直接 persistent Playwright 路径；
4. 已知 deterministic 动作禁止模型调用；
5. 使用已有 locator / event wait / context / session 能力；
6. 不增加 always-on agent；
7. 不增加 always-on second verifier；
8. 失败只返回冻结错误，不在 runtime 临场重新设计。

必须生成：

candidate-f1/
  manifest.json
  runner.<existing_project_language>
  adapter.<existing_project_language>
  CONTRACT.md

如果现有项目语言/结构不同，允许复用其原语言，但上述逻辑产物必须等价存在。

STEP 2 只做静态/模拟验证，不启动真实浏览器。

## 7. F2 冻结实现

F2 = PLAYWRIGHT_COMPILED_REPLAY

定义：

已成功、结构已知、参数变化有限的任务，
先由冻结 compiler 把成功轨迹/语义动作编译成 deterministic workflow，
正式运行只注入参数并执行。

运行时目标：

MODEL_CALLS=0
JEV_CALLS=0
OPEN_AGENT_CALLS=0

必须具备：

1. frozen workflow schema；
2. parameter schema；
3. precondition；
4. deterministic action sequence；
5. event/state waits；
6. verifier；
7. drift detector；
8. ROUTE_NOT_APPLICABLE 明确出口。

当 precondition 不满足时：

F2 必须直接返回：
ROUTE_NOT_APPLICABLE

禁止：
- 临时调用 GPT；
- 临时调用 Jev；
- 临时重新 observe 整页并生成新 workflow；
- 临时 fallback 到另一 route。

候选之间的 fallback/比较由 STEP 3 冻结 harness 控制，不由 F2 自己决定。

必须生成：

candidate-f2/
  manifest.json
  workflow-schema.json
  parameter-schema.json
  compiler.<project_language>
  runner.<project_language>
  verifier.<project_language>
  CONTRACT.md
  at least one frozen fixture workflow

本轮 compiler 只能对已有 STEP 1/历史成功证据做离线编译，
不得访问真实站点。

## 8. F3 冻结实现

F3 = PERSISTENT_CDP_BATCHED_HELPER

目的：

验证成熟 persistent browser/CDP + batched helper 是否能在同 VALID 下减少协议往返和 T_VALID。

注意：

STEP 1 的：
CDP_9222_ENDPOINT_404

已经证明固定 9222 不能作为生产前提。

因此 F3 冻结为：

ISOLATED_SELF_OWNED_PERSISTENT_SESSION
NO_FIXED_9222_DEPENDENCY

要求：

1. 候选自己拥有隔离 browser/session 生命周期；
2. 不接管用户现有共享 Profile；
3. endpoint/transport 在候选启动时确定，不硬编码 9222；
4. batched helper 把可合并的 state-read / locate / action / extract 往返合并；
5. 已知 deterministic 任务禁止模型调用；
6. 不为了减少调用数删除 VALID 必要等待或验证；
7. 不建立第二套永久生产浏览器，当前只是 finalist candidate；
8. STEP 3 验证通过后才有资格竞争最终系统。

必须生成：

candidate-f3/
  manifest.json
  session-owner.<project_language>
  batched-helper.<project_language>
  runner.<project_language>
  verifier.<project_language>
  CONTRACT.md

本轮不启动浏览器，只通过 mock transport / fake CDP adapter 完成虚拟验证。

## 9. B 类 one-Jev 路径冻结

Jev 不是 F4。

它是 FAMILY_B 的一个冻结能力：

CODE pre-handler
-> compact finite state
-> at most ONE canonical typed Jev request
-> candidate action
-> CODE final verifier

必须程序化冻结：

- input schema；
- finite candidate schema；
- typed request builder；
- response parser；
- invalid/uncertain contract；
- zero-retry rule；
- one-request maximum；
- no ensemble；
- no probability fusion；
- no hidden second Jev call。

本轮使用 mock Jev response 做虚拟测试。

REAL_JEV_REQUESTS=0

## 10. D 类 open-agent 路径冻结

Open agent 不是默认路线。

只用于：

OPEN_PROBLEM
or
ONE_JEV_INVALID_OR_UNCERTAIN

冻结接口：

one planning call
-> structured plan
-> deterministic execution steps
-> CODE verifier

不得：

- 每一步重新调用 agent；
- 每一步重新规划；
- 用 agent 选择 browser route；
- 将恢复机制变成 always-on。

本轮用 mock plan 做虚拟测试。

REAL_OPEN_AGENT_REQUESTS=0

## 11. E 类恢复路径冻结

恢复只在现实失败信号出现后触发。

冻结 trigger：

SESSION_LOST
STALE_STATE
TARGET_CHANGED
BROWSER_CRASH
NETWORK_INTERRUPTION
CONTRACT_DRIFT

正常路径：

RECOVERY_OVERHEAD=0

恢复不得成为每次运行的前置步骤。

本轮通过故障注入 simulation 验证。

## 12. STEP 3 Harness 必须现在实现

STEP 3 不能临场写测试程序。

本轮必须提前实现并冻结：

step3-harness/
  task-schema.json
  route-interface-schema.json
  result-schema.json
  timing-boundary.json
  run-matrix.json
  verifier.<project_language>
  statistics.<project_language>
  winner-selector.<project_language>
  harness.<project_language>
  CONTRACT.md

winner-selector 固定：

1. VALID first
2. then minimum T_VALID
3. exact tie -> tie
4. no second KPI

失败样本不得删除。

statistics 可以计算：
minimum
median
maximum
P95（样本数足够时仅诊断）

但 winner 只能使用冻结规则。

## 13. 最终系统 Router 预实现

STEP 3 结束后不得临场设计最终 router。

因此本轮先实现一个 data-driven minimal router：

final-router/
  router.<project_language>
  winner-map.schema.json
  CONTRACT.md

router code 现在冻结。

STEP 3 只允许由 winner-selector 产生：

winner-map.json

router 读取 winner-map.json。

这不属于 STEP 3 架构修改；
只是把现实 winner 数据写入 STEP 2 已冻结的数据接口。

router 本身禁止模型调用。

## 14. 虚拟程序化测试

本轮必须真正运行“虚拟/模拟程序”，不是只写文档。

禁止真实浏览器、真实站点、真实 Jev、真实 open-agent。

至少覆盖：

- F1 applicable / invalid task；
- F2 applicable / parameter error / precondition fail / drift；
- F3 session available / transport fail / stale mock state；
- one-Jev valid / invalid / uncertain / illegal response；
- open-agent valid plan / invalid plan；
- recovery each frozen trigger；
- router explicit route mode；
- winner-selector all-valid / one-fail / tie / known-faster-reference conflict；
- timing boundary start/stop invariants；
- failure records retained；
- no second KPI；
- no hidden model call；
- no hidden browser call。

建立 deterministic virtual case matrix。

每个有限状态组合全部覆盖；
对存在组合爆炸的输入使用固定 seed property tests。

最低要求：

VIRTUAL_CONTRACT_TESTS=PASS
VIRTUAL_FAILURE_TESTS=PASS
VIRTUAL_ROUTE_INTERFACE_TESTS=PASS
VIRTUAL_WINNER_RULE_TESTS=PASS
VIRTUAL_NO_REAL_IO_ASSERTION=PASS

## 15. “程序化成熟”判据

只有同时证明：

F1_EXECUTABLE_PACKAGE=PASS
F2_EXECUTABLE_PACKAGE=PASS
F3_EXECUTABLE_PACKAGE=PASS
JEV_TYPED_PATH_PACKAGE=PASS
OPEN_AGENT_PATH_PACKAGE=PASS
RECOVERY_PACKAGE=PASS
STEP3_HARNESS_EXECUTABLE=PASS
FINAL_ROUTER_CODE_FROZEN=PASS
ALL_ROUTE_INTERFACES_UNIFIED=PASS
VIRTUAL_CONTRACT_TESTS=PASS
VIRTUAL_FAILURE_TESTS=PASS
VIRTUAL_WINNER_RULE_TESTS=PASS
NO_REAL_BROWSER_IO=PASS
NO_REAL_MODEL_IO=PASS
PRODUCTION_MUTATION=0

才允许：

EXECUTABLE_FREEZE=PASS
VIRTUAL_99=PASS
NEXT_ALLOWED_STEP=3_REAL_VERIFY

否则：

EXECUTABLE_FREEZE=BLOCKED
VIRTUAL_99=INCOMPLETE
NEXT_ALLOWED_STEP=2_VIRTUAL_99
ACTION=STOP

## 16. STEP 3 命令处理

上一轮 STEP 3 command 不得直接使用。

本轮完成后：

- 若可执行冻结 PASS：
  生成新的 STEP 3 command v2；
  只引用本轮冻结 candidate packages + harness + contract；
  不允许 STEP 3 自行实现任何缺失部件。

- 若可执行冻结 FAIL：
  不生成可执行 STEP 3 命令。

## 17. 输出文件

至少生成：

docs/playwright-browser-automation/20260920-step2-executable-freeze/
  PLAYWRIGHT-BROWSER-AUTOMATION5-STEP2-EXECUTABLE-FREEZE-RESULT-v1.md
  PLAYWRIGHT-BROWSER-AUTOMATION5-STEP2-EXECUTABLE-FREEZE-RESULT-v1.json
  PLAYWRIGHT-BROWSER-AUTOMATION5-STEP2-VIRTUAL-TEST-MATRIX-v1.json
  PLAYWRIGHT-BROWSER-AUTOMATION5-STEP2-FROZEN-IMPLEMENTATION-MANIFEST-v1.json
  PLAYWRIGHT-BROWSER-AUTOMATION5-STEP3-REAL-VERIFY-COMMAND-v2.md

并保留所有候选实现、schema、mock、测试与 harness。

全部：
写后回读
JSON parse
git diff --check
SHA256
本地 commit

不得 push，除非明确授权。

## 18. 最终回传

只回传：

METHOD_AUTHORITY=
CURRENT_STEP=
PRIOR_VIRTUAL_DESIGN_FREEZE=
EXECUTABLE_FREEZE_GAP=
F1_EXECUTABLE_PACKAGE=
F2_EXECUTABLE_PACKAGE=
F3_EXECUTABLE_PACKAGE=
JEV_TYPED_PATH_PACKAGE=
OPEN_AGENT_PATH_PACKAGE=
RECOVERY_PACKAGE=
STEP3_HARNESS_EXECUTABLE=
FINAL_ROUTER_CODE_FROZEN=
ALL_ROUTE_INTERFACES_UNIFIED=
VIRTUAL_CONTRACT_TESTS=
VIRTUAL_FAILURE_TESTS=
VIRTUAL_WINNER_RULE_TESTS=
REAL_BROWSER_RUNS=
REAL_JEV_REQUESTS=
REAL_OPEN_AGENT_REQUESTS=
PRODUCTION_MUTATION=
EXECUTABLE_FREEZE=
VIRTUAL_99=
NEXT_ALLOWED_STEP=
STEP3_COMMAND_V2=
ACTION=
EVIDENCE_FILES=
LOCAL_COMMIT=
SHA256=

如果并且仅如果：
EXECUTABLE_FREEZE=PASS
且 VIRTUAL_99=PASS

才允许同一回复给出 STEP 3 v2 最短 handoff。

最后一行必须原样返回：

【playwright浏览器自动化5｜STEP2可执行冻结补全｜1】
