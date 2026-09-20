# REALITY CERTIFICATION — v0.3.0

日期：2026-09-21
基准：PE-P0-GENERAL-01
命令包：v0.2.2
模型请求：typesafe/jev-1.13
实际返回模型：typesafe/jev-1.13-20260917

## 认证结果

```text
KEY_AUTH=PASS
HTTP_DECISIONS=PASS
DECISION_SCHEMA=PASS

SWEEP_s1=10/10_PASS
SWEEP_s2=10/10_PASS
SWEEP_s4=10/10_PASS
SWEEP_s8=10/10_PASS

SWEEP_WINNER_SHARDS=2

CONFIRM_s2=30/30_PASS
COMMERCIAL_GATE_SERIES=PASS

T_REAL_STAR_MS=840.6046999999962
T_P0_MS=840.6046999999962
REAL_CERTIFIED=YES
```

## 30 次确认统计

以下统计由用户提供的 30 次确认日志计算：

- MIN = 840.605 ms
- P50 = 907.2285 ms
- P95 = 1014.1072 ms
- MAX = 1192.165 ms
- MEAN = 920.4148 ms
- PASS = 30/30

这些分位数仅用于诊断；唯一优化量仍为通过 COMMERCIAL_GATE 后的最短有效 T_E2E。

## Sweep 现实观察

| topology | min ms | p50 ms | p95 ms | max ms | pass |
|---|---:|---:|---:|---:|---:|
| s1 | 866.845 | 946.8055 | 1029.6251 | 1045.133 | 10/10 |
| s2 | 850.206 | 918.0860 | 1093.6500 | 1110.007 | 10/10 |
| s4 | 908.026 | 930.9810 | 1199.9225 | 1306.132 | 10/10 |
| s8 | 874.781 | 991.4010 | 1528.7858 | 1550.073 | 10/10 |

按冻结规则，Sweep 以最短有效 T_E2E 选择 s2；随后 s2 30/30 确认通过。

## 证据边界

本认证依据是用户在 ChatGPT 会话中贴出的本机 PowerShell 完整运行日志。
日志给出的本机 RESULT.json 路径：
`C:\Users\A\Desktop\jev-probability-engine-p0-v0.2.2-command-pack\jev-probability-engine-p0-v0.2.2-command-pack\reality-test\results\RESULT.json`

本次未通过连接器直接读取该本地 RESULT.json，因此本文件不声称对该本地文件内容做了独立远端回读；认证数值严格来自用户提供的控制台日志。

## 历史纠偏

v0.2.1 的 correctness 结果因 Choice response parser bug 作废；它只保留为 connectivity evidence。
v0.2.2 修复 parser，当前现实结果证明：
- 当前 Key/API/model path 可用；
- Choice schema 可正确解析；
- 1/2/4/8 shard 均能通过固定 COMMERCIAL_GATE；
- s2 在本次固定环境下产生最低有效实测；
- 完整 P0 现实认证通过。
