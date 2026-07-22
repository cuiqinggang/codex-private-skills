# R1 Replica Standard

## PASS Threshold

R1 PASS requires:

- Keyframe similarity average >= 88 / 100.
- Lowest core keyframe >= 80 / 100.
- Motion rule replica score >= 85 / 100.
- Sound event and mood replica score >= 80 / 100.
- Modern desktop + magic juxtaposition score >= 85 / 100.
- Clearly unlike keyframes <= 1.
- Every layer gate PASS.
- The output is not the original video and not a full source-frame sequence rebuild.

## Evidence Required

- Source metadata and hash.
- Locked target clip.
- Extracted frames and frame index.
- Extracted audio and event map.
- Replica specification.
- Rebuild plan and layer plan.
- Visual and motion/audio logs.
- First composite MP4.
- Source-vs-replica contact sheet.
- Comparison report.
- Verification result JSON and Markdown.
- Repair log if any repair happened.
- Final acceptance JSON.

## Hard FAIL

- Full source clip delivered as the output.
- Full extracted source frame sequence encoded as the output.
- No audio analysis.
- No modern desktop layer.
- No same-time comparison.
- Any final threshold below PASS.
