---
name: visual-proof-acceptance
description: "Use when verifying or accepting work that has visual, media, browser, UI, product, video, image, generated asset, demo, clone, replica, reproduction, or multi-stage deliverable output. This skill enforces evidence-first acceptance and, for clone/replica work, a Codex self-correction loop: left-original/right-clone comparison, Codex self-review, mandatory revision until self-pass, then GPT confirmation package."
---

# Visual Proof Acceptance

## Purpose

Use this skill when a task can look "done" from logs but may still be visually wrong, off-target, or far from the intended result.

Typical triggers:

- video/image/media generation or editing
- frontend/browser/UI/product work
- workflow outputs with screenshots, previews, exports, reports, or dashboards
- staged creative/technical pipelines where later drift is expensive
- user asks for 验收, 彻底验收, 看一眼, 目视检查, contact sheet, screenshot, browser check, proof, QC, review-ready, or status code

This skill is a principle, not a heavy ritual. Use the smallest useful proof for the task risk.

## Core Rule

Never claim visual/product completion from command success alone.

Acceptance requires:

```text
real artifact + technical probe + visible evidence + honest report
```

If the task has no meaningful visual surface, use the same principle with the narrowest observable evidence.

## Clone / Replica Hard Rule

For clone, replica, reproduction, "make it the same", visual remake, video remake, image remake, UI remake, programming-effect remake, or similar tasks, Codex must not hand a failing result to the user or GPT for judgment.

The required chain is:

```text
generate clone result
generate left-original / right-clone comparison evidence
Codex inspects the comparison
if Codex sees a hard failure, revise the clone
repeat comparison and self-review
only after Codex self-passes, generate the GPT confirmation package
the package contains Codex's self-review conclusion, reasons, left-right evidence, keyframe overview, and questions for GPT
GPT reviews the package and gives the final pass or rejection
```

The user is not the detail inspector. Codex must make the best self-judgment it can and generate a complete GPT confirmation package for final review.

## G00 Acceptance Classification

Classify the acceptance level:

| Level | Use when | Required proof |
| --- | --- | --- |
| V0 Quick | Tiny or text-only output | File exists / command output / narrow readback |
| V1 Standard | Normal generated files, reports, small UI changes | File checks + targeted command/probe + concise report |
| V2 Visual | Video/image/browser/UI/demo/product output | Technical probe + screenshot/contact sheet/browser observation + visual findings |
| V3 Gate | Release, destructive action, account/security/payment, broad batch change, or user-facing publish | Stop if required evidence, approval, source rights, or safety facts are missing |

Default to V2 for videos, images, websites, dashboards, apps, and visual demos.

Use the clone self-correction loop for any V2/V3 clone or replica task that has both an original and a generated/recreated output.

## Verification Workflow

### 1. Check Real Artifacts

Verify the output exists where expected.

Check:

- exact path
- file size
- modified time
- non-empty output
- expected companion files: report, log, manifest, screenshot, contact sheet, ffprobe report, test output

Fail if the artifact is missing, empty, in the wrong directory, or only described but not created.

### 2. Check Scope Lock

Confirm the work stayed inside the requested boundary.

Check:

- no unrequested stage jump
- no re-screening or replacing locked assets unless asked
- no fake placeholders passed as real output
- no final-release claim for a sample/prototype
- no broad unrelated edits

Fail or downgrade status if scope drift happened.

### 3. Probe Technical Properties

Use the narrowest tool that proves the artifact is structurally valid.

Examples:

- video/audio: `ffprobe`, duration, resolution, streams, codecs
- image: dimensions, format, open/read test
- browser/UI: page loads, console errors, screenshot, responsive viewport
- document/spreadsheet/PDF: parser/readback, page count, key text, render snapshot
- code: tests, lint/typecheck, smoke command

Do not treat probe success as visual success. It only proves the file can be read.

### 4. Produce Visible Evidence

For visual work, generate or capture something a human can inspect quickly.

Use as appropriate:

- contact sheet for video
- screenshot for image/UI/browser
- before/after image
- browser snapshot plus screenshot
- exported preview reel
- sampled frames at key timestamps

The evidence should cover important states, not just a pretty frame.

For video contact sheets, include:

```text
opening
main transitions
each required scene/slot
problem-prone areas
ending
```

### 5. Perform Visual Review

Actually inspect the visible evidence.

Ask:

- Does it match the requested intent?
- Are required objects/states visible?
- Is the layout or composition coherent?
- Are there obvious artifacts, overlays, watermarks, wrong crops, wrong clips, or source marks?
- Is the output only technically valid but visually wrong?
- Does it feel like the user asked, or did it drift?

For UI/browser work:

- verify the real page, not just code
- check desktop and mobile if relevant
- check text fit and overlap
- check important interactions

For video/media:

- check duration and stream structure
- inspect contact sheet
- if needed, inspect a few frames or open the video
- check audio logic when audio matters

### 6. Report PASS / FAIL / REVIEW-READY Honestly

Use honest status, not optimistic language.

Good statuses:

```text
PASS
REVIEW_READY
PARTIAL
BLOCKED
NEEDS_REWORK
MISSING_INPUT
RECTANGLE_ONLY_NEEDS_REWORK
SOURCE_RIGHTS_NEED_REVIEW
```

Clone/replica statuses:

```text
INTERNAL_SELF_FAIL_NEEDS_REVISION
CODEX_SELF_PASS_READY_FOR_GPT_CONFIRMATION
GPT_CONFIRMED_PASS
GPT_REJECTED_NEEDS_REWORK
BLOCKED_BEFORE_GPT_CONFIRMATION
```

`INTERNAL_SELF_FAIL_NEEDS_REVISION` is not a final delivery status. It means Codex must revise and rerun the loop.

`CODEX_SELF_PASS_READY_FOR_GPT_CONFIRMATION` is the only status that allows a GPT final confirmation package. It is not final PASS.

`GPT_CONFIRMED_PASS` is the true final PASS, and only after GPT confirms the Codex self-pass evidence.

`REVIEW_READY` remains valid for baseline/evidence packages that do not yet contain a clone result, such as original-video standard answer packs.

Do not write PASS when:

- visual evidence is missing
- the result is a placeholder
- a required input is missing
- the output is only a rectangle/rough mock when the task requires a spatial effect
- source rights or release readiness are unverified
- the main user intent is not visible

Use `REVIEW_READY` when a sample is generated and inspectable but not final quality.

## Clone Self-Correction Loop

For each iteration, save:

```text
iteration_01/side_by_side.mp4
iteration_01/keyframe_compare_contact_sheet.jpg
iteration_01/self_judgment.md
iteration_01/fix_notes.md
```

Then repeat as `iteration_02/`, `iteration_03/`, and so on until Codex self-passes or reaches a real blocker.

Each `self_judgment.md` must check:

```text
1. composition/layout consistency
2. finger or control position consistency when relevant
3. object/plant/subject appearance position consistency
4. object/plant/subject shape consistency
5. growth/motion/interaction rhythm consistency
6. pressure/release/bounce animation consistency when relevant
7. occlusion/layering correctness
8. shadow, blending, texture, and natural integration
```

Hard failures requiring revision:

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

If any hard failure exists, do not generate `gpt_final_confirmation_package.html`. Revise the clone and rerun comparison.

Only when Codex judges all required conditions are satisfied may it generate:

```text
gpt_final_confirmation_package.html
keyframe_compare_contact_sheet.jpg
original_vs_clone_side_by_side.mp4
codex_self_visual_judgment.md
gpt_final_confirmation_prompt.md
```

At that point write:

```text
CODEX_SELF_PASS_READY_FOR_GPT_CONFIRMATION
```

Then Codex must produce a complete GPT final review package containing the prompt, evidence summary, keyframe overview, left-right comparison evidence, and the exact questions GPT must answer. If a safe GPT bridge route is available for the task, Codex may use it to request final review; otherwise the package remains ready for GPT review without downgrading the Codex self-pass evidence.

If multiple iterations still cannot self-pass, write `BLOCKED_BEFORE_GPT_CONFIRMATION` and explain: attempts, per-iteration failures, why left-right consistency was not reached, and what new material or method is needed.

For detailed clone-loop wording, see `references/clone-self-correction-loop.md` when the task is a reproduction/clone and the next step is not merely an original baseline package.

## Final Report Template

For V2/V3 tasks, include:

```text
1. Output files
2. Input/manifest used
3. Scope boundary honored or not
4. Commands/checks run
5. Technical probe results
6. Visible evidence produced
7. Visual review findings
8. What works
9. What is weak or not final
10. Skipped checks and why
11. Residual risks
12. Recommendation for next stage
13. Final status code
```

Keep the report proportional. A tiny task does not need a long audit.

## Red Flags

Stop or downgrade if you see:

- file missing but final answer says complete
- command succeeded but no visual inspection occurred
- output file exists but duration/resolution/streams are wrong
- contact sheet shows wrong content
- visible text/logos/watermarks that violate requirements
- browser page loads but layout visibly overlaps
- user asked for sample but output is described as final
- acceptance status hides obvious flaws
- the work drifted from the user's mental target

## Standard Principle

The acceptance question is not:

```text
Did the command finish?
```

It is:

```text
Does the real output, when inspected through the right visible surface, match the intended result closely enough for this stage?
```

When in doubt, produce visible proof and say what it shows.
