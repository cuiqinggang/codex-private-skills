# JEV-native R2 唯一冻结源

```text
SOURCE_OF_TRUTH=THIS_FILE
PROJECT=playwright浏览器自动化10
FREEZE_ID=JEV-NATIVE-PLAYWRIGHT-EXTREME-V1-R2-STREAM-EXEC
STATUS=VIRTUAL_99_EXECUTABLE_FROZEN
CURRENT_STEP=3
CURRENT_CORE=高智能虚拟成熟
EXECUTOR_ROLE=RUN_VERIFY_REPORT_STOP
```

## 0. 冻结源定位与本机授权

```text
SHARED_REPO_REMOTE=cuiqinggang/codex-private-skills
SHARED_REPO_LOCAL=C:\Users\A\Documents\Codex\codex-private-skills
SOURCE_BRANCH=codex/playwright-browser-automation10-jev-native-r2-final-freeze
SOURCE_RELATIVE_PATH=docs/playwright-browser-automation/20260922-jev-native-r2/JEV-NATIVE-R2-FROZEN-SOURCE.md
RUNNER_SOURCE_RELATIVE_PATH=docs/playwright-browser-automation/20260922-jev-native-r2/REAL-VERIFY-RUNNER.cjs
RUNNER_GIT_BLOB_SHA=9b5d2c870c60a9a6a1edeb78623dee66fca0e644

WORKSPACE=C:\Users\A\playwright-browser-automation5-final-reality-competition-work
BROWSER_ROOT=C:\AI\Playwright-Native-AI-Browser

SHARED_REPO_READ_AUTHORIZED=YES
WORKSPACE_VERIFY_AUTHORIZED=YES
BROWSER_ROOT_READ_AND_VERIFY_AUTHORIZED=YES
PROXY_OR_SYSTEM_MUTATION_AUTHORIZED=NO
```

只允许使用上述 C 盘路径。禁止猜路径、搜索其他盘或修改代理/Windows 系统设置。

## 1. 唯一目标

```text
VALID=PASS
T*=min(T_VALID)

T_TARGET_MS=820
T_MATURE_MAX_MS=1050
HISTORICAL_T_STAR_REAL_MS=1525.09
```

T0 = 正式热路径任务开始。
T1 = 第一个完整、独立、正确的 VALID 结果出现。
除 T_VALID 外不建立第二评分指标。

## 2. 方法/步骤固定

```text
METHOD_ID=first-principles-physical-limit-convergence
DESIGN_AUTHORITY_VERSION=3.1.7
LOCAL_EXECUTION_GATE_COMPATIBLE_FROM=3.1.6
CURRENT_STEP=3
SHORT_HANDOFF_MUST_NOT_DUPLICATE_METHOD_VERSION=YES
```

Codex 只执行、验证、回报、停止。任何 Reality Delta 都必须 STOP 并返回 GPT；禁止现场修复、改路由、改模型、改 VALID 或改计时边界。

## 3. 固定身份

```text
TASK_SHA256=31f60923bddd1fece2a1d64a574f6ad5a3bc16fd0b0ef01127c87522e7084960
VALID_RULE_SHA256=2d2e4ab5495fdffb921a57113e6c7ecf5e9cf6802f9a729386bf941a3fd5c7ae
CANONICAL_GOLDEN_SHA256=1c67a634e0c0fc24ed057752358f4c20a6c05550be6146fd8d11b1a723f25e08
BROWSER_R3_FINGERPRINT_SHA256=9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd
```

固定本机入口：
- Golden: `C:\AI\Playwright-Native-AI-Browser\scripts\golden-harness.cjs`
- Fixture: `C:\AI\Playwright-Native-AI-Browser\scripts\local-fixture-server.cjs`
- Twin profile: `C:\Users\A\playwright-browser-automation5-final-reality-competition-work\TWIN-PLAYWRIGHT-GOLDEN-REALITY-SHADOW\PLAYWRIGHT_GOLDEN_REALITY_PROFILE.json`

任何固定身份不匹配：立即 Reality Delta。

## 4. JEV-native 分工最终冻结

本固定 Golden 的 action/selector/VALID 均由 state + frozen contract 唯一确定，因此按现有 JEV Virtual-99 规则走 CODE，不为了“出现 JEV”强行增加网络调用。

```text
GOLDEN_DECISION_CLASS=DETERMINISTIC
GOLDEN_JEV_CALLS_EXPECTED=0
JEV_LAYER_AVAILABLE=YES
JEV_REQUIRED_ONLY_FOR_NON_CODEABLE_CLOSED_SEMANTIC_DECISION=YES
FORCE_JEV_ON_DETERMINISTIC_GOLDEN=FORBIDDEN
```

## 5. 可执行 Runner 冻结

```text
RUNNER_PRESENT=YES
RUNNER_EXECUTION_MODE=GIT_OBJECT_STREAM_TO_NODE_STDIN
RUNNER_MATERIALIZATION=NONE
RUNNER_PATCH_ALLOWED=NO
RUNNER_FILE_WRITE_ALLOWED=NO
RUNNER_REDESIGN_ALLOWED=NO
RUNNER_GIT_BLOB_SHA=9b5d2c870c60a9a6a1edeb78623dee66fca0e644
```

上一轮 `EXECUTABLE_FREEZE_MATERIALIZATION_FAILED` 的根因是仍要求把 runner 写入工作区，因此执行器尝试 patch。该层现已删除。

Runner 不再被复制、patch、生成或覆盖。Git object 本身就是可执行冻结资产。

## 6. 唯一现实验证流程

Codex 只允许以下确定性动作：

1. 在 `SHARED_REPO_LOCAL` 确认 Git origin 为 `cuiqinggang/codex-private-skills`。
2. 只执行一次：
   `git fetch origin codex/playwright-browser-automation10-jev-native-r2-final-freeze`
3. 验证 Runner Git blob：
   `git rev-parse origin/codex/playwright-browser-automation10-jev-native-r2-final-freeze:docs/playwright-browser-automation/20260922-jev-native-r2/REAL-VERIFY-RUNNER.cjs`
   必须精确等于：
   `9b5d2c870c60a9a6a1edeb78623dee66fca0e644`
4. 不创建任何 runner 文件，直接执行冻结 Git object：
   `git show origin/codex/playwright-browser-automation10-jev-native-r2-final-freeze:docs/playwright-browser-automation/20260922-jev-native-r2/REAL-VERIFY-RUNNER.cjs | node -`
5. 原样回传 Runner 最终结果并 STOP。

明确禁止：

```text
apply_patch
Set-Content runner
Out-File runner
Copy-Item runner
生成新的 runner
编辑 runner
改变 runner
checkout/switch/merge/rebase
```

如果 Git blob 不匹配、stdin 执行环境不支持、或 Runner 自身返回 Reality Delta：

```text
ACTION=STOP
RETURN_TO_GPT=YES
```

不得换另一种实现继续尝试。

## 7. Runner 固定执行语义

冻结 Runner 自身负责：
- 校验 TASK / VALID / canonical Golden / Browser R3 / Twin；
- Runtime / Browser / Context / Page 在 measured T0 前建立；
- 每轮恢复 ready initial state 后再 T0；
- 复用 Golden 的确定性业务动作与 VALID 语义；
- signal-driven readiness；
- 无 fixed wait / networkidle 主等待；
- 3 warmups；
- 30 measured；
- 30/30 VALID；
- 输出 min/P50/P95/max；
- 比较 820 / 1050 / 1525.09；
- Reality Delta -> STOP -> GPT。

## 8. 最终输出格式

```text
REAL_RUNS=
VALID_RUNS=
T_REAL_MIN_MS=
T_REAL_P50_MS=
T_REAL_P95_MS=
T_REAL_MAX_MS=
TARGET_820_REACHED=
MATURE_1050_REACHED=
BEATS_1525_09=
NEW_T_STAR_REAL_MS=
REALITY_DELTA=
ACTION=STOP
RETURN_TO_GPT=
```

## 9. 极短交接合同

聊天页面不再重复设计、版本、hash 或 runner 内容。

Codex 唯一需要收到：

```text
CURRENT_STEP=3
LOCAL_SHARED_REPO=C:\Users\A\Documents\Codex\codex-private-skills
读取唯一冻结源并执行“唯一现实验证流程”。
禁止物化/patch/修改 Runner；任何 Reality Delta 立即停止。
```
