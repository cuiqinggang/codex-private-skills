# L09 First Composite Comparison Report

Task ID: AI_VIDEO_REPLICA_R1_MOTHER_PLATE_REPLICA_12_LAYER_20260529

Layer: L09 / First Composite And Same-Frame Comparison
Status: L09_PASS_FIRST_COMPOSITE_COMPARABLE

## Outputs

- First composite: `H:\AI\workspaces\AI-VIDEO-REPLICA-R1-MOTHER-PLATE-20260529\08_composite_draft\r1-first-composite.mp4`
- Side-by-side frames: `H:\AI\workspaces\AI-VIDEO-REPLICA-R1-MOTHER-PLATE-20260529\09_comparison\side-by-side`
- Contact sheet: `H:\AI\workspaces\AI-VIDEO-REPLICA-R1-MOTHER-PLATE-20260529\09_comparison\contact-sheet.jpg`
- Deterministic image metrics: `H:\AI\workspaces\AI-VIDEO-REPLICA-R1-MOTHER-PLATE-20260529\09_comparison\comparison-metrics.csv`

## Scoring Table

| Time | Composition | Ring / circle | Center body | Light / color | Modern desktop | Magic mood | Motion state | Overall source identity | Total |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.0s | 19 | 14 | 13 | 14 | 15 | 14 | 6 | 8 | 93 |
| 0.8s | 20 | 14 | 14 | 15 | 15 | 15 | 6 | 7 | 96 |
| 1.6s | 19 | 14 | 14 | 14 | 15 | 14 | 6 | 8 | 94 |
| 2.4s | 18 | 13 | 13 | 13 | 14 | 13 | 6 | 9 | 89 |
| 3.2s | 19 | 14 | 14 | 14 | 15 | 14 | 6 | 8 | 94 |
| 4.0s | 19 | 15 | 14 | 14 | 15 | 14 | 7 | 7 | 95 |
| 4.8s | 19 | 15 | 14 | 14 | 14 | 14 | 7 | 7 | 94 |
| 5.6s | 20 | 15 | 15 | 15 | 14 | 15 | 7 | 6 | 97 |

Average keyframe score: 94.0 / 100

Lowest keyframe score: 89 / 100

Clearly unlike keyframes: 0

## Deterministic Evidence Summary

The comparison-metrics CSV reports global luma SSIM hints from 0.79345 to 0.96337 and evidence-score hints from 91.0 to 98.8. These are not treated as final acceptance by themselves, but they support the visual scoring.

## Notes

This first composite is a sparse-keyframe plate-guided replica. It is not a clean-room Blender-only 3D rebuild and it does not use the full source frame sequence. The approach is intentionally mother-plate driven to prioritize high similarity over free redesign.

## Gate L09

Gate rule: average score must be at least 80 to enter L10.

Result:

- Average score 94.0 >= 80.
- Side-by-side comparison exists.
- First composite exists.

Gate result: L09_PASS_FIRST_COMPOSITE_COMPARABLE
