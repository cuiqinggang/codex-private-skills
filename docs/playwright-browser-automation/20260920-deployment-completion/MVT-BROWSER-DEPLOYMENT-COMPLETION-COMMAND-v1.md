【playwright浏览器自动化5｜物化浏览器现实竞争总装｜1｜高智能虚拟成熟】

# MVT Browser Deployment Completion — 冻结执行命令 v1

## 0. 任务性质

这不是修复任务。

这不是新的方案设计。

这条命令只是把 GPT 已经冻结的部署完整性方案物化到本机冻结候选上。

方法权威：

first-principles-physical-limit-convergence v3.1.5

核心归属：

高智能虚拟成熟

执行器角色固定为：

读取
-> 物化
-> 静态验证
-> 模拟
-> 回传
-> STOP

禁止自行修复、重新设计、增加路线或修改冻结规则。

---

## 1. 远端唯一来源

仓库：

cuiqinggang/codex-private-skills

分支：

codex/mvt-browser-deployment-completion-v1

先读取：

skills/mvt-browser-deployment-completion/SKILL.md
skills/mvt-browser-deployment-completion/VERSION
skills/mvt-browser-deployment-completion/manifest.json
skills/mvt-browser-deployment-completion/ACCEPTANCE.md
skills/mvt-browser-deployment-completion/references/D001-D007-REALITY-DELTA.md
skills/mvt-browser-deployment-completion/references/DEPLOYMENT-ASSEMBLY-CONTRACT-v1.json
skills/mvt-browser-deployment-completion/tests/DEPLOYMENT-ASSEMBLY-VIRTUAL-99-v1.json

必须确认：

VERSION=1.0.0-rc1
METHOD_AUTHORITY=first-principles-physical-limit-convergence@3.1.5
CORE=高智能虚拟成熟
VIRTUAL_99=PASS
TOTAL_VIRTUAL_CASES=46/46

任一不满足：

SOURCE_GATE=BLOCKED
ACTION=STOP

不得自行调整远端内容。

---

## 2. 本地冻结来源

候选冻结工作区：

C:\Users\A\playwright-browser-automation5-step2-work

必须：

git rev-parse HEAD
= 6a8c3b0dfb98bfd3312df319dbd31b0ffd7ed629

git status --porcelain
= 空

并确认之前冻结证据仍存在：

22/22 tests PASS
26/26 simulations PASS
58/58 manifest hashes PASS

不满足：

FROZEN_SOURCE_GATE=BLOCKED
ACTION=STOP

不得在原冻结工作区直接改文件。

---

## 3. 隔离总装工作区

建立独立工作区：

C:\Users\A\playwright-browser-automation5-deployment-complete-v1

来源必须固定到：

6a8c3b0dfb98bfd3312df319dbd31b0ffd7ed629

不得修改：

C:\AI\Playwright-Native-AI-Browser
共享浏览器 Profile
代理
FlClash
Windows 网络
原 step2 frozen workspace

本轮：

REAL_BROWSER_RUNS=0
REAL_JEV_REQUESTS=0
REAL_OPEN_AGENT_REQUESTS=0

---

## 4. 七个总装门必须全部物化

依据：

skills/mvt-browser-deployment-completion/references/DEPLOYMENT-ASSEMBLY-CONTRACT-v1.json

在隔离工作区建立：

deployment-complete-v1\

并生成：

1. real-run-config.json
2. route-bindings.json
3. condition-state-machines.json
4. t-valid-full-record-contract.json
5. result-pipeline.json
6. capability-execution-matrix.json
7. recovery-execution-bindings.json
8. deployment-manifest.json
9. virtual-assembly-test-result.json
10. FINAL-REALITY-COMPETITION-COMMAND-v2.md

### 4.1 D001 — real-run-config

必须锁定：

- source commit
- candidate roots
- harness root
- final-router root
- A/B/C/D/E/CAP frozen matrix
- COLD/WARM/RECONNECT
- repeat counts
- T_VALID_FULL contract
- result output root
- no-mutation policy

禁止留下“运行时再决定”的字段。

### 4.2 D002 — route-bindings

必须只使用冻结目录：

candidate-f1
candidate-f2
candidate-f3
step3-harness
final-router

以及冻结的 Jev/open-agent/recovery package。

解析规则：

- runner / adapter / compiler / verifier / session-owner / batched-helper / harness / statistics / winner-selector 等文件只允许合同规定扩展名；
- 每个必需角色必须 exactly one match；
- 0 match = BLOCK；
- >1 match = BLOCK；
- 禁止根据“看起来像”选择。

必须产生所有 required task-family/case/condition/route 的 exact binding。

最终：

AMBIGUOUS_BINDINGS=0
UNBOUND_REQUIRED_CASES=0

### 4.3 D003 — condition-state-machines

必须逐字实现合同中的：

COLD
WARM
RECONNECT

事件顺序。

禁止：

- 把 warm precondition 放进计时后再说是 warm；
- 把 browser 已启动的情况记为 cold；
- reconnect 时重启 browser 冒充 reconnect。

模拟检查所有状态转移。

### 4.4 D004 — T_VALID_FULL recorder

所有 route 共用同一 recorder contract。

必须：

MONOTONIC_HIGH_RESOLUTION
t_valid_full_ms = end_monotonic_ms - start_monotonic_ms

字段必须完整。

禁止 route 自己定义 timer。

TIMING_BOUNDARY_OVERRIDES=0

### 4.5 D005 — result pipeline

唯一顺序：

RUNNER_RESULT
-> INDEPENDENT_VERIFIER
-> NORMALIZED_ATTEMPT
-> APPEND_ONLY_JSONL
-> STATISTICS
-> PROVISIONAL_WINNER_SELECTOR
-> ARTIFACT_HASHES

所有失败 attempt 保留。

DROPPED_FAILURE_ATTEMPTS=0

Winner rule：

VALID first
-> minimum T_VALID_FULL
-> exact tie remains tie
-> no second KPI

### 4.6 D006 — capability matrix

唯一事实来源优先使用：

C:\Users\A\playwright-browser-automation5-step1-sparse\docs\playwright-browser-automation\20260920-step1-mature-reality\PLAYWRIGHT-BROWSER-AUTOMATION5-STEP1-CAPABILITY-MATRIX-v1.json

必须 JSON parse PASS。

对每个 frozen capability 生成：

case_id
capability
status
route_binding
fixture_or_request
expected
verifier
repeat_count

若某能力不能完整绑定：

该能力只能 UNKNOWN
OVERALL_CAPABILITY_COMPLETE=NO

不得现场新增实现。

### 4.7 D007 — recovery bindings

必须绑定全部：

SESSION_LOST
STALE_STATE
TARGET_CHANGED
BROWSER_CRASH
NETWORK_INTERRUPTION
CONTRACT_DRIFT

每项：

fault_injector
recovery_runner
verifier
repeat_count=3
result_record

正常路径：

RECOVERY_OVERHEAD=0

---

## 5. Harness 与现有冻结实现的绑定规则

不得重写现有 F1/F2/F3。

不得重写 step3-harness。

只允许生成配置/绑定/adapter mapping。

如果现有 harness 或 route package 已有 machine-readable invocation/entrypoint：
直接引用。

如果只在其冻结 CONTRACT.md 中存在唯一 canonical entrypoint：
原样解析并绑定。

如果：

- machine-readable entrypoint 不存在；
- CONTRACT 中也没有唯一 canonical entrypoint；
- 两者冲突；
- 同一角色解析出两个候选；

则：

ENTRYPOINT_BINDING=BLOCKED
REALITY_DELTA=<exact path/role>
ACTION=STOP

不得自己发明新调用约定。

---

## 6. 本轮 Virtual-99

禁止真实 browser/model/network task。

至少运行：

### 正向

- 七门全部存在；
- F1/F2/F3 每个 required binding 唯一；
- harness required files 唯一；
- COLD 状态顺序；
- WARM 状态顺序；
- RECONNECT 状态顺序；
- T_VALID 公式；
- append-only pipeline；
- winner rule；
- capability bindings；
- 6 个 recovery bindings；
- normal recovery overhead=0。

### 负向故障注入

至少模拟：

- 删除一个 runner；
- 添加第二个同角色 runner；
- 删除一个 required case binding；
- 修改 timer start；
- 修改 timer stop；
- 删除失败 attempt；
- result pipeline 非 append-only；
- capability 缺 verifier；
- recovery 缺一个 fault；
- normal path 强制 recovery；
- Jev retry=1；
- Jev max request=2；
- 将 JEV_COMPAT 改成主指标；
- 执行器自行猜路径；
- 失败后 SELF_REPAIR；
- 虚拟阶段发生真实 browser/Jev/open-agent I/O。

要求所有错误都在现实运行前 BLOCK。

最低：

POSITIVE_ASSERTIONS>=30
NEGATIVE_FAULT_INJECTIONS>=16
VIRTUAL_ACCURACY=100%

---

## 7. deployment-manifest

对以下全部文件计算 SHA256：

- 七门配置；
- deployment manifest 自身以外的所有总装文件；
- 解析到的 F1/F2/F3 manifests；
- harness contract/schema；
- final-router contract/schema；
- capability source；
- reality competition contract；
- generated v2 command。

记录：

source_commit
generated_at
file_path
sha256
role

写后回读。

---

## 8. 生成最终现实竞争命令 v2

只有当：

D001_RESOLVED=PASS
D002_RESOLVED=PASS
D003_RESOLVED=PASS
D004_RESOLVED=PASS
D005_RESOLVED=PASS
D006_RESOLVED=PASS
D007_RESOLVED=PASS
AMBIGUOUS_BINDINGS=0
UNBOUND_REQUIRED_CASES=0
TIMING_BOUNDARY_OVERRIDES=0
DROPPED_FAILURE_ATTEMPTS=0
VIRTUAL_99=PASS
REAL_BROWSER_RUNS=0
REAL_JEV_REQUESTS=0
REAL_OPEN_AGENT_REQUESTS=0

才允许生成并启用：

deployment-complete-v1\FINAL-REALITY-COMPETITION-COMMAND-v2.md

该命令必须：

- 只读取 deployment-complete-v1；
- 只调用已经绑定好的 harness/routes；
- 不允许重新解析/猜路径；
- 不允许写 glue code；
- 不允许修改合同；
- 不允许 Codex 决定最终产品；
- 运行完只回传 reality data；
- STOP。

否则：

FINAL_REALITY_COMMAND_V2=NOT_AUTHORIZED

---

## 9. PASS

必须：

D001_RESOLVED=PASS
D002_RESOLVED=PASS
D003_RESOLVED=PASS
D004_RESOLVED=PASS
D005_RESOLVED=PASS
D006_RESOLVED=PASS
D007_RESOLVED=PASS
RUN_CONFIG=PASS
MATRIX_BINDING=PASS
CONDITION_STATE_MACHINE=PASS
TVALID_RECORDER=PASS
RESULT_PIPELINE=PASS
CAPABILITY_MATRIX=PASS
RECOVERY_BINDING=PASS
AMBIGUOUS_BINDINGS=0
UNBOUND_REQUIRED_CASES=0
POSITIVE_ASSERTIONS>=30
NEGATIVE_FAULT_INJECTIONS>=16
VIRTUAL_ACCURACY=100%
REAL_BROWSER_RUNS=0
REAL_JEV_REQUESTS=0
REAL_OPEN_AGENT_REQUESTS=0
PRODUCTION_MUTATION=0
CODEX_SELF_REPAIR=0
DEPLOYMENT_COMPLETENESS=PASS
REALITY_COMPETITION_READY=YES
ACTION=STOP

任一失败：

DEPLOYMENT_COMPLETENESS=BLOCKED
REALITY_COMPETITION_READY=NO
REALITY_DELTA=<exact issue>
ACTION=STOP

禁止自行修。

---

## 10. 最终回传

只回传：

METHOD_AUTHORITY=
CORE=
SKILL=
SKILL_VERSION=
FROZEN_SOURCE_COMMIT=
FROZEN_SOURCE_GATE=
D001_RESOLVED=
D002_RESOLVED=
D003_RESOLVED=
D004_RESOLVED=
D005_RESOLVED=
D006_RESOLVED=
D007_RESOLVED=
RUN_CONFIG=
MATRIX_BINDING=
CONDITION_STATE_MACHINE=
TVALID_RECORDER=
RESULT_PIPELINE=
CAPABILITY_MATRIX=
RECOVERY_BINDING=
AMBIGUOUS_BINDINGS=
UNBOUND_REQUIRED_CASES=
POSITIVE_ASSERTIONS=
NEGATIVE_FAULT_INJECTIONS=
VIRTUAL_ACCURACY=
REAL_BROWSER_RUNS=
REAL_JEV_REQUESTS=
REAL_OPEN_AGENT_REQUESTS=
PRODUCTION_MUTATION=
CODEX_SELF_REPAIR=
DEPLOYMENT_COMPLETENESS=
REALITY_COMPETITION_READY=
FINAL_REALITY_COMMAND_V2=
ACTION=
EVIDENCE_FILES=
LOCAL_COMMIT=
SHA256=

最后一行原样返回：

【playwright浏览器自动化5｜物化浏览器现实竞争总装｜1｜高智能虚拟成熟】
