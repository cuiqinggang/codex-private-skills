# Browser Reality R3 验收

版本：1.2.0

## A. 历史保护
- R1/R2 文件未覆盖：PASS 才能继续。
- Reality Fingerprint V3 保持原值：`9bdd4430596e306cf6f8061069659e2680d8a1b66bd69d7bb3e45fe4cfd63dd8`。
- 新浏览器采集必须使用新的 r3-browser 快照目录。

## B. Reality 不变性
必须全部为 YES：
```text
PROXY_CHANGED=NO
NETWORK_SETTINGS_CHANGED=NO
PROFILE_MUTATED_BY_COLLECTOR=NO
SERVICE_WORKER_POLICY_CHANGED=NO
ROUTING_OR_MOCK_ENABLED_BY_COLLECTOR=NO
PAGE_CONTENT_MUTATED_BY_COLLECTOR=NO
```

## C. 计时与观测分离
```text
GOLDEN_TIMING_RUN_PRESENT=YES
GOLDEN_OBSERVABILITY_RUN_PRESENT=YES
OBSERVABILITY_TIME_USED_AS_T_VALID=NO
```

## D. 浏览器关键状态
必须有确定证据：
- Node / Playwright / Browser product+version。
- 浏览器可执行文件和启动配置安全指纹。
- Context 类型、实际 viewport/locale/timezone/userAgent。
- Profile/userDataDir 安全指纹。
- Page/Frame/Worker/Service Worker 图。
- 登录态判据。
- Cookie/LocalStorage/IndexedDB/SessionStorage/OPFS 能力与存在性摘要；不要求上传明文。

## E. #dialog / 目标元素 actionability
对于 Golden Task 的目标 locator，必须保存：
```text
LOCATOR_COUNT
VISIBLE
STABLE
RECEIVES_EVENTS_APPROX
ENABLED
BOUNDING_BOX
HIT_TARGET
OVERLAY_OR_INTERCEPTOR
ACTIVE_ANIMATIONS
PLAYWRIGHT_TRACE_ACTION_LOG
```

如果 click 失败而上述证据缺失：
`BROWSER_REALITY_ANCHOR_COMPLETE=NO`。

## F. 网络
必须至少同时具备：
1. 宿主网络摘要：接口、DNS、路由、WinHTTP/用户代理摘要、代理环境变量存在性/安全哈希。
2. 浏览器网络：request/response/finish/failure、redirect、timing、protocol、cache/service-worker 来源（可得时）。
3. WebSocket（存在时）连接、握手和帧尺寸/哈希摘要。
4. TLS/security details（可得时）。
5. 远端正文、Cookie、Authorization、Token 不得明文进入远端安全镜像。

若 Service Worker 存在：
`SERVICE_WORKER_REALITY_CAPTURED=YES`，
而不是为了抓网络把它 block。

## G. Runtime
必须捕获：
- console
- pageerror / Runtime.exceptionThrown
- crash
- lifecycle/frame 事件
- JavaScript dialog opening/closing（CDP 只读）
- CORS/CSP/blocked reason（事件提供时）

## H. 原始证据与远端安全镜像
本机 raw 至少：
- trace.zip
- cdp.jsonl
- storage-state.json
- dom-snapshot.json
远端：
- 原始敏感文件本身不提交
- 只提交 SHA-256、大小、结构摘要、脱敏事件

## I. Golden Task 现实复现
至少三次同合同复现，记录每次：
`OUTCOME / ERROR / START / END / SELECTOR / URL_SAFE / ARTIFACT_HASH_SET`。

只有三次结果的关键失败/成功语义一致，才可：
`GOLDEN_TASK_REALITY_REPRODUCED=3_OF_3`。

## J. Browser R3 最终门禁
只有以下全部成立：
```text
BROWSER_CRITICAL_UNKNOWN_COUNT=0
BROWSER_EXECUTION_RELEVANT_STATE_COMPLETE=YES
GOLDEN_TASK_REALITY_REPRODUCED=3_OF_3
SECRET_PLAINTEXT_ZERO_REMOTE=PASS
OBSERVATION_PERTURBATION=NO
BROWSER_R3_FINGERPRINT_CREATED=YES
```
才允许：
`BROWSER_TWIN_INPUT_READY=YES`。

当前冻结状态：
```text
BROWSER_R3_COLLECTOR_CONTRACT=FROZEN
BROWSER_R3_REAL_CAPTURE=NOT_YET
BROWSER_TWIN_INPUT_READY=NO
ENVIRONMENT_99=NOT_YET
```
