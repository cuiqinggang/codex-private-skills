# Recent Use Log

## 2026-07-08 - AI博士学习 12秒 V0 粗合成

- Task: create and audit a 12-second rough promotional video from existing
  local assets.
${REDACTED_SECRET}
- Gate added: iterative video audit before final reporting.
- Concrete catch: `screen_sequence_12s.mp4` and `main_keyframes_12s.mp4` were
  initially longer than 12 seconds; script was fixed to force exact 12.000s.
- Final status: `REVIEW_READY`, not `FINAL_PASS`.

## 2026-07-12 - AI博士学习 V4 12秒完整重建

- Task: rebuild a 12-second family education promo from 48 formal images,
  10 supplemental images, historical V1-V3 videos, voice and BGM.
${REDACTED_SECRET}
- Reusable gates added: anti-PPT motion ratio; explicit problem/start actions;
  single-composition high-five with approach/contact/rebound; CTA/voice and
  clap/contact sync within one frame; 30fps tail-pollution inspection.
- Repair chain: V01-V04 failed for short video stream, low loudness, unclear
  story, ghost hands, red contamination, excessive low-motion ratio, and
  0.2-second sync errors. V05 passed six rounds plus two independent reviews.
- Final status: `FINAL_CANDIDATE_PASS`.

## 2026-07-13 - AI博士学习 PPT V04 六页说服力重做

- Task: retain existing family images, rebuild a fixed six-page 12-second promo, replace the incorrect locked phrase, show a concrete three-step explanation, improve pacing, and clarify CTA value.
${REDACTED_SECRET}
- Reusable catches: screen logs must become an explanation-result card; CTA must not cover the high-five; final mixed-audio ASR exposed CTA starting too early, then it was moved to 9.82s; loudness was raised from -24.59 to -15.64 LUFS without re-encoding video.
- Three tests: technical/audio PASS; six-page and five-transition visual PASS; final-mix ASR/hash/replay PASS.
- Final status: `FINAL_CANDIDATE_PASS`.
