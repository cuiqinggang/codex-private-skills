# Maintenance Runtime Gate

All maintenance runs must provide runtime evidence before PASS.

## Minimum Runtime

| Task | Minimum elapsed minutes | Minimum checkpoints |
| --- | ---: | ---: |
| Weekly 30min light check | 30 | 3 |
| Monthly 2h sample optimization | 120 | 8 |
| Quarterly 4h graph governance | 240 | 16 |
| Post-project 30min retrospective | 30 | 3 |
| Semiannual or annual 8h reorganization | 480 | 32 |

## Required Evidence

- `started_at`
- `ended_at`
- `elapsed_minutes`
- checkpoint list
- final checkpoint
- checkpoint timeline
- reviewed scope
- final status
- explicit `formal_skills_modified` value

## Hard Rule

If `elapsed_minutes` is below the required minimum, the run must be FAIL or PARTIAL. It cannot be PASS.

