# 现实执行环境精确数字孪生唯一版 v1.1.0

机器名：`exact-reality-digital-twin`

唯一目标：**先重放现实，再在 Shadow（影子）中试验。**
Reality（现实）不可修改；Shadow 不得冒充 Reality。

## 双层 Reality 输入

### 1. Host / Codex 现实（已完成）
来源：`reality-execution-environment-anchor@1.2.0` 的历史 R1/R2。
Reality Fingerprint V3：
`9bdd4430596e306cf6f8061069659e2680d8a1b66bd69d7bb3e45fe4cfd63dd8`

已冻结现实行为：
```text
SetTokenInformation
-> error 1344
-> 3/3
-> child not running
-> PATH NOT_REACHED
-> no running child token
```

旧合同自测：24/24 PASS。

### 2. Browser E2E 现实（新增合同，尚未真实采集）
v1.1.0 正式加入 Browser Reality R3 输入合同：
`BROWSER-TWIN-INPUT-CONTRACT.md`

它要求真实采集并重放：
Browser/Profile/Context/Auth/DOM/actionability/Network/Service Worker/WebSocket/Runtime/Trace/CDP/Golden Task。

当前：
```text
BROWSER_R3_REALITY_INPUT=NOT_YET
BROWSER_GOLDEN_REPLAY=NOT_YET
BROWSER_REALITY_TWIN_DELTA=NOT_YET
BROWSER_SHADOW_RUN=NOT_YET
ENVIRONMENT_99=NOT_YET
```

因此，v1.1.0 已修正“同一台电脑 = 完整浏览器环境”的旧理解。
在 Browser R3 真实指纹产生之前，本 Twin 禁止声称已完成完整浏览器数字孪生。
