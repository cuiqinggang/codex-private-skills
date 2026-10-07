# TASK C EXECUTION PACKAGE

TASK_ID=BLIND-C-WEBARENA-VERIFIED-552
CONTRACT_VERSION=4
ROLE=EXECUTION_SIDE
BENCHMARK_PIN=ServiceNow/webarena-verified@6473f72db5dcefc97b5725b59e734504edc28a21
TASK_NUMBER=552
ORACLE_ACCESS=DENIED
DATASET_EVAL_FIELD_ACCESS=DENIED

## Agent-visible intent

Use the Web IDE to create a folder named `real_space` in the `gimmiethat.space` repository. Within it, create `urls.json` containing the full URLs of the 5 most recent posts from the `space` forum on the discussion forum as a JSON object with a `urls` array, newest to oldest. Commit the changes to the default branch.

## Systems

- Reddit-like discussion forum sandbox；
- GitLab sandbox；
- Browser session；
- environment-control health/state；
- local output staging for agent response + HAR/network trace；
- official offline evaluator runs Reviewer-side only.

## Hard requirements

1. Browser is primary task interaction path.
2. Read current forum state; do not assume cached post order.
3. Before mutation, read GitLab target state and default branch.
4. Create valid JSON and validate locally before submit.
5. Commit is exactly-once: if client acknowledgment is ambiguous, read server state before any retry.
6. Capture final HAR/network trace and agent response artifact.
7. Reviewer runs deterministic evaluator; execution side sees only PASS/FAIL/DELTA.
8. Session loss/env fault must recover without duplicate submit.
9. Cross-task prompt/state/path candidates must be REJECT.
10. No access to original benchmark row's eval/expected fields or public mirrors that reveal them.

## Sandbox network gate

Allow only configured local WebArena site URLs and environment-control endpoints required by this TASK.
Deny general public internet during execution.
Deny repository/dataset source containing task 552 reference answer.

## Initial NEXT_NODE

C01=VERIFY_SANDBOX_HEALTH_WITHOUT_RESETTING_OTHER_TASKS
