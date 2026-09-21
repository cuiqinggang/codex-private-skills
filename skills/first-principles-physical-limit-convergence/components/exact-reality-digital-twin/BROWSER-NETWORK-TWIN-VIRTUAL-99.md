# Browser + Network Twin Fusion Virtual-99 v1

状态：**VIRTUAL_MATURITY=PASS**
引擎：`exact-reality-digital-twin@1.2.0`
归属：第三核心「高智能虚拟成熟」

## 1. 本轮解决的问题

v1.1.0 只把 Browser Reality R3 写入外围合同，但 `ENGINE.py` 仍是 v1.0.0 的 1344 单点重放器。
v1.2.0 正式把 Host、Browser、Network、Runtime、DOM actionability、Golden Task、Reality/Twin Diff、Shadow 与时间指标融合到同一个确定性引擎。

这不是文件拼接。统一执行链被冻结为：

```text
Host R2 + Host Network
        +
Browser Environment / Profile / Auth
        +
Page / Frame / Worker / Service Worker
        +
Browser Network / WebSocket / TLS evidence
        +
Runtime / Console / Exception / Dialog
        +
DOM / Overlay / Animation / Actionability
        +
Golden Task
        ↓
Unified Twin State
        ↓
Causal Timeline
        ↓
Semantic Signature
        ↓
3/3 Stability Gate
        ↓
Reality Replay
        ↓
Reality/Twin Diff
        ↓
T_VALID
        ↓
Shadow Overlay
```

## 2. 不允许虚构现实数据

当前真实 Browser R3 数据仍不完整。

已知：
- Host R2 Reality：READY。
- Host R2 Fingerprint：
  `9bdd4430596e306cf6f8061069659e2680d8a1b66bd69d7bb3e45fe4cfd63dd8`
- 宿主网络采集器已产生本机证据。
- Browser Attach 控制通道当前阻断。
- BrowserContext / Page / Profile / #dialog actionability / Trace / CDP / DOMSnapshot / Golden Task 真实数据：UNKNOWN。

因此 v1.2.0 的规则是：

```text
缺数据 -> UNKNOWN
UNKNOWN -> 现实重放门禁 FAIL
禁止 GPT/Engine 自动补值
```

## 3. 统一状态模型

每个 Browser Reality run 必须转换为同一状态：

- `host`：R2 指纹 + 宿主网络安全镜像
- `browser`：环境/Profile/Auth/Frame/Service Worker/actionability
- `network`：request/response/failure/WebSocket 等摘要
- `runtime`：console/pageerror/exception/crash/dialog
- `timeline`：Playwright + CDP 统一时间序列
- `golden_task`：真实 outcome + 真实 duration
- `module_presence`：关键模块存在性
- `critical_unknowns`：任何未观测关键状态
- `state_fingerprint`：确定性状态哈希

## 4. actionability 语义

Twin 不把“元素在 DOM 中”等同于“可点击”。

冻结分类：
- ELEMENT_NOT_FOUND
- STRICTNESS_MULTIPLE_ELEMENTS
- NOT_VISIBLE
- UNSTABLE
- EVENT_INTERCEPTED
- DISABLED
- ACTIONABLE
- UNKNOWN_ACTIONABILITY

`#dialog` 或等价目标必须进入这一套确定性判定。

## 5. 网络不是旁路模块

Browser network、DOM、Runtime 与 actionability 必须在同一时间轴。

例如现实可以表现为：

```text
response 延迟
-> JS state 未更新
-> overlay 未消失
-> receives_events=false
-> click 等待/timeout
```

Twin 必须保存这种因果顺序，而不是只保存一个 HAR 文件。

## 6. Golden Task 与 T_VALID

冻结现实性能合同：

1. 预声明三个真实计时运行：T1 / T2 / T3。
2. 三次必须同一合同、同一 Golden Task、关键语义 3/3 一致。
3. 另有预声明 O1 可观测运行，用于 Trace/CDP/DOMSnapshot/因果证据。
4. O1 绝不代替失败的 T1/T2/T3，也不参与性能排名。
5. 所有 Reality、质量、安全、秘密、未知门禁通过后：

```text
T_VALID = min(T1, T2, T3)
```

三次计时总和只叫 `certification_evidence_time_ms`，不是优化指标。

## 7. Reality/Twin Diff

只有以下全部成立才允许现实 Twin READY：

```text
BROWSER_CRITICAL_UNKNOWN_COUNT=0
GOLDEN_TASK_REALITY_REPRODUCED=3_OF_3
TWIN_REPLAY=PASS
REALITY_TWIN_DELTA_COUNT=0
OBSERVATION_PERTURBATION=NO
SECRET_PLAINTEXT_ZERO_REMOTE=PASS
BROWSER_R3_FINGERPRINT_CREATED=YES
```

## 8. Shadow

Shadow 只能覆盖 Twin 副本：
- Reality 指纹前后必须一致。
- Shadow delta 必须显式。
- Shadow 结果禁止写回 Reality。

## 9. Virtual-99 结果

引擎确定性虚拟夹具测试：
```text
SELFTEST=33/33 PASS
```

覆盖：
- 6 类 actionability 失败 + ACTIONABLE
- 3/3 稳定性
- 未知值阻断
- Host 指纹漂移阻断
- 网络失败计数
- Runtime exception/dialog
- Reality/Twin Delta=0
- Shadow 隔离
- T_VALID=min(3 runs)
- 确定性 fusion fingerprint

虚拟 replay benchmark：
```text
REPEATS=5000
P50≈0.007 ms
P95≈0.008 ms
```

该 benchmark 只证明 Twin 本地重放器开销很小，不是用户真实浏览器 T_VALID，不作为现实认证数据。

## 10. 当前冻结状态

```text
VIRTUAL_MATURITY=PASS
UNIFIED_TWIN_ENGINE=FROZEN
VIRTUAL_SELFTEST=33/33 PASS
TIME_CONTRACT=FROZEN

REAL_BROWSER_ATTACH=BLOCKED
REAL_BROWSER_R3_INPUT=INCOMPLETE
BROWSER_TWIN_INPUT_READY=NO
FULL_BROWSER_TWIN=NO
ENVIRONMENT_99=NOT_YET
```

下一现实动作不是重新设计 Twin，而是只执行已经冻结的 Attach-first 现实输入采集与重放验证。
