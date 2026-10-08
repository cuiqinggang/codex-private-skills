# V27 shared browser stage v1.1.0

Freeze: V27-SHARED-BROWSER-20261009-F01 (2026-10-09)
Authority: ENGINE 27, BRAIN 24; neither upgraded.

Goal: Multiple authorized clients including n8n, Codex and other agents share the original browser. Non-conflicting operations may run concurrently; operations genuinely conflicting on conversation, tab or shared context require resource-scoped coordination. No client monopoly, proxy modification, browser replacement, or real business sending.

Reuse n8n native MCP Client, Remove Duplicates and Wait, Playwright MCP, and existing chatgpt-business-entry.js. Do not implement another scheduler, generic lock, persistence service or sender.

Minimum path: classify target/operation -> detect actual conflict -> coordinate only if needed -> call existing business entry -> read back evidence -> finish or recover. COMMITTED means no retry; NOT_EXECUTED means controlled retry; UNKNOWN means do not retry automatically and do not block unrelated tasks.

Verified evidence: n8n workflow serial tests #23-25; persistent dedup #18-20,#22; Wait restart #21; post-write fault #26 with no-repeat #27; n8n real reversible DOM write #28 concurrently with independent MCP browser_tabs read. No actual sends.

Not verified: inter-client same-resource arbitration, unrelated actual simultaneous writes, fault-release semantics, UNKNOWN end-to-end reconciliation, production Reasonix entry integration.

Time gate: ENGINE 27 requires comparable T_BASE_REAL, T_VIRTUAL_BEST and total-cost delta, including recovery. These are unknown, therefore VIRTUAL_MATURE=NO and STOP_GATE=NOT_PASSED. User deferred further Reality tests.

Stage rule freeze yes; browser collaboration policy v1.1.0; production FINAL_VALID=NO.
