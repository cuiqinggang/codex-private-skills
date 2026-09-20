# 更新协议

1. 先区分 TARGET 与 COLLECTOR。
2. 历史只追加，R1/R2/R3 永不覆盖。
3. 动态行为以 TARGET/实际浏览器运行时为权威。
4. 秘密原文只允许本机 raw；远端只保存脱敏元数据与 SHA-256。
5. Host/Codex 继续沿用 R1/R2 的最终锚点和 V3 指纹。
6. 浏览器任务必须新建 Browser R3 快照，不能用 R2 的“网络非阻断”替代浏览器网络事实。
7. Browser R3 必须分离 GOLDEN_TIMING_RUN 与 GOLDEN_OBSERVABILITY_RUN，禁止把重观测开销写进极限时间。
8. Browser Reality 禁止通过改 proxy/network/profile/cookie/service-worker/cache/route/mock/DOM 来“改善采集”。
9. 对 Golden Task 采集 Browser/Profile/Context/Auth/DOM/actionability/Network/Service Worker/WebSocket/Runtime/Trace/CDP。
10. 同一 Golden Task 关键语义必须现实复现 3/3。
11. 只有 Browser R3 关键未知归零、秘密远端零明文、观测无扰动并生成新指纹后，才能置 `BROWSER_TWIN_INPUT_READY=YES`。
12. PASS/PARTIAL/FAIL 均可追加归档，但版本状态必须真实。
