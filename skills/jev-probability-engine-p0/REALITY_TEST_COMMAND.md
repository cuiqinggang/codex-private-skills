# JEV Probability Engine P0 — Reality Test Command

TASK_STEP=3_REALITY_ANCHOR

完整命令包：`jev-probability-engine-p0-v0.2.1-command-pack.zip`
SHA256：`208d816c5372ccb6fec4f4b7055d03774bc2794a875c206518dd274520291ad4`
持久化位置：`ChatGPT Library /AI-Skills/jev-probability-engine-p0-v0.2.1-command-pack.zip`

解压到任意工作目录后，在包根目录执行：

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-reality-anchor.ps1
```

启动器读取 `OPENROUTER_API_KEY`；如果当前进程没有该变量，会现场读取一次。

禁止在现实运行中重新设计 benchmark、修改模型、降低 COMMERCIAL_GATE、调整 run count 或修改 fixture。

只有输出 `COMMERCIAL_GATE_SERIES=PASS`、`T_REAL_STAR_MS=<number>`、`T_P0_MS=<number>`、`REAL_CERTIFIED=YES` 才算现实认证完成。
