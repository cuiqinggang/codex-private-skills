# 使用说明

当前版本：1.2.0。

## 读取顺序
1. `SKILL.md`
2. `DUAL-CONTEXT-MODEL.md`
3. `COLLECTION-PROCESS-R1-R2.md`
4. `snapshots/2026-09-21-r2/45-REALITY-ENVIRONMENT-ANCHOR-R2-FINAL.json`
5. `snapshots/2026-09-21-r2/46-REALITY-FINGERPRINT-V3.json`
6. `BROWSER-REALITY-R3.md`
7. `BROWSER-REALITY-R3-CONTRACT.json`
8. `BROWSER-REALITY-R3-ACCEPTANCE.md`

## 状态解释
R1/R2 的 Windows/Codex Reality Anchor 仍然完整有效，且历史指纹不变。
但它不能再代表完整浏览器 E2E Reality。

v1.2.0 新增 Browser Reality R3 采集能力，把以下现实状态纳入锚定：
Browser/Profile/Context/Auth/DOM/actionability/Network/Service Worker/WebSocket/Runtime/Trace/CDP/Golden Task。

当前 Browser R3 只是“采集合同与采集器已冻结”，尚未在用户真实 Golden Task 上运行，所以：
```text
BROWSER_R3_REAL_CAPTURE=NOT_YET
BROWSER_TWIN_INPUT_READY=NO
ENVIRONMENT_99=NOT_YET
```

原始敏感证据只允许本地保存；远端只保存脱敏摘要与 SHA-256。
