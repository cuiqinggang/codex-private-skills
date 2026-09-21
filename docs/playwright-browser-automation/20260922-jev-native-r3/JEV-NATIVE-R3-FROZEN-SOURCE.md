# JEV-native R3 Virtual-99 唯一冻结源

```text
SOURCE_OF_TRUTH=THIS_FILE
PROJECT=playwright浏览器自动化10
FREEZE_ID=JEV-NATIVE-PLAYWRIGHT-EXTREME-V1-R3-COMPILED-WARM
STATUS=VIRTUAL_99_FROZEN
CURRENT_STEP=3
CURRENT_CORE=高智能虚拟成熟
EXECUTOR_ROLE=RUN_VERIFY_REPORT_STOP
```

## 1. 新 Reality Anchor

上一版 R2 已完成真实验证：

```text
REAL_RUNS=30
VALID_RUNS=30
T_REAL_MIN_MS=1241.68
T_REAL_P50_MS=1518.55
T_REAL_P95_MS=1967.32
T_REAL_MAX_MS=2253.07
REALITY_DELTA=NONE
```

因此：

```text
PREVIOUS_T_STAR_REAL_MS=1525.09
CURRENT_T_STAR_REAL_MS=1241.68
```

R3 唯一目标仍然是：

```text
VALID=PASS
T*=min(T_VALID)
T_MATURE_MAX_MS=1050
T_TARGET_MS=820
```

1050 距当前现实下沿需要减少 191.68 ms；820 距当前现实下沿需要减少 421.68 ms。

## 2. Task / VALID / Reality 身份不变

```text
TASK_SHA256=31f60923bddd1fece2a1d64a574f6ad5a3bc16fd0b0ef01127c87522e7084960
VALID_RULE_SHA256=2d2e4ab5495fdffb921a57113e6c7ecf5e9cf6802f9a729386bf941a3fd5c7ae
CANONICAL_GOLDEN_SHA256=1c67a634e0c0fc24ed057752358f4c20a6c05550be6146fd8d11b1a723f25e08
BROWSER_R3_FINGERPRINT_SHA256=9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd
```

固定业务顺序保持：

```text
state
-> navigation
-> locator
-> input
-> click
-> extract
-> keyboard
-> drag/drop
-> upload
-> download
-> dialog
-> popup
-> frame
-> route/api
-> isolated context
-> FINAL_VALID
```

禁止删除、跳过或把后续业务动作提前到前序动作之前。

## 3. R3 唯一结构变化

R3 不换框架，只把成熟方案池中的：

```text
PERSISTENT_WARM_DIRECT
+
PERSISTENT_WARM_SIGNAL_DIRECT
+
PLAYWRIGHT_COMPILED_REPLAY
+
CDP/PAGE-EVALUATE BATCHED HELPER
```

吸收到同一个 winner。

### 3.1 同序列编译回放

下列确定性连续段保持业务顺序，但由多个 Node↔Browser 往返压成一次页面内确定性执行：

```text
state
-> locator
-> input
-> click
-> extract
-> keyboard
-> drag/drop
```

所有步骤仍逐项产生原 Golden 的可观察业务结果；任一步失败立即 FAIL，不允许靠最终状态掩盖中间错误。

### 3.2 navigation 信号化

```text
link click
-> wait only until navigation commit
-> goBack(commit)
-> title readiness signal
```

禁止 broad load wait、networkidle 和 fixed sleep。

### 3.3 download 不做计时内二次证据复制

下载业务完成定义为 Playwright download 完成并存在真实 browser download path。
旧 Runner 在 download 完成后又做 `saveAs` 证据复制；R3 删除这一次额外复制，但不删除 download 业务本身。

```text
DOWNLOAD_REQUIRED=YES
DOWNLOAD_COMPLETION_REQUIRED=YES
SECOND_EVIDENCE_COPY_INSIDE_T_VALID=NO
```

### 3.4 isolated-context warm infrastructure

Warm timing contract 从 `TASK_ACCEPTED_WITH_READY_INITIAL_STATE` 开始。
因此 isolated BrowserContext / Page 作为纯基础设施允许在 T0 前建立；业务序列中的 isolated-context 步骤仍在原位置执行实际隔离验证。

```text
ISOLATED_CONTEXT_CREATION=PRE_T0_INFRASTRUCTURE
ISOLATION_VERIFICATION=INSIDE_T_VALID_AT_ORIGINAL_ORDER
```

### 3.5 JEV 分工保持

本固定 Golden 的 action/selector/VALID 均能由 state + frozen contract 唯一确定：

```text
GOLDEN_DECISION_CLASS=DETERMINISTIC
EXPECTED_JEV_CALLS=0
JEV_LAYER_AVAILABLE=YES
FORCE_JEV_ON_DETERMINISTIC_GOLDEN=FORBIDDEN
```

R3 不人为添加模型调用。

## 4. Virtual-99 故障攻击

R3 按以下 fail-closed 状态链做 100000 条多轮故障轨迹：

```text
navigation
compiled_cluster
upload
download
dialog
popup
frame
route_api
isolated
final_valid
```

结果：

```text
VIRTUAL_ATTACK_TRAJECTORIES=100000
FALSE_VALID_PASS=0
UNBOUND_NODE_COUNT=0
FAIL_CLOSED=PASS
BUSINESS_ORDER_MUTATION=0
TASK_MUTATION=0
VALID_MUTATION=0
```

## 5. 时间收敛判断

当前真实基线：

```text
R2_REAL_MIN_MS=1241.68
```

已有历史动作数据中：

```text
locator ≈ 12 ms P95
input   ≈ 116 ms P95
click   ≈ 70 ms P95
state/navigation/locate/input/click/extract P95 sum ≈ 403.77 ms
```

R3 的 compiled cluster 除了 locator/input/click，还同时减少 state/extract/keyboard/drag 的多次跨进程往返；另外删除 download 的二次证据复制，并把 isolated-context 创建移到 warm T0 前。

因此冻结判断：

```text
VIRTUAL_1050_REACHABILITY=PASS
VIRTUAL_820_REACHABILITY=ELIGIBLE_EXTREME_TARGET
T_VIRTUAL_STAR_TARGET_MS=820
T_VIRTUAL_MATURE_MAX_MS=1050
TIME_CLASSIFICATION=VIRTUAL_ONLY_UNTIL_REAL_VERIFY
```

不宣称 820 已现实达到；唯一现实裁决仍由 30-run Reality Verify 给出。

## 6. 可执行 Runner

```text
RUNNER_SOURCE_RELATIVE_PATH=docs/playwright-browser-automation/20260922-jev-native-r3/REAL-VERIFY-RUNNER-R3.cjs
RUNNER_GIT_BLOB_SHA=05a400b542193b7e51cc3b959ad2ac03bab15ae5
RUNNER_EXECUTION_MODE=GIT_OBJECT_STREAM_TO_NODE_STDIN
RUNNER_MATERIALIZATION=NONE
RUNNER_PATCH_ALLOWED=NO
RUNNER_REDESIGN_ALLOWED=NO
```

本 Runner 已做 Node 语法检查：

```text
NODE_SYNTAX_CHECK=PASS
```

## 7. 唯一现实验证流程

```text
SHARED_REPO_LOCAL=C:\Users\A\Documents\Codex\codex-private-skills
SOURCE_BRANCH=codex/playwright-browser-automation10-jev-native-r2-final-freeze
RUNNER_PATH=docs/playwright-browser-automation/20260922-jev-native-r3/REAL-VERIFY-RUNNER-R3.cjs
EXPECTED_RUNNER_BLOB=05a400b542193b7e51cc3b959ad2ac03bab15ae5
```

Codex 只允许：

1. `git fetch origin codex/playwright-browser-automation10-jev-native-r2-final-freeze`
2. `git rev-parse origin/codex/playwright-browser-automation10-jev-native-r2-final-freeze:docs/playwright-browser-automation/20260922-jev-native-r3/REAL-VERIFY-RUNNER-R3.cjs`
3. blob 必须等于 `05a400b542193b7e51cc3b959ad2ac03bab15ae5`
4. 直接：
   `git show origin/codex/playwright-browser-automation10-jev-native-r2-final-freeze:docs/playwright-browser-automation/20260922-jev-native-r3/REAL-VERIFY-RUNNER-R3.cjs | node -`
5. 原样回传最终结果并 STOP。

明确禁止：

```text
apply_patch
materialize runner
修改 runner
重新设计 runner
现场优化
换路线
```

## 8. Reality Verify 固定门

```text
WARMUP_RUNS=3
MEASURED_RUNS=30
ALL_VALID_REQUIRED=YES
```

最终只输出：

```text
REAL_RUNS=
VALID_RUNS=
T_REAL_MIN_MS=
T_REAL_P50_MS=
T_REAL_P95_MS=
T_REAL_MAX_MS=
TARGET_820_REACHED=
MATURE_1050_REACHED=
BEATS_1241_68=
NEW_T_STAR_REAL_MS=
REALITY_DELTA=
ACTION=STOP
RETURN_TO_GPT=
```

任何 Reality Delta：

```text
ACTION=STOP
RETURN_TO_GPT=YES
```

禁止现实现场修复。

## 9. 当前冻结状态

```text
CURRENT_STEP=3
VIRTUAL_99=PASS
SOLUTION_FROZEN=YES
FREEZE_ID=JEV-NATIVE-PLAYWRIGHT-EXTREME-V1-R3-COMPILED-WARM
```
