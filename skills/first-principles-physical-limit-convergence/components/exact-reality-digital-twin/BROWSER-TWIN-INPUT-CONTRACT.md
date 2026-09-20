# Browser Twin 输入合同 v1.1.0

唯一 Twin：`exact-reality-digital-twin`

## 输入来源
浏览器现实输入只能来自：
`reality-execution-environment-anchor@1.2.0 / Browser Reality R3`

不得从推测、另一台机器、普通 mock、逻辑 Virtual-99 或“同一台电脑”假设生成。

## 必需输入
只有当 R3 给出：
```text
BROWSER_CRITICAL_UNKNOWN_COUNT=0
BROWSER_EXECUTION_RELEVANT_STATE_COMPLETE=YES
GOLDEN_TASK_REALITY_REPRODUCED=3_OF_3
SECRET_PLAINTEXT_ZERO_REMOTE=PASS
OBSERVATION_PERTURBATION=NO
BROWSER_R3_FINGERPRINT_CREATED=YES
BROWSER_TWIN_INPUT_READY=YES
```
才允许建立 Browser Reality Mode。

输入至少包括：
- Node / Playwright / Browser 版本与可执行文件指纹
- launch/context 实际配置
- Profile/userDataDir 安全指纹
- Cookie/LocalStorage/IndexedDB/SessionStorage/OPFS 结构与登录态判据
- Page/Frame/Worker/Service Worker 图
- DOM / layout / overlay / animation
- 目标 locator actionability
- HTTP(S) 请求响应、redirect、timing、cache/service-worker 来源、TLS
- WebSocket 等长连接
- console / pageerror / crash / dialog / lifecycle
- Trace/CDP/DOMSnapshot 证据哈希
- Golden Task 3/3 现实结果

## Reality / Shadow 边界
Reality Mode：
- 只重放 R3 已观测事实。
- 禁止修改 serviceWorkers、proxy、network、cache、DOM、storage、route。
- 未采集字段必须保持 UNKNOWN，不得自动填值。

Shadow Mode：
- 可对 Reality 的副本做假设改变。
- 每个改变必须显示与 Reality 的 delta。
- Shadow 结果永远不得回写为 Reality。

## 浏览器 Twin 的最低能力
1. 能按同一动作顺序重放 Golden Task。
2. 能在关键 action 前后重建 actionability 状态。
3. 能关联导致 actionability 的 DOM/overlay/animation 与网络/远端响应时间线。
4. 能区别：
   - 元素不存在
   - 多元素 strictness
   - 不可见
   - 不稳定
   - 被 overlay 截获
   - disabled
   - JS dialog 阻塞
   - page/frame navigation
   - request/network failure
   - service worker 路径
   - runtime exception/crash
5. Reality/Twin 差异必须显式，不允许“合理猜测”。

## 当前状态
```text
LEGACY_WIN1344_REALITY_INPUT=READY
LEGACY_WIN1344_CONTRACT_SELFTEST=24/24 PASS

BROWSER_R3_REALITY_INPUT=NOT_YET
BROWSER_GOLDEN_REPLAY=NOT_YET
BROWSER_REALITY_TWIN_DELTA=NOT_YET
BROWSER_SHADOW_RUN=NOT_YET
ENVIRONMENT_99=NOT_YET
```

因此 v1.1.0 是“浏览器合同已纳入唯一 Twin”，不是“浏览器 Twin 已现实认证”。
