# Rule Patch 2026-07-05: UltraFusion V7.0 Semi-Automatic ABCD

## New Rule

UltraFusion V7.0 adds a semi-automatic copy-paste route:

```text
Codex generates question packages.
Human copies and pastes only.
External models answer.
Codex fuses, converges, scores, and judges gain.
```

## Trigger Keywords

- `UltraFusion V7.0`
- `半自动ABCD`
- `ABCD问题包`
- `复制粘贴多层推理`
- `外部模型回答`
- `Score_0 vs Score_FINAL`
- `Gain < 2`

## Interaction Rule

When this route is triggered, Codex must produce clean copy blocks for A/B/C/D. The human should not be asked to design prompts, compare drafts, or make fusion judgments. The human operation is limited to copying packages to external models and pasting answers back.

## Compatibility Rule

V7.0 does not delete UltraFusion 6.1B. It is an optional route label:

```text
UF_V7_SEMI_AUTO_ABCD
```

Existing automated official-site routes remain available when automation is appropriate.

## Quality Gate

The run is only valuable when:

```text
Gain = SCORE_FINAL - Score_0 >= 2.0
```

If `Gain < 2.0`, Codex must call the run `INVALID_CHAIN` and explain why the extra layers failed to produce enough value.

