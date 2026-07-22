# Rule Patch: GPT—Codex Role Separation

For complex projects, never use “GPT reviewed it” as an ambiguous completion claim.

Required declarations:

- `PRIMARY_CONTROLLER`: `CODEX` or `CHATGPT_WORK`
- `MODEL_ROLE`: `GPT_REASONING_INSIDE_CONTROLLER`
- `REVIEW_MODE`: `INDEPENDENT_AGENT`, `SELF_REVIEW_FALLBACK`, or `CHATGPT_WORK_EXTERNAL_REVIEW`
- `REVIEWER`: actual reviewer identity
- `STATUS`: `PASS`, `REVIEW_READY`, `PARTIAL`, or `BLOCKED`

Rules:

1. GPT performs reasoning inside the selected controller; it is not automatically a separate reviewer.
2. Codex is the default controller when work must land in repositories, local files, terminals, tests, Git, or system tooling.
3. When multi-agent support is available and independent review is requested, create a separate review agent with read-only-first scope.
4. Main-agent self-check must not be described as independent review.
5. ChatGPT Work is an optional external surface, not an implicit Codex subagent. Use a written handoff package when switching surfaces.
6. P0/P1 findings block delivery until closed and reverified. Any open P2 blocks `PASS`; use `PARTIAL` or `REVIEW_READY`.
7. Cross-surface handoff requires data classification, redaction, secrets/PII scan, actual-attachment list, access/plugin check, data-control check, and user approval for sensitive transfer.

Trigger phrases: `完整项目处理`, `GPT和Codex分工`, `哪个负责审核`, `独立审核`, `如何交接`, `如何转换`, `ChatGPT工作和Codex协作`.

Preflight action: read `references/GPT-CODEX-ROLE-TRANSFER-PROTOCOL-20260710.md` before planning.

Failure-review entry: if a run ambiguously claims a GPT review, record the incident as `AMBIGUOUS_REVIEWER_FAILURE` and rerun the review gate with an explicit reviewer.
