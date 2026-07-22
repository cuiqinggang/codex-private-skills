# Case: Codex Goal / Loop Long Coding Closed Loop

Date: 2026-07-08

Source video:
${REDACTED_SECRET}

Transcript evidence:
${REDACTED_SECRET}

Readable transcript:
${REDACTED_SECRET}

## Material Value Judgment

Status: HIGH_VALUE

Reason:

1. It explains why long coding work needs a closed loop, not just repeated prompting.
2. It gives a concrete long-run coding scenario: schema/model refactor, tests, failures, repairs, and final acceptance.
3. It names the key risk: uncontrolled loops can burn tokens and degrade code.
4. It aligns with `long-coding-flow`, `loop-stage-acceptance`, Codex Goals, and Loop Engineering.
5. It can become a reusable preflight rule for long coding, refactors, migration, debugging, and knowledge/workflow tasks.

## Core Lesson

Do not treat long-running coding as:

```text
failure -> ask AI to fix -> failure -> ask AI to fix -> ...
```

Treat it as:

```text
observable goal -> bounded stage -> verification -> strategy decision -> continue / stop / rollback / human review
```

The video's key distinction:

- Loop without closure becomes a token black hole.
- Closed loop has a target, a verifier, an alternate strategy, and a stop rule.

## Four Questions Per Round

Every long-coding loop round must answer:

1. Why should this run continue?
2. What concrete evidence will verify this round?
3. If verification fails, what strategy changes instead of repeating the same fix?
4. At what point should the run stop, report `BLOCKED`, rollback, or ask for human review?

If any question cannot be answered, do not start the next round.

## Where This Applies

Use this case for:

1. large refactors and data-model/schema migrations
2. test-driven bug repair
3. flaky test reproduction
4. performance tuning with benchmarks
5. dependency upgrades
6. frontend visual repair with screenshots or Playwright
7. knowledge-base cleanup and indexing
8. skill-package repair or evolution
9. multi-step research with an evidence-backed final report
10. periodic architecture cleanup caused by fast AI-generated code accumulation

## Where It Does Not Apply Directly

Avoid autonomous loop execution when:

1. the target is subjective or not observable
2. no test, benchmark, artifact, screenshot, diff, report, or human gate exists
3. rollback is impossible
4. one failed action may create irreversible side effects
5. the task requires credentials, payments, account actions, or destructive operations
6. the next step depends on user preference rather than evidence
7. the loop has no time, token, round, or budget limit

Use a small experiment, a plan, or a human review gate first.

## Loop vs Goal

### Loop Mode

Best when the task is one stage or one artifact and can be repaired in bounded rounds.

Recommended default:

```text
first version -> self-check -> defect list -> repair -> verify
max repair rounds: 3
terminal states: PASS / PARTIAL / BLOCKED
```

Use for: page polish, report repair, prompt improvement, one failing test class, one dashboard page, one skill reference.

### Goal Mode

Best when the end state is stable but the path is unknown.

A strong goal must define:

1. outcome
2. verification surface
3. constraints
4. boundaries
5. iteration policy
6. blocked stop condition

Use for: multi-file refactor, benchmark tuning, migration, large bug hunt, flaky test investigation, multi-step research, long audit.

## Recommended Closed-Loop Contract

For future long coding tasks, create or restate:

```text
Goal:
- desired end state:
- non-goals:
- forbidden changes:

Verification:
- tests/benchmarks/checks:
- manual or visual gate:
- evidence files:

Boundaries:
- allowed files/dirs/tools:
- forbidden files/dirs/tools:
- approval-needed actions:

Iteration:
- max rounds per stage:
- max total stages or timebox:
- how to pick the next hypothesis:
- what must change after a failed round:

Stop:
- PASS condition:
- PARTIAL condition:
- BLOCKED condition:
- rollback condition:
- human-review condition:

Memory:
- execution log:
- verification log:
- handoff:
- reusable lesson:
```

## Anti-Black-Hole Rules

1. Never rerun the same fix after the same failure without a changed hypothesis.
2. Never rely only on model self-evaluation when real evidence is available.
3. Never continue after three repair rounds in the same stage unless the user explicitly expands the budget.
4. If tests cannot run, report that as a blocker or downgrade to `PARTIAL`.
5. If a repair expands scope, return to the goal and boundary check before editing.
6. If context grows large, compact into task-package files instead of feeding full chat history back into the model.
7. If a high-risk tool action appears, pause for human approval.
8. If budget is reached, summarize progress and next best step; do not call it complete.

## Trigger Keywords

Use this case when the user mentions:

```text
长流程编程
长流程编码
Codex Global
Codex Goal
/goal
goal 方式
Loop Engineering
闭环工程
不要无限循环
不要浪费 token
一直修到好
长时间自动编码
前后端大重构
数据模型重构
测试失败自动修复
直到 achieve
```

## Preflight Action

Before starting a related task:

1. Run the reuse preflight check with the user's task description.
2. Read `long-coding-flow/SKILL.md`.
3. Read `loop-stage-acceptance/SKILL.md`.
4. If the task is codebase-related and `.codegraph/` exists, use CodeGraph before broad search.
5. Create or verify `00-goal.md`, `02-plan.md`, `04-verification.md`, `05-handoff.md`, and `07-loop-control.md` for long work.
6. Pick Loop Mode or Goal Mode before execution.

## Failure Review Entry Point

If the loop fails, record:

1. repeated failure signature
2. whether the same hypothesis was retried
3. evidence that was missing or ignored
4. whether round/time/token limits were respected
5. rollback or recovery action
6. next user input or external condition needed

Store the review under the most relevant skill's `references/` or `logs/` folder.

## Acceptance Criteria

This lesson is deployed when:

1. trigger keywords are searchable
2. transcript evidence exists
3. the Loop vs Goal distinction is written down
4. the four per-round questions are preserved
5. stop conditions and budget limits are explicit
6. next-run reuse instructions are present
7. usage log records the case

## External Sources Checked

- OpenAI Developers: Codex Goals are thread-scoped completion contracts with evidence, budget, lifecycle controls, and stop conditions.
- Anthropic Engineering: effective agents need environmental feedback, checkpoints, human feedback when needed, and stopping conditions.
- LangChain/LangGraph docs: human-in-the-loop and recursion limits are control mechanisms for pausing, resuming, and preventing unbounded graph execution.
- 12-Factor Agents: own context, execution state, control flow, pause/resume, and error compaction.
- Recent loop-engineering research: loop specifications should include trigger, goal, verification, stopping rule, and memory.
