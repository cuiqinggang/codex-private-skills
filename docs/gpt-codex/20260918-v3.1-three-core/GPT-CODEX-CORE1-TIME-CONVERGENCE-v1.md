# GPT↔Codex CORE 1 Time Convergence v1.3.8 — stopped reality result

STATUS=REALITY_DELTA
CORE_1_TIME_CONVERGENCE=FAIL
ARCHITECTURE_CHANGED=NO
WARM_RUNS=3 PLANNED
FUNCTIONAL_VALID=0/3
T_VALID_RUNS=UNAVAILABLE
T_VALID_MIN_SECONDS=UNAVAILABLE
T_VALID_P50_SECONDS=UNAVAILABLE
T_VALID_MAX_SECONDS=UNAVAILABLE
P50_REQUEST_TO_COMMAND_SECONDS=UNAVAILABLE
P50_COMMAND_TO_RESULT_SECONDS=UNAVAILABLE
P50_RESULT_TO_DECISION_SECONDS=UNAVAILABLE
P50_FINAL_CONSUME_SECONDS=UNAVAILABLE
P50_TLS_RECOVERY_WAIT_SECONDS=UNAVAILABLE
P50_LOCAL_AVOIDABLE_WAIT_SECONDS=UNAVAILABLE
GPT_WAIT_CLASS=NORMAL
GPT_FIRST_ANSWER_LIMIT_SECONDS=180
GPT_FIRST_ANSWER_SECONDS=AT_MOST_157.107_ON_RECOVERY_WAKE
ANSWER_STARTED=YES_ON_RECOVERY_WAKE
GPT_BUS_ACTION_STATUS=BLOCKED
GPT_BUS_PROTOCOL_RETRY_COUNT=0
GPT_THINKING_STUCK_COUNT=1
GPT_THINKING_STUCK_RECOVERY_SECONDS=106.237
DUPLICATE_BUSINESS_EFFECT=0
FINAL_TIME_FREEZE_RECOMMENDATION=NO

## Frozen architecture and stop condition

The original failed gpt-codex-time-v1-r1 Bus branch remains untouched. New r1 is bus/gpt-codex-time-v2-r1 at 93481d9c418efdabc2337d1b3094d80180266cf1. Only 000001 REQUEST exists. GPT did not publish 000002 COMMAND. No local toy effect was executed. New r2/r3 branches do not exist.

The v1.3.8 self-contained GPT_BUS_WAKEUP_V1 included TASK_ID, REPOSITORY, BUS_BRANCH, MESSAGE_SEQ, MESSAGE_PATH, EXPECTED_GPT_BUS_REPLY_TYPE=COMMAND, REQUIRED_ACTION=WRITE_NEXT_BUS_MESSAGE_TO_GITHUB and LOGICAL_EVENT_ID. It explicitly required the current ChatGPT session's GitHub write action and permitted only GPT_BUS_COMMIT_OK, GPT_BUS_WRITE_UNAVAILABLE or GPT_BUS_BLOCKED as page status. First wakeup was confirmed sent at 2026-09-18T16:50:45.389Z. The assistant remained at “正在思考” with no business body after the NORMAL 180-second limit. GitHub had no COMMAND. The same browser profile was refreshed; the prior transient conversation URL redirected to ChatGPT root, and the formal query found no marker there. The same wakeup, TASK_ID, MESSAGE_SEQ and logical_event_id was confirmed sent again in a new conversation at 2026-09-18T16:56:09.483Z.

On recovery wake, the formal Browser query observed completed page text: GPT_BUS_BLOCKED TASK_ID=gpt-codex-time-v2-r1 REASON=GITHUB_WRITE_SAFETY_CHECK. Formal wait_extract independently returned COMPLETE_EXTRACTED with the identical 77-character text, no stop control and a ready copy control. A fresh GitHub Bus check still found only 000001 REQUEST and unchanged remote head. The frozen BLOCKED branch mandates immediate STOP + REALITY_DELTA, without a protocol retry or r2/r3. The page text was never treated as a business COMMAND.

The second answer onset was not continuously instrumented; 157.107 seconds is the conservative elapsed upper bound from second send confirmation to our first persisted observation. The first wake had no answer before recovery. A 1-second-precision exact onset must not be inferred from the later wait_extract firstObservedAtEpochMs, which began after the answer was already complete. GPT_THINKING_STUCK_RECOVERY_SECONDS is from persisted stuck detection at 16:54:23.246439Z to confirmed recovery send at 16:56:09.483Z. First send to detection was 217.857 seconds, including tool scheduling; the last formal query before recovery still showed only “正在思考”.

## Time attribution carried forward

Read-only real-case-v2 GitHub commit times anchor T0=15:24:45Z, T1=15:28:28Z, T2=15:29:52Z, T3=15:32:31Z, and T4 local STOP=15:35:19.609048Z on 2026-09-18. The commit-anchored stages are 223.000, 84.000, 159.000 and 168.609 seconds, with T_VALID=634.609 seconds. Earlier envelope created_at calculations were not publish times.

Available old boundaries: request_publish=T0; command_remote_visible=T1; result_publish=T2; decision_remote_visible=T3; stop=T4. Browser wakes were confirmed at 15:25:32.758Z and 15:31:37.909Z. The toy file write was observed at 15:29:44.3164826Z, 7.684 seconds before RESULT commit. An earlier final-consume TLS timeout occurred, but its exact error start/end were not instrumented. Browser-ready, consumed, effect-start/end and pure GPT time cannot be recovered retrospectively. Therefore EXTERNAL_GPT_BROWSER_TIME, GIT_NETWORK_TIME, TLS_RECOVERY_WAIT and FINAL_POST_DECISION_WAIT for v2 are only partially attributable; no fabricated substage values are used.

For new r1, request_publish=2026-09-18T16:47:42.234660Z; browser_wake_start=16:49:48.666825Z; browser_wake_ready local mark=16:51:16.818887Z. Its local Git API instrumentation recorded 32 calls totalling 44.917 seconds and 0 recorded local poll seconds before STOP. COMMAND, effect, RESULT, DECISION and T_VALID were never reached. A Browser write capability safety check was the terminal blocker, not a local poll/backoff bottleneck.

## Scope and evidence

ACTUAL_ENTRYPOINT=C:\AI\Playwright-Native-AI-Browser\skills\playwright-native-ai-browser\scripts\chatgpt-business-entry.js
FORMAL_FLOW_REUSED=YES
FORMAL_BUSINESS_ENTRYPOINT=VERIFIED

Local code changes were limited to the v1.3.8 self-contained wakeup template and source branch in config. The prior passive timing, immediate expected-message check, bounded transient GET recovery, task-scoped IDs and immediate post-DECISION stop remain. The four-message role/type rules, GitHub shared truth, Browser stack, SQLite dedupe/resume and read-after-write checks were not changed.

CodeGraph usage: .codegraph absent in local project; no graph analysis required.
Knowledge Brain usage: INDEX, ROUTING_MAP and code-reference-index.md checked; no hot entry changed.

NEXT_FROZEN_DECISION_REQUIRED=Resolve current ChatGPT GitHub write safety check or supply a permitted GitHub write action within the existing GPT role. Do not convert Browser page text into a Codex COMMAND.
