# Clone Self-Correction Loop

Use this reference for clone, replica, remake, reproduction, or "make the output match the original" tasks.

## Statuses

```text
INTERNAL_SELF_FAIL_NEEDS_REVISION
CODEX_SELF_PASS_READY_FOR_GPT_CONFIRMATION
GPT_CONFIRMED_PASS
GPT_REJECTED_NEEDS_REWORK
BLOCKED_BEFORE_GPT_CONFIRMATION
```

`INTERNAL_SELF_FAIL_NEEDS_REVISION` is internal only. It cannot be used as a final handoff and cannot be sent to GPT for confirmation.

`CODEX_SELF_PASS_READY_FOR_GPT_CONFIRMATION` means Codex has inspected left-original/right-clone evidence and believes the result is ready for GPT to verify. Codex must generate a GPT final confirmation package. It is not final PASS.

`GPT_CONFIRMED_PASS` is the only final PASS.

## Required Loop

```text
generate clone result
generate original vs clone left-right comparison
Codex self-checks the comparison
if any hard failure exists, revise clone
regenerate comparison
repeat until self-pass or blocked
after self-pass, Codex generates the GPT final confirmation package
```

Every iteration must save:

```text
iteration_xx/side_by_side.mp4
iteration_xx/keyframe_compare_contact_sheet.jpg
iteration_xx/self_judgment.md
iteration_xx/fix_notes.md
```

## Self-Check Items

Check every important keyframe, screenshot, or interaction state:

```text
1. composition/layout consistency
2. finger/control position consistency when relevant
3. object/plant/subject appearance position consistency
4. object/plant/subject shape consistency
5. growth/motion/interaction rhythm consistency
6. pressure/release/bounce animation consistency when relevant
7. occlusion/layering correctness
8. shadow, blending, texture, and natural integration
```

## Hard Failures

Any of these requires another revision:

```text
finger/control trajectory obviously differs
object/path/layout obviously differs
clone covers or corrupts the original foreground subject
foreground subject is polluted, warped, or visually broken
clone appears as a pasted sticker or sudden hard overlay
required pressure/release/bounce/intermediate motion is missing
detail timing is obviously wrong
background, device, keyboard, UI, or stable environment is obviously deformed
left-right comparison is obviously not the same effect
```

## GPT Confirmation Package Gate

Generate the GPT confirmation package only after Codex self-passes.

Required files:

```text
gpt_final_confirmation_package.html
keyframe_compare_contact_sheet.jpg
original_vs_clone_side_by_side.mp4
codex_self_visual_judgment.md
gpt_final_confirmation_prompt.md
```

Required package wording:

```text
Codex has completed the self-correction loop.
The current result has passed Codex self-review.
Status: CODEX_SELF_PASS_READY_FOR_GPT_CONFIRMATION.

Please GPT judge from the left-right screenshots, left-right synchronized video,
and Codex self-review report whether Codex's self-review is correct and whether
the result can be finally marked GPT_CONFIRMED_PASS.
```

The package must include Codex's self-review conclusion, reasons, left-right comparison evidence, keyframe overview, and the exact questions GPT must answer. If a safe GPT bridge route is available for the task, Codex may use it to request final review. The user should not be asked to perform the detailed comparison.

## Blocked Before GPT Confirmation

If Codex cannot reach self-pass after multiple iterations, do not pretend success.

Write:

```text
BLOCKED_BEFORE_GPT_CONFIRMATION
```

Include:

```text
1. number of attempts
2. where each iteration failed
3. why left-right consistency was not reached
4. what new input or different method is needed
```
