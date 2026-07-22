# SOP: Three-Round Screenshot Acceptance

Date: 2026-07-02
Status: ACTIVE

## Purpose

Make durable Codex outputs trustworthy by verifying that they exist, run in a realistic path, and can be retested or recovered. The result is only complete when the verification record and screenshots support the conclusion.

## When To Use

Use this SOP when a task writes final material into a skill package, knowledge base, material library, command package, project delivery package, deployment package, recovery package, test package, automation script, or default rule.

## Steps

1. Identify the durable artifact and final write location.
2. Prepare an acceptance record using `templates/THREE-ROUND-SCREENSHOT-ACCEPTANCE-RECORD.md`.
3. Round 1: open the artifact, list it in its directory, or run the simplest valid command.
4. Capture a screenshot for Round 1.
5. Round 2: perform a realistic invocation, such as running a script, opening the generated page, searching the new trigger phrase, or using the artifact from its intended entry point.
6. Capture a screenshot for Round 2.
7. Round 3: retest after repair, verify a boundary case, or confirm recovery by reopening or reinvoking the artifact from a clean command.
8. Capture a screenshot for Round 3.
9. If any round fails, record the failure, repair it, and rerun the failed round.
10. Write the final conclusion:
   - FINAL_PASS only when all three rounds pass and screenshot paths are recorded.
   - PARTIAL when the output exists but full verification is missing.
   - FAIL when the output cannot be verified.

## Minimum Evidence Bundle

- acceptance record
- three screenshot files
- command or test output log when available
- repair notes when any failure occurred

## Final Answer Rule

For applicable tasks, the final answer must state whether the artifact reached FINAL_PASS, PARTIAL, or FAIL. If screenshots were not captured, say so plainly and do not claim FINAL_PASS.

