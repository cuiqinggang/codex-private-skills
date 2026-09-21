# PLAYWRIGHT 浏览器自动化10｜Browser Reality R3 最终现实采集冻结命令 v1

定位：`CURRENT_STEP=1 / 成熟现实 / CORE_OWNER=成熟方案集群`。

本文件是唯一执行真相。Codex 只允许 `EXECUTE → VERIFY → REPORT → STOP`；禁止分析、设计、优化、修复、重规划、Virtual-99。

## 0. 权威与冻结输入

- 页面名：`playwright浏览器自动化10`
- 母方法：`first-principles-physical-limit-convergence@3.1.7`
- 权威分支：`codex/first-principles-physical-limit-convergence-v3.1.7`
- 权威 HEAD：`7f5cd0de2556f37efe760d862516365567f6e12e`
- Reality Anchor：`reality-execution-environment-anchor@1.2.0`
- Exact Twin：`exact-reality-digital-twin@1.1.0`（本命令禁止进入 Twin）
- Browser R3 collector：`skills/reality-execution-environment-anchor/collectors/browser-reality-r3.mjs`
- Host network collector：`skills/reality-execution-environment-anchor/collectors/browser-host-network-r3.ps1`
- R3 contract：`skills/reality-execution-environment-anchor/BROWSER-REALITY-R3-CONTRACT.json`
- R3 acceptance：`skills/reality-execution-environment-anchor/BROWSER-REALITY-R3-ACCEPTANCE.md`
- 当前工作目录：`C:\Users\A\playwright-browser-automation5-final-reality-competition-work`
- 浏览器工程：`C:\AI\Playwright-Native-AI-Browser`
- 当前 Canonical Golden：`C:\AI\Playwright-Native-AI-Browser\scripts\golden-harness.cjs`
- 当前 Canonical Golden SHA256：`9ec5020496a7d703eae0da7ffbe0c6968bdd669cd848469e844bcc6f508d2cfb`
- Reality Pack：`C:\Users\A\playwright-browser-automation5-final-reality-competition-work\REALITY-PACK`
- Reality Pack manifest SHA256：`fd7d381a7f8185a5c12af7a74f7b4d43809d172d84fff78454863383ae9727cd`
- TASK_SHA256：`31f60923bddd1fece2a1d64a574f6ad5a3bc16fd0b0ef01127c87522e7084960`
- VALID_RULE_SHA256：`2d2e4ab5495fdffb921a57113e6c7ecf5e9cf6802f9a729386bf941a3fd5c7ae`
- 历史现实纪录：`HISTORICAL_T_STAR_REAL_MS=1525.09`，本命令不得覆盖。

## 1. 本命令唯一目标

完成 Browser Reality R3 的最后现实采集并形成可供唯一 Exact Twin 使用的 R3 输入。

最终只有以下全部成立才 PASS：

```text
BROWSER_CRITICAL_UNKNOWN_COUNT=0
BROWSER_EXECUTION_RELEVANT_STATE_COMPLETE=YES
GOLDEN_TASK_REALITY_REPRODUCED=3_OF_3
SECRET_PLAINTEXT_ZERO_REMOTE=PASS
OBSERVATION_PERTURBATION=NO
BROWSER_R3_FINGERPRINT_CREATED=YES
BROWSER_TWIN_INPUT_READY=YES
```

本命令不得修改、运行或进入 `exact-reality-digital-twin`；不得开始 Reality Shadow、Virtual-99、Step 2、Step 3。

## 2. 硬边界

始终禁止：

- 修改 FlClash、代理、Windows 网络、网卡、DNS、路由、ACL。
- 污染共享浏览器 Profile。
- block Service Worker。
- 增加 request routing / mock / network emulation。
- 修改页面内容、Cookie、登录态、TASK、VALID、URL、locator、wait、业务动作顺序。
- 上传 raw trace、raw HAR、raw storage-state、Cookie/token/Authorization 明文到 GitHub。
- 因现实失败自行换方案或补丁。

任何现实差异：记录 `REALITY_DELTA`，立即 STOP，返回 GPT。

## 3. 方法版本与源码门禁

先机械核验：

1. 远端权威分支 HEAD 必须精确为 `7f5cd0de2556f37efe760d862516365567f6e12e`。
2. 远端 `VERSION` 必须为 `3.1.7`。
3. Anchor `VERSION` 必须为 `1.2.0`。
4. Twin `VERSION` 必须为 `1.1.0`。
5. 当前 Golden SHA256 必须精确等于 `9ec5020496a7d703eae0da7ffbe0c6968bdd669cd848469e844bcc6f508d2cfb`。
6. Reality Pack manifest SHA256 必须精确等于 `fd7d381a7f8185a5c12af7a74f7b4d43809d172d84fff78454863383ae9727cd`。

如果权威源码在本机不可得，只允许把该权威分支以 task-local 只读来源拉取到当前 workspace 的 `.r3-source-v3.1.7`；不得覆盖全局 Skill。若 Git/GitHub 鉴权阻断，`REALITY_DELTA=R3_AUTHORITY_SOURCE_UNAVAILABLE` 后 STOP。

## 4. Golden 的唯一允许变化：R3 Observer Seam

必须先 byte-for-byte 备份当前 Golden 到：

`evidence\golden-history\golden-harness.pre-r3-observer.<当前SHA>.cjs`

备份 Hash 必须等于当前 Canonical Hash。

只允许给现有 `runRound` 增加以下**默认关闭**参数：

```text
r3ObserverFactory = undefined
disableBuiltInTrace = false
```

除此之外，现有 Capture Seam 参数继续保留：

```text
captureHarPath
storageStatePath
captureTraceFromContextStart
```

业务动作一律不改。

### 4.1 Observer 启动点

在现有 `page.goto(baseURL)` + `title readiness` 完成后、`pageStateMs` 之前：

- 如果 `r3ObserverFactory` 存在，则调用一次：
  `observer = await r3ObserverFactory({browser, context, page, round, baseURL, profilePath})`。
- 若不存在，行为与当前 Canonical 完全一致。

### 4.2 Trace 所有权

- 默认 `disableBuiltInTrace=false`：保持当前 Golden trace 行为。
- R3 Observability run 必须传 `disableBuiltInTrace=true`，让官方 `browser-reality-r3.mjs` 独占 R3 raw trace。
- 不允许双 tracing.start。

### 4.3 #dialog actionability 检查点

只在原业务动作之间插入观察，不改变业务：

1. 在 `page.click('#dialog')` 之前调用 `observer.checkpoint('BEFORE_DIALOG','#dialog')`。
2. dialog accept 完成后调用 `observer.checkpoint('AFTER_DIALOG','#dialog')`。

### 4.4 Observer stop 点

在主 Context 的最后业务动作完成、现有 screenshot 完成后、main context close 前调用一次：

`observer.stop({phase:'MAIN_CONTEXT_COMPLETE'})`。

它只负责落盘 R3 raw/safe 证据；最终整个 Golden PASS/FAIL 仍以后续 reconnect 完整结果为准。

## 5. 修改后默认模式回归门

执行 `node --check`。

然后使用现有正式 `scripts\run-library.cjs`，在不传 R3 参数的情况下连续运行 3 次。

要求：

```text
DEFAULT_AFTER_R3_RUN_1=PASS
DEFAULT_AFTER_R3_RUN_2=PASS
DEFAULT_AFTER_R3_RUN_3=PASS
DEFAULT_AFTER_R3_VALID_RUNS=3/3
```

任意失败：恢复备份，核验恢复 Hash，`REALITY_DELTA=R3_OBSERVER_SEAM_REGRESSION`，STOP。

3/3 PASS 后，计算新 Golden SHA256，记为 `R3_CANONICAL_GOLDEN_SHA256`。旧 Hash 只作为历史，不删除。

## 6. R3 现实采集目录

新建且不得覆盖：

`C:\Users\A\playwright-browser-automation5-final-reality-competition-work\R3-BROWSER-REALITY`

结构固定：

```text
R3-BROWSER-REALITY\
  authority\
  host-pre\
  run-01\
  run-02\
  run-03\
  host-post\
  final\
```

如果目录已存在，禁止静默覆盖，`REALITY_DELTA=R3_TARGET_ALREADY_EXISTS`，STOP。

## 7. Host 网络只读采集

使用权威 `browser-host-network-r3.ps1`：

- Golden 三次 R3 运行前采集一次到 `host-pre`。
- 三次完成后采集一次到 `host-post`。
- 必须保持 `REALITY_MUTATION=NO`、`OUTBOUND_PROBE=NO`。
- 只允许安全摘要进入 final；raw 只留本机。

## 8. 三次 Golden Observability Run

必须使用同一 `runRound`、同一 TASK、同一 VALID、同一 profilePath、同一 fixture/URL 逻辑。

每次只允许附加 R3 observer，不得修改业务。

对 run-01 / run-02 / run-03：

1. `r3ObserverFactory` 只能调用权威 `startBrowserRealityR3`。
2. 参数固定：
   - `targetSelector='#dialog'`
   - `enableTrace=true`
   - `outputDir=<run-N>`
   - `taskId='PLAYWRIGHT_GOLDEN_R3_RUN_N'`
   - `declaredConfig` 只放非敏感配置与固定 Hash。
3. `disableBuiltInTrace=true`。
4. 不启用当前 Capture Seam 的 HAR/storageState；R3 collector 自己负责 raw storage/CDP/trace。
5. 每次 runRound 返回后，额外写 `safe/full-run-result.json`，只包含：
   - OUTCOME
   - ERROR 的安全摘要/Hash
   - START
   - END
   - SELECTOR=`#dialog`
   - URL_SAFE
   - Canonical Golden SHA256
   - TASK_SHA256
   - VALID_RULE_SHA256
   - 本次 artifact hash set。

三次 Observability time 仅作证据，绝对不得作为 T_VALID 或更新 1525.09 ms。

## 9. 每次 R3 必须存在的证据

每次至少验证：

```text
raw/trace.zip
raw/cdp.jsonl
raw/storage-state.json
raw/dom-snapshot.json
safe/events.jsonl
safe/cdp.jsonl
safe/environment.json
safe/actionability.json
safe/golden-task-result.json
safe/full-run-result.json
```

并机械验证：

- trace ZIP 可打开且 entries > 0。
- cdp.jsonl size > 0。
- dom-snapshot.json JSON parse PASS。
- storage-state.json JSON parse PASS；不得打印秘密。
- actionability.json 至少含 BEFORE_DIALOG 与 AFTER_DIALOG。
- BEFORE_DIALOG 必须能机械得到 EXACTLY_ONE / VISIBLE / STABLE / RECEIVES_EVENTS_APPROX / ENABLED 证据；任何缺失记为 unknown，不允许脑补。
- events/cdp 必须覆盖实际可观察到的 request/response/runtime/dialog/lifecycle 事件；不存在的 WebSocket/Service Worker 只能写 `NOT_PRESENT`，不能伪造。

## 10. Golden 3/3 Reality Reproduction

只有三次完整 Golden 都 PASS 且关键语义一致才允许：

`GOLDEN_TASK_REALITY_REPRODUCED=3_OF_3`。

若任一失败：不得补跑第 4 次；记录第一个现实差异并 STOP。

## 11. R3 Final Anchor 与 Fingerprint

在 `final` 内生成：

- `BROWSER-R3-FINAL-ANCHOR.json`
- `BROWSER-R3-FINGERPRINT.json`
- `BROWSER-R3-MANIFEST.json`

`BROWSER-R3-FINAL-ANCHOR.json` 必须逐项回答 R3 contract 的十个 required_modules：

```text
R3_BROWSER_PROCESS
R3_CONTEXT_CONFIG
R3_AUTH_STORAGE
R3_PAGE_GRAPH
R3_DOM_ACTIONABILITY
R3_NETWORK_HOST
R3_NETWORK_BROWSER
R3_RUNTIME_ERRORS
R3_ARTIFACTS
R3_GOLDEN_TASK_RESULT
```

每个模块只允许 `PASS / NOT_PRESENT / UNKNOWN / FAIL`，并列出 supporting artifact hash。

`BROWSER_CRITICAL_UNKNOWN_COUNT` = 所有 required_modules 与 acceptance hard fields 中 `UNKNOWN` 数量。

### Fingerprint 算法冻结

只对**安全镜像和 Hash/计数**做 fingerprint，绝不把 raw secret 纳入远端安全镜像。

算法：

1. 构造对象：method/version、R3 contract SHA、R3 collector SHA、R3_CANONICAL_GOLDEN_SHA256、TASK/VALID Hash、Reality Pack manifest Hash、host-pre safe Hash、host-post safe Hash、三次 run 的 safe artifact Hash sets、required_modules 状态。
2. 递归按 object key 升序排序；数组保持原顺序；UTF-8；无多余空白。
3. 对该 canonical JSON 计算 SHA256。
4. 写入 `BROWSER_R3_FINGERPRINT_SHA256`。

## 12. 不变性与敏感信息门

最终必须明确：

```text
PROXY_CHANGED=NO
NETWORK_SETTINGS_CHANGED=NO
PROFILE_MUTATED_BY_COLLECTOR=NO
SERVICE_WORKER_POLICY_CHANGED=NO
ROUTING_OR_MOCK_ENABLED_BY_COLLECTOR=NO
PAGE_CONTENT_MUTATED_BY_COLLECTOR=NO
OBSERVATION_PERTURBATION=NO
SECRET_PLAINTEXT_ZERO_REMOTE=PASS
```

本命令不提交 raw 到 GitHub；因此任何远端同步都只能是安全摘要/Hash，且本命令默认不做远端同步。

## 13. 最终唯一门禁

只有全部成立：

```text
DEFAULT_AFTER_R3_VALID_RUNS=3/3
R3_REAL_RUNS=3/3
BROWSER_CRITICAL_UNKNOWN_COUNT=0
BROWSER_EXECUTION_RELEVANT_STATE_COMPLETE=YES
GOLDEN_TASK_REALITY_REPRODUCED=3_OF_3
SECRET_PLAINTEXT_ZERO_REMOTE=PASS
OBSERVATION_PERTURBATION=NO
BROWSER_R3_FINGERPRINT_CREATED=YES
BROWSER_TWIN_INPUT_READY=YES
REALITY_DELTA=NONE
```

才能写：

`BROWSER_R3_REAL_CAPTURE=PASS`。

否则：

`BROWSER_R3_REAL_CAPTURE=FAIL` 或 `BLOCKED`，立即 STOP，不进入 Twin。

## 14. 最终回报格式

```text
CURRENT_STEP=1
STEP_NAME=成熟现实
CURRENT_CORE=成熟方案集群
METHOD=first-principles-physical-limit-convergence@3.1.7
METHOD_HEAD=7f5cd0de2556f37efe760d862516365567f6e12e
ANCHOR_VERSION=1.2.0
TWIN_VERSION=1.1.0

PRE_R3_CANONICAL_GOLDEN_SHA256=
BACKUP_SHA256=
R3_CANONICAL_GOLDEN_SHA256=
DEFAULT_AFTER_R3_VALID_RUNS=

R3_REAL_RUN_1=
R3_REAL_RUN_2=
R3_REAL_RUN_3=
R3_REAL_RUNS=
GOLDEN_TASK_REALITY_REPRODUCED=

R3_BROWSER_PROCESS=
R3_CONTEXT_CONFIG=
R3_AUTH_STORAGE=
R3_PAGE_GRAPH=
R3_DOM_ACTIONABILITY=
R3_NETWORK_HOST=
R3_NETWORK_BROWSER=
R3_RUNTIME_ERRORS=
R3_ARTIFACTS=
R3_GOLDEN_TASK_RESULT=

BROWSER_CRITICAL_UNKNOWN_COUNT=
BROWSER_EXECUTION_RELEVANT_STATE_COMPLETE=
OBSERVATION_PERTURBATION=
SECRET_PLAINTEXT_ZERO_REMOTE=

BROWSER_R3_FINGERPRINT_CREATED=
BROWSER_R3_FINGERPRINT_SHA256=
BROWSER_TWIN_INPUT_READY=
BROWSER_R3_REAL_CAPTURE=

HISTORICAL_T_STAR_REAL_MS=1525.09
REALITY_DELTA=
ACTION=STOP
RETURN_TO_GPT

【playwright浏览器自动化10｜Browser Reality R3最终现实采集｜1｜成熟方案集群】
```

## 15. 收尾

无论 PASS/FAIL/BLOCKED：

- 不得进入 exact-reality-digital-twin。
- 不得创建 PLAYWRIGHT_GOLDEN_REALITY_PROFILE。
- 不得开始 Reality Shadow。
- 不得进入 Step 2 / Virtual-99。
- 必须 STOP 并 RETURN_TO_GPT。
