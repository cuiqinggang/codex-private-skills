# JEV-native R2 唯一冻结源

```text
SOURCE_OF_TRUTH=THIS_FILE
PROJECT=playwright浏览器自动化10
FREEZE_ID=JEV-NATIVE-PLAYWRIGHT-EXTREME-V1-R2-EXECUTABLE
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

本固定 Golden 的 action/selector/VALID 均由 state + frozen contract 唯一确定，因此按现有 JEV Virtual-99 规则必须走 CODE，而不是为了“出现 JEV”强行增加网络调用。

```text
GOLDEN_DECISION_CLASS=DETERMINISTIC
GOLDEN_JEV_CALLS_EXPECTED=0
JEV_LAYER_AVAILABLE=YES
JEV_REQUIRED_ONLY_FOR_NON_CODEABLE_CLOSED_SEMANTIC_DECISION=YES
FORCE_JEV_ON_DETERMINISTIC_GOLDEN=FORBIDDEN
```

这不是删除 JEV-native 架构，而是执行其既有职责边界：
- CODE：状态 + 冻结合同可唯一确定；
- JEV：无法 CODE 化的闭合语义判断；
- GPT/DeepSeek：开放问题，只能回 GPT 后重新虚拟成熟，禁止现实现场调用。

因此本次现实测速专门验证 JEV-native 架构的**确定性最快分支**，不人为增加 JEV latency。

## 5. 可执行 Runner 已冻结

上一轮 `FROZEN_SOURCE_NOT_MECHANICALLY_EXECUTABLE` 的根因已经在这里关闭：不再允许 Codex自己物化/设计 runner，Runner 文件本身已经成为冻结资产。

```text
RUNNER_PRESENT=YES
RUNNER_SOURCE_RELATIVE_PATH=docs/playwright-browser-automation/20260922-jev-native-r2/REAL-VERIFY-RUNNER.cjs
RUNNER_SHA256=da3832e99299fc9e0781880bb0070d8d64db10499c628d8b47316b408729e4aa
RUNNER_MATERIALIZED_PATH=C:\Users\A\playwright-browser-automation5-final-reality-competition-work\TWIN-PLAYWRIGHT-GOLDEN-REALITY-SHADOW\JEV-NATIVE-VIRTUAL-99\REAL-VERIFY-RUNNER.cjs
RUNNER_SYNTAX_CHECK=PASS
NEW_RUNNER_DESIGN_BY_CODEX=FORBIDDEN
```

Runner 已冻结的执行语义：
- Browser/Context/Page 在 measured T0 前建立；
- 每轮 measured run 先恢复 ready initial state，再开始 T0；
- 继承 Golden 的 page state、navigation、locator、input、click、extract、keyboard、drag/drop、upload、download、dialog、popup、frame、route/api、isolated-context 业务语义；
- 使用 `goto(...,{waitUntil:'commit'})` + Locator signal readiness；
- 不使用固定 waitForTimeout / networkidle；
- trace/screenshot/reconnect 等非 first-valid 热路径内容不进入 T_VALID；
- first complete independent hot-path VALID 后立即 T1；
- 3 warmups + 30 measured；
- 30/30 VALID 才允许现实结果成立。

## 6. Runner 唯一物化和执行流程

Codex 不得重写 runner。只允许下列确定性动作：

1. 在 `SHARED_REPO_LOCAL` 验证 origin 指向 `cuiqinggang/codex-private-skills`。
2. 执行一次：
   `git fetch origin codex/playwright-browser-automation10-jev-native-r2-final-freeze`
3. 用：
   `git show origin/codex/playwright-browser-automation10-jev-native-r2-final-freeze:docs/playwright-browser-automation/20260922-jev-native-r2/REAL-VERIFY-RUNNER.cjs`
   原字节写到 `RUNNER_MATERIALIZED_PATH`。
4. 计算 SHA-256，必须精确等于：
   `da3832e99299fc9e0781880bb0070d8d64db10499c628d8b47316b408729e4aa`
5. 执行：
   `node C:\Users\A\playwright-browser-automation5-final-reality-competition-work\TWIN-PLAYWRIGHT-GOLDEN-REALITY-SHADOW\JEV-NATIVE-VIRTUAL-99\REAL-VERIFY-RUNNER.cjs`
6. 原样回传 runner 最终输出，STOP。

若任何一步无法机械执行：

```text
REALITY_DELTA=EXECUTABLE_FREEZE_MATERIALIZATION_FAILED
ACTION=STOP
RETURN_TO_GPT=YES
```

禁止现场修改 runner 后继续。

## 7. 最终输出格式

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

## 8. 极短交接合同

聊天页面不再重复设计、版本、hash 或 runner 细节。

Codex 唯一需要收到：

```text
CURRENT_STEP=3
LOCAL_SHARED_REPO=C:\Users\A\Documents\Codex\codex-private-skills
读取唯一冻结源，按其中“Runner 唯一物化和执行流程”执行。
只回传最终结果；任何 Reality Delta 立即停止。
```
