# GPT-Codex simple final v1.5.1 — real execution result

PLAN_BRANCH=codex/gpt-codex-convergence-orchestrator-v1.5.1-flexible-simple-paths
PLAN_PATH=docs/gpt-codex/20260919-simple-final/GPT-CODEX-SIMPLE-FINAL-PLAN-v1.md
METHOD=first-principles-physical-limit-convergence v3.1.1
ARCHITECTURE=PREFERRED_SHARED_WORKSPACE_WITH_SIMPLE_FALLBACKS
PATH_A_REAL=PASS
PATH_B_REAL=PASS
PATH_C_REAL=PASS_CONTROLLED
BUSINESS_VALID=3/3
USER_MIDDLE_COPY_PASTE=0
DUPLICATE_BUSINESS_EFFECT=0
SYSTEM_OR_PROXY_CHANGED=NO
NATURAL_GITHUB_OUTAGE_TESTED=NO
NATURAL_GPT_WRITE_BLOCK_DURING_THIS_RUN=NO
NATURAL_FAILOVER_END_TO_END=UNVERIFIED

## Implementation

C:\AI\GPT-Codex-Convergence-Orchestrator\simple_flow.py implements A/B/C selection and Browser answer handling. The six durable fields are TASK_ID, CURRENT_STEP, ACTIVE_PATH, LAST_GPT_COMMAND_HASH, LAST_RESULT and DONE. The existing github_bus.py, orchestrator.py, codex_executor.py, SQLite ledger and timing events remain in use. GitHub GET transient retry is bounded to one retry. Shared RESULT in B is committed with the existing non-force Git ref update and read-after-write verification. Page blocks are parsed exactly, without using page ACK as business data. The effect is still the reviewed toy WRITE_FILE contract; no general arbitrary-command executor was introduced.

A returned page status GPT_BUS_BLOCKED or GPT_BUS_WRITE_UNAVAILABLE routes to B if the shared REQUEST is readable; if GitHub read fails, it routes to C. B page status GPT_SHARED_READ_UNAVAILABLE routes to C. A compliant page GPT_COMMAND/GPT_DECISION that bypasses Bus write is checked against GitHub and can be accepted on B. The start/resume path verifies or idempotently republishes the same REQUEST before emitting its wakeup. A still prefers the full shared Bus.

The formal Browser entry was C:\AI\Playwright-Native-AI-Browser\skills\playwright-native-ai-browser\scripts\chatgpt-business-entry.js, invoked through the existing playwright_native_ai_browser MCP. Each real page turn used formal query, send and wait_extract; new tasks used new conversations. No new browser identity, profile, transport service, proxy or system setting was created or changed.

## PATH A — default real closed loop

TASK_ID=gpt-codex-simple-final-v1
BUS_BRANCH=bus/gpt-codex-simple-final-v1
FOUR_MESSAGE_TYPES=REQUEST,COMMAND,RESULT,DECISION
FINAL_BUS_HEAD=5efedb2532d3863c66c6980ef0924edb84b72917
RESULT_SHA256=6c26f2350c539e156ca37983864f421d0d8d87e77472ce50634abbac08ef90f7
T0_REQUEST_COMMIT=2026-09-18T18:07:48Z
T1_COMMAND_COMMIT=2026-09-18T18:10:37Z
T2_RESULT_COMMIT=2026-09-18T18:11:35Z
T3_DECISION_COMMIT=2026-09-18T18:13:07Z
T4_STOP=2026-09-18T18:14:01.903046Z
T_REQUEST_TO_COMMAND_SECONDS=169.000
T_COMMAND_TO_RESULT_SECONDS=58.000
T_RESULT_TO_DECISION_SECONDS=92.000
T_FINAL_CONSUME_SECONDS=54.903
T_VALID_SECONDS=373.903
TLS_RECOVERY_WAIT_SECONDS=0
LOCAL_AVOIDABLE_WAIT_SECONDS=0

GPT wrote COMMAND and DECISION directly to GitHub. Codex consumed only remote business messages, wrote the task-local file, checked exact bytes and SHA256, and stopped. A duplicate Codex poll returned effect_written_this_poll=false and result_created_this_poll=false; file mtime did not change.

## PATH B — independent controlled acceptance

TASK_ID=gpt-codex-simple-path-b-v1
ACTIVE_PATH=B
SHARED_TASK_BRANCH=bus/gpt-codex-simple-path-b-v1
SHARED_RESULT_PATH=workspaces/gpt-codex-simple-path-b-v1/simple/RESULT.json
SHARED_RESULT_HEAD=e8ce5a242ddda62db09aa98407f70b837b3f3ab7
PAGE_COMMAND=GPT_COMMAND block
PAGE_DECISION=GPT_DECISION block
RESULT_SHA256=6c26f2350c539e156ca37983864f421d0d8d87e77472ce50634abbac08ef90f7
STOP=2026-09-18T18:21:07.888359Z

The Browser prompt supplied only shared file paths and placeholders for task content and result hash. GPT returned the exact task content in the COMMAND page block and the exact shared result SHA256 in DECISION. Codex extracted both with the formal entry, parsed them without semantic rewriting, verified the effect and returned STOP. The shared RESULT was remotely read back. B was selected for this independent capability test with an explicit test reason; a new natural write failure did not occur during this run.

## PATH C — independent controlled acceptance

TASK_ID=gpt-codex-simple-path-c-v1
ACTIVE_PATH=C
PAGE_COMMAND=GPT_COMMAND block
PAGE_DECISION=GPT_DECISION block
RESULT_SHA256=6c26f2350c539e156ca37983864f421d0d8d87e77472ce50634abbac08ef90f7
STOP=2026-09-18T18:25:44.736579Z

The Browser prompt carried only the current task content; the later decision prompt carried only the verified result. GPT returned both complete page blocks, Codex checked the actual file and SHA256, then stopped. C was tested via an isolated state without disabling GitHub; this proves the page transport and local validation, not a natural GitHub outage.

## Switch and recovery checks

- A write-block status -> B and B shared-read-unavailable status -> C: deterministic route decision checks PASS.
- B -> C persisted state: PASS.
- A restart/resume reuses and verifies the same REQUEST before wakeup: direct check PASS.
- A page business block with no Bus write selects B only after checking shared state: direct check PASS.
- All three final files have exact 25-byte content GPT_CODEX_CODE_TO_CODE_OK and the SHA256 above.
- Earlier failed evidence branches bus/gpt-codex-time-v1-r1 and bus/gpt-codex-time-v2-r1 retain their original HEAD values 45b9092b5bdd6e9bd0ab9acc8edd86d9b6930e09 and 93481d9c418efdabc2337d1b3094d80180266cf1.

## Limits and freeze recommendation

PATHS_TOY_FUNCTIONAL=3/3
DEFAULT_A_TIME_VALID=PASS
NATURAL_A_TO_B_FAILOVER_THIS_RUN=UNVERIFIED
NATURAL_B_TO_C_FAILOVER_THIS_RUN=UNVERIFIED
GENERAL_ARBITRARY_BUSINESS_ACTIONS=OUT_OF_SCOPE_FOR_TOY_EXECUTOR
FINAL_RECOMMENDATION=KEEP_V1_5_1_THREE_SIMPLE_PATHS

The three path transports and the bounded toy business contract are real. The B/C route triggers were controlled tests; no production GitHub outage or current GPT write block was induced. These cases have different start boundaries, so B/C elapsed times are not compared with A T_VALID.

CodeGraph usage: .codegraph absent in the local project; not used.
Knowledge Brain usage: INDEX, ROUTING_MAP and code-reference-index.md checked; no hot index changed.
