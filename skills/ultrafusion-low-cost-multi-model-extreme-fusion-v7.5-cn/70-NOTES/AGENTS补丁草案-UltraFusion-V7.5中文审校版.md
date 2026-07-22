# AGENTS.md 补丁草案：UltraFusion V7.5 中文审校版

当任务涉及 `UltraFusion V7.5`、`V7.5 中文审校版`、`V7.0 中文化`、`中文等价复刻`、`半自动ABCD中文审校` 时，优先读取：

```text
${REDACTED_SECRET}
```

执行边界：

- V7.5 是 V7.0 的中文审校版，不替代 V8.0 / V8.2；
- 不覆盖 V7.0 原目录；
- 保留 V15 全量注入、ABCD、Score_0、SCORE_FINAL、Gain、失败复盘；
- 英文协议字段保留，但必须给中文解释；
- 如果只完成中文化、未跑外部模型终验，最终状态为 `REVIEW_READY_CN`。