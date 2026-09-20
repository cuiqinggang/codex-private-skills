# CHANGELOG

## 0.3.0 — 2026-09-21

Reality certified:
- OpenRouter Key/API/model path PASS.
- Decision schema PASS.
- s1/s2/s4/s8 sweep 全部 10/10 PASS.
- sweep winner = s2.
- s2 confirmation = 30/30 PASS.
- COMMERCIAL_GATE_SERIES=PASS.
- T_REAL*=840.6046999999962 ms.
- T_P0=840.6046999999962 ms.
- REAL_CERTIFIED=YES.

Diagnostics:
- confirmation P50=907.2285 ms.
- P95=1014.1072 ms.
- MAX=1192.165 ms.

Evidence boundary:
- certification values derive from the user's posted PowerShell transcript.
- local RESULT.json path was reported by the runner but was not independently fetched by the connector.

## 0.2.1 — 2026-09-21

Added:
- Reality Anchor / Real P0 完整现实测试命令包。
- 一条 PowerShell 启动命令。
- OpenRouter Decisions 直连测试器。
- 1/2/4/8 shard 拓扑扫描。
- 30-run 最快拓扑确认。
- action receipt、依赖解锁、private-oracle verifier、RESULT.json。
- static virtual gate 与 offline full-chain mock gate。

Unchanged:
- PE-P0-GENERAL-01。
- COMMERCIAL_GATE。
- T0/T1。
- MODEL_BARRIER_DEPTH_MIN=1。
- ACTION_DEPENDENCY_DEPTH_MIN=2。
- Core② v0.2.0 architecture。

Reality:
COMMAND_VIRTUAL_FREEZE=PASS
OFFLINE_MOCK_E2E=PASS
T_REAL*=NOT_MEASURED
T_P0=NOT_MEASURED
REAL_CERTIFIED=NO

## 0.2.0 — 2026-09-21
Core② mature-cluster + Virtual-99 structural freeze.

## 0.1.0 — 2026-09-21
Initial Step-1 structural physical-limit freeze.
