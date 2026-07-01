# Time Gate Matrix Template

| Task mode | Required field | Required value | Evidence path | Verification result |
|---|---|---|---|---|
| ENDURANCE_VALIDATION | minimum_elapsed_minutes | >= 120 or >= 480 | | |
| ENDURANCE_VALIDATION | checkpoint_count | >= required minimum | | |
| PRODUCTION_WITH_TIME_BUDGET | time_budget_minutes | declared | | |
| PRODUCTION_WITH_TIME_BUDGET | finish_when_all_gates_pass | true | | |
| PRODUCTION_WITH_TIME_BUDGET | no_forced_waiting | true | | |
