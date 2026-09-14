# Changelog

## 0.1.0 — 2026-09-15

Initial reusable performance benchmark convergence skill extracted from the `visual-art-engine-performance-ladder` P0 Measurement Protocol V2 case.

Included:

- benchmark profile freezing;
- runtime/filesystem/path-length preflight;
- runner + harness manifest fingerprinting;
- label-blind A/A selftests;
- statistical selftest and null Type-I calibration;
- MDE after null calibration;
- interleaved block A/A and paired A/B;
- shared-A cluster handling;
- order-effect equivalence rules;
- environment drift gate;
- confirmation batches;
- separation between benchmark PASS and project score 99;
- evidence retention and superseded-result rules;
- reusable failure lessons including label leakage and Windows evidence-path length.

Source case milestone:

- old contaminated A/A effect `3.24545 ms`, CI `[0.579475,5.953475]`;
- label-blind runtime-confirmed A/A completed 160/160 valid;
- new formal effect `2.8688 ms`, CI `[-0.847625,6.585225]`, noise floor `3.7609 ms`;
- label-leak causal repair confirmed;
- overall `AA_CALIBRATION=INCONCLUSIVE` because order-effect CI was not contained inside the frozen equivalence interval;
- candidate lock remained ON.
