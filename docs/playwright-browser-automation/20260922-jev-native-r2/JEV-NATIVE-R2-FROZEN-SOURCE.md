# JEV-native R2 唯一冻结源

```text
SOURCE_OF_TRUTH=THIS_FILE
PROJECT=playwright浏览器自动化10
FREEZE_ID=JEV-NATIVE-PLAYWRIGHT-EXTREME-V1-R2
STATUS=VIRTUAL_99_FROZEN
CURRENT_STEP=3
CURRENT_CORE=高智能虚拟成熟
EXECUTOR_ROLE=RUN_VERIFY_REPORT_STOP
```

## 1. 唯一目标

```text
VALID=PASS
T*=min(T_VALID)

T_TARGET_MS=820
T_MATURE_MAX_MS=1050
HISTORICAL_T_STAR_REAL_MS=1525.09
```

T0 = 正式任务开始。
T1 = 第一个独立、完整、正确的 VALID 结果出现。
除 T_VALID 外不建立第二评分指标。

## 2. 方法/版本吸收规则

```text
METHOD_ID=first-principles-physical-limit-convergence
DESIGN_AUTHORITY_VERSION=3.1.7
LOCAL_EXECUTION_GATE_COMPATIBLE_FROM=3.1.6
SHORT_HANDOFF_MUST_NOT_DUPLICATE_METHOD_VERSION=YES
```

设计权威来自 v3.1.7；本机全局接收门当前可能仍加载 v3.1.6。两者在本任务所需的硬规则上兼容：
- 三核心白名单不变；
- CURRENT_STEP=3 才允许现实验证；
- Codex 只执行/验证/回报/停止；
- Reality Delta 必须 STOP 并返回 GPT；
- 禁止 Codex 自行修复、改路由、改模型、改 VALID、改计时边界。

因此最终短交接不再重复一个容易漂移的 method version 字符串。执行器只读取本冻结源，并以本文件内 CURRENT_STEP=3 为唯一任务步骤绑定。

## 3. 固定身份

```text
TASK_SHA256=31f60923bddd1fece2a1d64a574f6ad5a3bc16fd0b0ef01127c87522e7084960
VALID_RULE_SHA256=2d2e4ab5495fdffb921a57113e6c7ecf5e9cf6802f9a729386bf941a3fd5c7ae
CANONICAL_GOLDEN_SHA256=1c67a634e0c0fc24ed057752358f4c20a6c05550be6146fd8d11b1a723f25e08
BROWSER_R3_FINGERPRINT_SHA256=9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd
```

固定本机入口：
- Workspace: `C:\Users\A\playwright-browser-automation5-final-reality-competition-work`
- Browser root: `C:\AI\Playwright-Native-AI-Browser`
- Golden: `C:\AI\Playwright-Native-AI-Browser\scripts\golden-harness.cjs`
- Fixture: `C:\AI\Playwright-Native-AI-Browser\scripts\local-fixture-server.cjs`
- Twin: `TWIN-PLAYWRIGHT-GOLDEN-REALITY-SHADOW\`
- JEV virtual package: `TWIN-PLAYWRIGHT-GOLDEN-REALITY-SHADOW\JEV-NATIVE-VIRTUAL-99\`

任何固定身份不匹配：不得继续，输出 Reality Delta。

## 4. Runner binding（运行器绑定）

Runner 不是新的方案，只是本冻结合同的机械执行适配器。

```text
RUNNER_BINDING=FROZEN
MATERIALIZE_IF_MISSING=MECHANICAL_ONLY
NEW_DESIGN_DECISION_ALLOWED=NO
```

机械物化规则：

1. 读取并校验 canonical Golden、TASK、VALID、R3/Twin 固定身份。
2. Golden 的业务动作、顺序、输入、验证器、结果语义不得增加、删除或替换。
3. 继承成熟 `PERSISTENT_WARM_SIGNAL_DIRECT_V1`：
   - Runtime / Browser / Page 在 T0 前常驻；
   - ready initial state 在 T0 前建立；
   - locator auto-wait；
   - signal/event-driven readiness；
   - 禁止固定 waitForTimeout；
   - 禁止把 networkidle 当主要 readiness。
4. JEV transport 在 T0 前建立并预热；正常路径不允许 retry/fallback/cache。
5. CODE/JEV 分工固定：
   - state + frozen contract 可唯一确定 -> CODE；
   - 仅无法 CODE 化的闭合语义判断 -> JEV；
   - 开放问题不允许在现实验证中临时交给 GPT/DeepSeek，必须停止返回 GPT。
6. 每个 fresh snapshot 最多一次 canonical typed JEV request；不得拆成多轮网络往返。
7. JEV 决策必须带 snapshot fingerprint。执行前重新计算 freshness：
   - fingerprint 相同 -> 可进入 deterministic/actionability gate；
   - fingerprint 改变 -> 丢弃旧决策，重新 snapshot；若这要求改变冻结实现，STOP。
8. Playwright 执行动作前必须通过 deterministic legality + actionability/occlusion gate。
9. next-best 只能在以下条件全部满足时复用：
   - snapshot fingerprint unchanged；
   - first action 被确定性证明 NO_EFFECT；
   - first action 属于 side-effect-safe 类；
   - next-best 仍合法。
   否则不得复用。
10. FINAL_VALID 只使用冻结 VALID 规则，必须独立于 JEV 输出。
11. T1 在第一次 FINAL_VALID=PASS 时立即停止计时；结果就绪后的日志/汇总不得进入 T_VALID。

若上述任何一步需要执行器自行“想办法”、选择另一实现、改变架构或解释不明确条件：
```text
REALITY_DELTA=FROZEN_SOURCE_NOT_MECHANICALLY_EXECUTABLE
ACTION=STOP
RETURN_TO_GPT=YES
```

## 5. Virtual-99 已冻结攻击结果

```text
ARCHITECTURE=JEV-NATIVE-PLAYWRIGHT-EXTREME-V1-R2
FRESHNESS_GATE=PASS
ACTIONABILITY_GATE=PASS
SAFE_NEXT_BEST_GATE=PASS
INDEPENDENT_FINAL_VALID=PASS
UNBOUND_NODE_COUNT=0

T_VIRTUAL_STAR_TARGET_MS=820
T_VIRTUAL_MATURE_BAND_MS=820..1050
TIME_CLASSIFICATION=VIRTUAL_TARGET_NOT_REAL_CERTIFIED
```

这三个数的地位固定：
- 820 ms：Virtual-99 核心极限目标；
- 1050 ms：当前虚拟成熟上界；
- 1525.09 ms：历史现实纪录。

只有现实 measured run 才能生成新的现实 T*。

## 6. 唯一现实验证

```text
WARMUP_RUNS=3
MEASURED_RUNS=30
ALL_VALID_REQUIRED=YES
```

执行顺序：
1. 先做所有静态身份/hash/runner binding 门禁；
2. 3 次 warm-up，不计成绩；
3. 30 次 measured；
4. 每次只记录从 T0 到 first FINAL_VALID=PASS 的 T_VALID；
5. 30/30 必须 VALID=PASS。

最终只允许回报：

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

任何失败、缺绑定、hash/合同不一致、需要修改冻结方案：
```text
ACTION=STOP
RETURN_TO_GPT=YES
```

禁止现实现场修复后继续重跑。

## 7. 极短交接合同

聊天页面不再重复本文件内容，也不再重复 method version / hashes / runner 细节。

Codex 唯一需要收到：

```text
CURRENT_STEP=3
读取本唯一冻结源。
执行“唯一现实验证”。
完成后只回传冻结格式结果；任何 Reality Delta 立即停止。
```

任何更长的临时设计提示均不具有权威性。
