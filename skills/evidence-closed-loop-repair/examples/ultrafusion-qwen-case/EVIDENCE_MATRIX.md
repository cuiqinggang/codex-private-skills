# 案例证据矩阵

| 声明 | 阈值 | 需要的证据 | 允许状态 |
|---|---:|---|---|
| Qwen覆盖 | 100% | 全量required报告、关键文件截图 | PASS/FAIL |
| Grok/xAI/格洛克残留 | 0 | 文件名+正文+压缩包递归扫描 | PASS/FAIL |
| 07—09重新装配 | 100% | 派生关系精确比较 | PASS/FAIL |
| 0号/1号一致 | 100% | 逐字节比较 | PASS/FAIL |
| V15.1未修改 | 哈希不变 | SHA-256 | PASS/FAIL |
| 最终ZIP/7z正确 | 100% | 冷启动重解压 | PASS/FAIL/PENDING |
| D层真实质量提升 | 真实测试 | 端到端运行 | PASS/FAIL/PENDING |
