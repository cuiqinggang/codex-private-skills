# HANDOFF MECHANICAL GATE v2

CONTRACT_VERSION=4
STATUS=CURRENT
SUPERSEDES=HANDOFF_MECHANICAL_GATE_SPEC.md
METHOD_CHANGE=NO
PURPOSE=Add exact NEW_PAGE_TEMPLATE17 conformance checks missed by R01.

## Required checks

### A. Template-17 structural conformance
1. First line is `冻结标签=<TASK_SHORT>-FNNN`.
2. The next three lines contain, in order:
   - four-field location anchor `【页面名｜任务名｜序号｜虚/实】`;
   - 状态机 anchor with explicit Engine/Brain/Template Chinese names and versions;
   - 时间锚 with task-acceptance/current-state/T_VALID/T* values and no N/A.
3. Same-task continuation read order is exactly:
   BRAIN.md@METHOD_REF
   → TASK_CONSTRAINTS_PATH@STATE_REF
   → FREEZE_PATH@STATE_REF
   → NEW_PAGE_TEMPLATE.md@METHOD_REF.
4. ENGINE.md is not inserted as an independent mandatory read step; it remains BRAIN internal.
5. Body remains minimal: paths/versions/read order/task one-liner/next-step one-liner plus only machine fields needed by Contract V4. No copied method rules or old-chat narrative.

### B. Contract V4 mechanical fields
6. TASK_ID correct.
7. CONTRACT_VERSION=4.
8. FREEZE_VERSION correct.
9. ENGINE_VERSION=22.
10. BRAIN_VERSION=19.
11. NEW_PAGE_TEMPLATE_VERSION=17.
12. METHOD_REF resolves to the three declared method versions.
13. STATE_REF resolves.
14. TASK_CONSTRAINTS_PATH exists at STATE_REF.
15. FREEZE_PATH exists at STATE_REF.
16. Freeze label/tag and path version agree.
17. NEXT_NODE exists in the same TASK Freeze.
18. EXECUTION_PACKAGE exists at STATE_REF and has same TASK_ID.
19. CHRONOLOGICAL_GATE_PATH exists at STATE_REF.
20. INITIAL_EVIDENCE_PATH exists at STATE_REF and same TASK_ID.
21. RESOURCE_LEASE_STATE_PATH exists at STATE_REF.
22. No foreign TASK path/ID in prompt.
23. No stale Freeze.
24. No old-chat noise.
25. Fresh CEO can recover from prompt + declared authority files only.
26. Oracle/capability SHA absent.
27. Future slice/final answer path absent.
28. Public answer search disabled by referenced contract/execution package.
29. NEW_CEO_MEMORY=NO_PREVIOUS_CHAT_MEMORY.

FAIL semantics:
Any failed item => HANDOFF=FAIL. Do not continue by model memory.
Repair handoff/task validator only unless evidence proves TEMPLATE17 itself is insufficient or contradictory.
