# GPT↔Codex CORE 1 Time Convergence v1 — stopped reality result

STATUS=REALITY_DELTA
CORE_1_TIME_CONVERGENCE=FAIL
ARCHITECTURE_CHANGED=NO
FUNCTIONAL_VALID=0/3
WARM_CLEAN_RUNS_COMPLETED=0
BUS_BRANCH=bus/gpt-codex-time-v1-r1
BUS_HEAD=45b9092b5bdd6e9bd0ab9acc8edd86d9b6930e09
BUS_MESSAGES=000001 REQUEST only
T_VALID_RUNS=UNAVAILABLE
T_VALID_MIN_SECONDS=UNAVAILABLE
T_VALID_P50_SECONDS=UNAVAILABLE
T_VALID_MAX_SECONDS=UNAVAILABLE
FOUR_STAGE_P50=UNAVAILABLE
GPT_WAIT_CLASS=NORMAL
GPT_FIRST_ANSWER_LIMIT_SECONDS=180
GPT_FIRST_ANSWER_SECONDS=UNMEASURED
ANSWER_STARTED=YES
GPT_THINKING_STUCK_COUNT=0 CONFIRMED
GPT_THINKING_STUCK_RECOVERY_SECONDS=UNMEASURED
FINAL_TIME_FREEZE_RECOMMENDATION=NO

## New v1.3.7 rule applied

REQUEST -> COMMAND uses NORMAL, 180 seconds to first visible assistant body. RESULT -> DECISION would use SIMPLE, 60 seconds, but no RESULT was reached.

For r1, the initial Browser send was confirmed at 2026-09-18T16:07:19.316Z, then the page navigated and the formal answer extraction lost its execution context. No 000002 appeared in GitHub after a 480-second same-branch check. The site global history search found no persisted initial marker. A guarded recovery wake reused the same TASK_ID and MESSAGE_SEQ; its send was confirmed at 2026-09-18T16:18:30.700Z and the marker was read back in the canonical conversation. Its first answer onset was not continuously observed; the formal extraction at 2026-09-18T16:24:29.152Z found the answer already complete, so an exact first-answer duration cannot be claimed.

A subsequent formal query confirms ANSWER_STARTED=YES. The assistant answer is page-only ACTION=WRITE_FILE text. A fresh GitHub read confirms 000001.json is the sole queue item and the branch remains at 45b9092b5bdd6e9bd0ab9acc8edd86d9b6930e09. The v1.3.7 first-answer timeout may not refresh after正文 starts. Codex did not treat page text as GitHub COMMAND. r2/r3 were not started.

## Read-only v2 timing correction

The prior producer-supplied envelope created_at values were not actual publish times. GitHub commit timestamps anchor:
T0 REQUEST=2026-09-18T15:24:45Z;
T1 COMMAND=2026-09-18T15:28:28Z;
T2 RESULT=2026-09-18T15:29:52Z;
T3 DECISION=2026-09-18T15:32:31Z;
T4 Codex STOP=2026-09-18T15:35:19.609048Z.

Commit-anchored stages: 223.000, 84.000, 159.000, 168.609 seconds. T_VALID=634.609 seconds. The v2 final interval includes a TLS timeout/recovery; exact TLS start/end were not instrumented. The toy file was created at 2026-09-18T15:29:44.3164826Z, 7.684 seconds before the RESULT commit. The first Browser send was confirmed at 15:25:32.758Z, and the second at 15:31:37.909Z. Pure GPT/model time and Git network time cannot be separated retrospectively from these v2 facts.

## Local CORE 1 changes retained for review

Passive event timing, bounded same-check GET recovery for transient TLS/network errors, immediate expected-message checks, branch-head-triggered checks, task-scoped action IDs, and removal of unnecessary post-DECISION rereads. Four bus message types, GPT/Codex roles, GitHub shared truth, Browser formal entry, SQLite dedupe/resume, read-after-write checks and non-force updates were kept. No timing value is imputed for uncompleted r1/r2/r3.

## Next freeze needed

Resolve the page-only GPT answer versus required direct GitHub COMMAND publication without converting Browser content into business commands. Then rerun three warm clean cases with observed first-answer onset and commit-anchored T0–T3.

CodeGraph usage: .codegraph absent in the local project; CodeGraph not used.
Knowledge Brain usage: INDEX, ROUTING_MAP and code-reference-index.md were read earlier in the project chain; no hot entry changed.
