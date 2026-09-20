# Reality Test Command Virtual Freeze — v0.2.1

Date: 2026-09-21

COMMAND_VIRTUAL_FREEZE=PASS
OFFLINE_MOCK_E2E=PASS
INPUT_ITEMS=24
MODEL_BARRIER_DEPTH_MIN=1
ACTION_DEPENDENCY_DEPTH_MIN=2
TOPOLOGY_SWEEP=1,2,4,8_SHARDS
CONFIRM_RUNS=30
EMBEDDED_KEY=NO

离线 mock 已实际跑通：

request construction → sharding → answer merge → wave-1 actions → local receipt files → per-dependency unlock → dependent actions → disk readback → private-oracle verifier → manifest → RESULT.json。

Mock 时间不允许写入 T_REAL* 或 T_P0。

REAL_API_RUN=NOT_RUN
T_REAL*=NOT_MEASURED
T_P0=NOT_MEASURED
REAL_CERTIFIED=NO
