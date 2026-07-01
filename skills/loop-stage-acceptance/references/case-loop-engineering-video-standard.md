# Case: Loop Engineering Video Standard

Source text: `C:\Users\A\.codex\manual-paste-attachments\codex-pasted-text-20260615-230906-60be3bfb.txt`

Visual evidence: `C:\Users\A\Desktop\4\loop_video_contact_sheet.jpg`

## Material Value Judgment

Status: HIGH_VALUE

Why:

1. It upgrades Loop from "multi-round prompt" to validation-driven engineering.
2. It gives clear acceptance and rejection criteria for loop tasks.
3. It defines reusable rules: observable goals, small-step execution, harness verification, and explicit decisions.
4. It prevents common failures: endless running, no evidence, no rollback, and fake PASS.
5. It maps directly to the user's Codex, AI Company OS, Obsidian, dashboard, skill-package, and image/video workflows.

## Core Definition

Loop Engineering is not simply asking AI to run more rounds.

Mature loop:

```text
Observable Goal -> Small Execution Step -> Verification/Harness -> Decision -> Next Round or Stop
```

The four core elements are:

1. 目标: a result that can be observed, checked, scored, reproduced, and used to decide the next step.
2. 执行: a bounded small step performed by the agent, with a record of what changed.
3. 验证: a verifier or real-world signal checks whether the step worked.
4. 决策: continue, stop, rollback, or hand off to human review.

## New Rule

Do not call a workflow a mature loop unless it has a verifier.

Verification can be:

1. unit tests
2. lint
3. CI
4. Playwright
5. screenshot comparison
6. HTML open check
7. file existence check
8. link validity check
9. JSON or manifest consistency check
10. git diff review
11. contact sheet comparison
12. human visual gate review

Model self-evaluation is useful, but it is not enough for a strong PASS when external evidence is possible.

## Cron, Mega-Prompt, Routine, Loop

### Cron

Cron is time-triggered. It runs on a schedule, but it may not know whether the task succeeded. Cron lacks semantic stop conditions unless additional verification is added.

Use cron for periodic background work, not as proof of a mature loop.

### Mega-Prompt

Mega-prompt gives the model a large context and asks for a large answer in one pass. It can be useful, but it is fragile for long complex work because failure locations are unclear and intermediate validation is weak.

Mega-prompt is not a replacement for Loop Engineering.

### Routine

Routine is a long-term, periodic, often server-side workflow such as weekly checks, dependency updates, log scans, or health reports.

Routines discover or monitor issues.

### Loop

Loop is interactive, validation-driven, and repair-oriented. It advances through small steps, checks each step, then decides whether to continue, stop, rollback, or ask a human.

Loops repair or mature issues.

## Harness

Harness is the testing shell that makes a loop trustworthy.

Common harnesses:

1. `pytest`
2. Playwright
3. lint
4. CI
5. screenshot comparison
6. HTML open check
7. file list check
8. manifest comparison
9. git diff
10. human gate review

When possible, design the harness before running the loop.

## Long-Running Agent Roles

Use this structure for long-running agent tasks:

1. Planner: plans, reorders, removes completed tasks, and selects the next step.
2. Generator: creates patches, content, files, reports, or designs.
3. Evaluator: runs tests, checks UI, reads screenshots, compares manifests, and returns evidence.

The loop is:

```text
Planner -> Generator -> Evaluator -> Planner
```

The Evaluator should prefer real-world signals such as Playwright, screenshots, tests, lint, CI, filesystem checks, manifests, or user visual confirmation.

## Decision Matrix

| Question | If yes | If no |
| --- | --- | --- |
| Is the goal observable? | Suitable for loop | Clarify the goal first |
| Can the task be split into small steps? | Suitable for loop | Do not start direct loop |
| Is there a verifier? | Suitable for loop | Use human gate or create a verifier |
| Is rollback possible? | Suitable for loop | Add protection or avoid loop |
| Is there a cost limit? | Suitable for loop | Risk of runaway cost |
| Is there a stop condition? | Suitable for loop | Risk of endless loop |
| Is evidence produced? | Can consider PASS | Do not mark PASS |

## Four Decisions

### Continue

Use when verification passed, there is a next stage, and risk/cost remain controlled.

### Stop

Use when the target is reached, further gains are low, cost exceeds benefit, or maximum rounds have been reached.

### Rollback

Use when a change breaks existing behavior, tests fail, the page cannot open, the file structure is polluted, or the user boundary is violated.

### Human Review

Use when the decision depends on aesthetics, business direction, high-risk change, user preference, or a condition that cannot be automatically verified.

## Suitable For Loop Engineering

Use Loop Engineering when most of these are true:

1. target is clear
2. task can be split into small steps
3. verifier exists or can be built
4. rollback is possible
5. cost is controlled
6. stop condition is explicit
7. evidence can be captured
8. errors are observable
9. git or snapshots are available
10. user boundary is clear

Typical suitable scenarios:

1. code repair
2. HTML/CSS page repair
3. Playwright UI checks
4. Obsidian knowledge archive
5. Codex skill-package improvement
6. dashboard clickable entry repair
7. long-task stage acceptance
8. file consistency checks
9. image/video keyframe comparison
10. automated report generation

## Not Suitable For Direct Loop

Do not launch a direct loop when:

1. task is highly ambiguous
2. no verifier exists
3. rollback is impossible
4. one failed step is too costly
5. token cost is high and benefit is unclear
6. result is purely subjective
7. stop condition is missing
8. AI self-evaluation is the only evidence
9. task cannot be decomposed
10. user boundary is unclear

Do these first instead:

1. clarify target
2. analyze samples
3. extract standards
4. ask for human gate review
5. run a small experiment

## User Project Defaults

For this user's workflows:

1. Codex long tasks: no evidence means no PASS.
2. Dashboard tasks: if the page cannot open, no PASS.
3. Knowledge-base tasks: if there is no index or navigation, no PASS.
4. Image/video tasks: if there is no comparison image or contact sheet, no PASS.
5. Skill-package tasks: if there is no `SKILL.md`, template, and acceptance standard, no PASS.

## Skill Package Patch Pattern

When adding this video standard to a loops skill package, add or adapt:

1. `09_LOOP_ENGINEERING_VIDEO_STANDARD_PATCH.md`
2. `10_LOOP_ENGINEERING_DECISION_MATRIX.md`
3. `11_ROUTINES_VS_LOOPS_AND_HARNESS.md`
4. a `SKILL.md` section named `Loop Engineering 视频补丁原则`
5. a `SUMMARY.md` update, if `SUMMARY.md` exists
6. `LOOP_ENGINEERING_VIDEO_PATCH_REPORT.md`

Do not:

1. delete old files
2. overwrite the existing `SKILL.md`
3. rebuild the whole skill package
4. reduce the video to a summary
5. define loop as merely "multiple prompt rounds"
6. mix cron, mega-prompt, routine, and loop
7. claim PASS without verification evidence

## Acceptance Criteria

This case is considered reusable when:

1. Loop is defined as observable goal + execution + verification + decision.
2. Cron, mega-prompt, routine, and loop are distinguished.
3. Harness and real-world signals are listed.
4. Continue/stop/rollback/human-review decisions are defined.
5. Suitable and unsuitable loop conditions are listed.
6. The user's no-evidence-no-PASS defaults are preserved.
7. The source text and contact sheet evidence paths are recorded.

## Trigger Keywords

Use this case when the user mentions:

```text
Loop Engineering
/loops
验证驱动
Harness
测试 Harness
Routines vs loops
Cron vs loop
Mega-prompt vs loop
Planner Generator Evaluator
真实世界信号
没有验证器不得 PASS
继续 停止 回滚 人审
```
