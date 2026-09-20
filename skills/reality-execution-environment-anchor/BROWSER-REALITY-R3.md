# Browser Reality R3：浏览器现实执行环境完整锚定

版本：1.2.0
归属：核心2「成熟方案集群」
目标：在不修改现实环境的前提下，把真实浏览器 E2E（端到端）执行链补进 Reality Anchor（现实锚点），供唯一 Twin（数字孪生）消费。

## 1. 为什么需要 R3

R1/R2 已经完整锚定 Windows / Codex / 规则 / 沙盒 / 进程边界，并真实复现 `SetTokenInformation -> 1344 -> 3/3`。
但这个合同不足以代表浏览器任务。浏览器 E2E 的真实执行环境必须至少包含：

```text
Windows / 宿主网络
-> Node / Playwright
-> Browser executable + version + launch args
-> Browser Context
-> Profile / userDataDir
-> Cookie / LocalStorage / IndexedDB / SessionStorage
-> 当前登录态
-> Page / Frame / Worker / Service Worker
-> 页面 JavaScript / Console / uncaught exception
-> DOM / Shadow DOM / layout / overlay / animation
-> Playwright actionability
-> HTTP(S) / redirect / cache / DNS结果的浏览器可见表现
-> request / response / failure / timing / TLS security details
-> WebSocket / EventSource / WebTransport（出现时）
-> 远端服务器实际响应
-> Golden Task 的动作时间线和结果
```

“同一台电脑”不等于“同一个浏览器现实环境”。

## 2. Reality 模式固定原则

- READ_ONLY_CAPTURE_FIRST：先只读采集。
- NO_ENVIRONMENT_HARDENING_DURING_CAPTURE：采集期间禁止改代理、网络、Profile、Cookie、页面代码、浏览器参数、Service Worker 策略。
- REALITY_FIRST：记录现实，包括失败；不先修现实。
- HISTORY_APPEND_ONLY：R1/R2 保留，R3 新增快照，禁止覆盖旧指纹。
- SECRET_PLAINTEXT_ZERO_REMOTE：认证态、Cookie、Token、HAR/Trace 中的敏感正文只能本地原始留存；远端只允许脱敏摘要、计数、结构和 SHA-256。
- OBSERVABILITY_OVERHEAD_SEPARATION：高观测 Trace/HAR/CDP 运行不得作为极限时间基线；时间基线与诊断运行必须分开标记。

## 3. R3 双运行模型

### A. GOLDEN_TIMING_RUN（黄金计时运行）
用途：保留真实端到端时间与真实任务结果。
要求：
- 不新增会改变页面行为的 listener（监听器）或 route（网络路由）。
- 不启用会明显增加负载的全量 DOMSnapshot/Trace/HAR。
- 只记录最小起止时间、任务结果、版本/指纹引用。

### B. GOLDEN_OBSERVABILITY_RUN（黄金可观测运行）
用途：复现同一 Golden Task 的因果链。
允许只读观测：
- Playwright Trace（追踪）：screenshots / snapshots / sources / network。
- CDP（Chrome DevTools Protocol，Chrome 开发者协议）只读事件。
- 页面/Context 事件、DOMSnapshot、Console/PageError、网络时间线。
要求：
- 不把此运行的耗时当成极限时间。
- 若观测导致结果不再复现，则标记 OBSERVATION_PERTURBATION=YES，禁止把它冒充 Reality。

## 4. 成熟现实采集源

### Playwright 原生
1. Actionability（可操作性）：click 前至少涉及单一元素、Visible（可见）、Stable（稳定）、Receives Events（接收事件）、Enabled（启用）。
2. Trace Viewer（追踪查看器）：动作前/动作时/动作后 DOM snapshot、截图、源码、动作日志、网络和元数据。
3. BrowserContext storageState（存储状态）：Cookie、LocalStorage，并在当前版本能力允许时包含 IndexedDB/OPFS 等；认证状态属于敏感数据。
4. Page / BrowserContext events：request、response、requestfinished、requestfailed、console、pageerror、websocket、worker、popup 等。
5. Service Worker：必须记录其存在与 URL；Reality 模式禁止为了“看见网络请求”而直接改成 block。
6. BrowserContext / Browser metadata：页面集合、Context 数量、连接状态、Viewport/Locale/Timezone/UserAgent 等实际值。

### Chrome DevTools Protocol（CDP）
Reality 模式仅使用读取/订阅：
- Browser.getVersion
- SystemInfo.getInfo（可用时）
- Network.enable + requestWillBeSent / responseReceived / loadingFailed / loadingFinished / WebSocket 事件
- Page.enable + frame / lifecycle / load / DOMContentLoaded / dialog 事件
- Runtime.enable + consoleAPICalled / exceptionThrown
- DOMSnapshot.captureSnapshot
- Performance.getMetrics（可用时）

禁止在 Reality 模式调用改变现实语义的 CDP 命令，例如：
- Network.setBlockedURLs
- Network.emulateNetworkConditions
- Network.setCacheDisabled
- Network.setBypassServiceWorker
- Page.setDocumentContent
- Page.setWebLifecycleState

这些只可进入 Shadow（影子）试验。

## 5. 必采模块

R3_BROWSER_PROCESS
- 浏览器产品、版本、revision、协议版本、可执行文件路径/哈希（由宿主采集）、进程树、启动参数。
- Playwright 版本、Node 版本。
- persistent/ephemeral Context 类型。
- userDataDir / profile directory 的安全指纹，不上传原始敏感文件。

R3_CONTEXT_CONFIG
- viewport / screen / deviceScaleFactor
- locale / timezone
- userAgent / platform
- colorScheme / reducedMotion
- permissions / geolocation（若实际配置）
- serviceWorkers policy
- proxy 是否配置（敏感凭据必须脱敏）
- acceptDownloads / baseURL 等会影响行为的选项
- 实际 harness 传入的 launch/context options（必须由 harness 显式交给采集器，因为 Playwright 不能事后完整反射所有配置）。

R3_AUTH_STORAGE
- Cookie 数量、域集合、属性结构、值哈希
- LocalStorage / IndexedDB / SessionStorage / OPFS 的存在性、键集合和安全哈希
- 登录态判据（例如目标页面已登录标志）及其验证结果
- 原始 storageState 仅本地保存，远端禁止提交。

R3_PAGE_GRAPH
- 当前 URL（查询参数/fragment 脱敏）、title、安全哈希
- main frame + iframe 树
- popup/page graph
- worker/service worker
- Navigation / lifecycle 顺序
- document readyState / visibilityState

R3_DOM_ACTIONABILITY
目标 selector（例如 `#dialog`）必须记录：
- locator count
- visible
- enabled
- bounding box
- computed style: display/visibility/opacity/pointer-events/z-index/position/transform
- 两个连续 animation frame 的 bounding box，近似验证 Stable
- elementFromPoint hit target，近似验证 Receives Events
- active animations / transitions
- topmost overlay / intercepting element
- Playwright Trace 中对应动作日志作为最终 actionability 证据

R3_NETWORK
宿主侧：
- WinHTTP / 当前用户代理摘要
- DNS server / active interface / route 摘要
- 代理环境变量只记录 presence + 安全哈希，不上传凭据
浏览器侧：
- request -> response -> requestfinished / requestfailed 关联
- method / resourceType / status / protocol / remote address（可得时）
- redirect chain
- timing
- cache / service worker 来源
- TLS/securityDetails（可得时）
- WebSocket handshake + frame 元数据（正文默认不上传）
- EventSource/WebTransport（出现时）
- response body 默认不远端保存；仅在明确白名单且脱敏后保存。

R3_RUNTIME_ERRORS
- console
- pageerror / Runtime.exceptionThrown
- crash
- JavaScript dialog opening/closing
- CSP/CORS/blockedReason（可得时）

R3_ARTIFACTS
本地原始：
- trace.zip
- raw CDP JSONL
- raw network JSONL / HAR（如由真实 harness 已启用）
- raw storageState
- DOMSnapshot
- screenshots
远端安全镜像：
- 文件名、字节数、SHA-256、时间范围、结构摘要、脱敏事件流

## 6. Service Worker 关键规则

Playwright 的 page.route()/context.route() 可能看不到被 Service Worker 接管的请求。
成熟测试建议在网络 mock 场景可设置 `serviceWorkers: 'block'`，但那会改变现实。
因此：

```text
Reality capture:
  记录现实 Service Worker
  不 block
  用 Trace + CDP + Context 事件补充可见性

Shadow/debug:
  才允许 serviceWorkers='block' 做对照
```

## 7. Actionability 关键规则

对于 `locator.click()`，只看到 DOM 中存在元素不够。
R3 必须同时保存：

```text
EXACTLY_ONE
VISIBLE
STABLE
RECEIVES_EVENTS
ENABLED
```

并保存 action 前、action 时、action 后的 DOM/截图/日志证据。
其中 Stable 的 Playwright 定义是元素 bounding box 至少连续两个 animation frame 保持一致。

## 8. Network idle 规则

`networkidle` 不作为“页面准备好”的权威判断。
Golden Task 必须使用真实业务条件/locator assertion/特定 response 或状态作为 readiness（就绪）门禁。

## 9. R3 产物

每次真实采集新建：
`snapshots/YYYY-MM-DD-r3-browser-<run-id>/`

至少：
- 00-R3-MANIFEST.json
- 01-HOST-BROWSER.json
- 02-CONTEXT-CONFIG-SAFE.json
- 03-AUTH-STORAGE-SAFE.json
- 04-PAGE-GRAPH.json
- 05-DOM-ACTIONABILITY.json
- 06-NETWORK-SAFE.jsonl
- 07-RUNTIME-ERRORS.jsonl
- 08-ARTIFACT-HASHES.json
- 09-GOLDEN-TASK-RESULT.json
- 10-BROWSER-REALITY-ANCHOR-R3.json
- 11-BROWSER-REALITY-FINGERPRINT-V1.json

raw/ 目录仅本机，禁止提交远端。

## 10. 当前状态

R1/R2 host Reality 保持有效，不改旧指纹：
`9bdd4430596e306cf6f8061069659e2680d8a1b66bd69d7bb3e45fe4cfd63dd8`

R3 目前：
```text
BROWSER_R3_COLLECTOR_CONTRACT=FROZEN
BROWSER_R3_REAL_CAPTURE=NOT_YET
BROWSER_R3_FINGERPRINT=NOT_YET
BROWSER_TWIN_INPUT_READY=NO
ENVIRONMENT_99=NOT_YET
```

只有用户机器完成真实 Golden Task R3 采集后，才能生成新的 Browser Reality Fingerprint，并把它交给 exact-reality-digital-twin。
