# Performance Ladder

| Stage | Name | 初始状态 | 解锁条件 |
|---|---|---|---|
| P0 | ComfyUI Control | `READY_TO_MEASURE` | v1.0.0 工具与合同通过 |
| P1 | Minimal AI Image | `LOCKED_BY_PREVIOUS_STAGE` | P0=99 + FREEZE |
| P2 | Base Image | `LOCKED_BY_PREVIOUS_STAGE` | P1=99 + FREEZE |
| P3 | Added Components / LoRA | `LOCKED_BY_PREVIOUS_STAGE` | P2=99 + FREEZE |
| P4 | Advanced Image | `LOCKED_BY_PREVIOUS_STAGE` | P3=99 + FREEZE |
| P5 | Minimal Video | `LOCKED_BY_PREVIOUS_STAGE` | P4=99 + FREEZE |
| P6 | Production Video / Wan | `LOCKED_BY_PREVIOUS_STAGE` | P5=99 + FREEZE |
| P7 | Minimal H3 | `LOCKED_BY_PREVIOUS_STAGE` | P6=99 + FREEZE |
| P8 | Production H3 | `LOCKED_BY_PREVIOUS_STAGE` | P7=99 + FREEZE |

每一层必须完成固定 TASK、四列、真实计时、有效性门禁、99 裁决、冻结清单与回退路径。新增能力统一记录：

`ΔT_STAGE = T_NEW_STAGE - T_PREVIOUS_STAGE`

若新增有限能力却导致数量级时间崩塌，结论优先为 `PATH_ARCHITECTURE_ERROR`，不得以新阶段更复杂为理由直接接受。
