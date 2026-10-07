# BLIND TRIPLE LAUNCH PACKAGE

STATUS=START_READY_BUT_REQUIRES_THREE_MEMORY_ISOLATED_FRESH_CEO_CONTEXTS
CONTRACT_VERSION=4
STATE_REF=c87bf6a1538eee33fabc5d2cc5208e2d42a90eea
GATE_RESULT=HANDOFF_MECHANICAL_GATE_RESULT_R02.md

Launch exactly three independent fresh CEO contexts:
A=handoffs/TASK_A_FRESH_CEO_02.md
B=handoffs/TASK_B_FRESH_CEO_02.md
C=handoffs/TASK_C_FRESH_CEO_02.md

Each fresh CEO must:
- start with no previous chat memory for this task;
- re-run HANDOFF_MECHANICAL_GATE_SPEC_V2;
- only after PASS record its own TASK_ACCEPTED;
- read only its declared initial evidence slice;
- reject cross-task inputs;
- never receive reviewer capability or future slices.

Current reviewer/orchestrator context MUST NOT execute A/B/C as CEO because it has accessed sealed reviewer-only material during task selection and oracle construction.

HOST_CAPABILITY_NOTE=The current ChatGPT tool surface can write/read GitHub and operate remote terminals, but it does not expose a supported primitive that creates three independent memory-isolated ChatGPT True New Chat sessions and returns their turns to this orchestrator.
