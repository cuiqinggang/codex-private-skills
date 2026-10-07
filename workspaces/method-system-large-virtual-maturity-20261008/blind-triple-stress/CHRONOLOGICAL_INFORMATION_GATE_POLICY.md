# CHRONOLOGICAL INFORMATION GATE — EXECUTION POLICY

CONTRACT_VERSION=4
EXECUTION_VISIBLE=YES
REVIEWER_SCHEDULE_POINTER=ABSENT

For all A/B/C:
1. Only the currently released slice may be used.
2. Future logs, final outputs, later root-cause summaries, final diffs/reference answers are unavailable.
3. Executor may request NEXT_EVIDENCE only by stating what unknown blocks the next decision and why existing evidence is insufficient.
4. Reviewer response is limited to PASS / FAIL / DELTA / 缺少证据 / 结果不一致 or release of the next historically/legal slice.
5. Reviewer never supplies the correct repair or final answer.
6. A release request can be denied if it would skip chronology.
7. Deterministic stress conditions may exist, but there is no fixed failure count and no pre-scripted repair.
8. WALL_CLOCK may be compressed; decision/evidence/repair/freeze/handoff logic may not be compressed.

Initial released slices:
- A: evidence/task-a/A_T0.md
- B: evidence/task-b/B_T0.md
- C: evidence/task-c/C_T0.md
