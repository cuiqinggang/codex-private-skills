# Reusable Benchmark Playbook

## 0. Goal

Use this playbook when a project needs trustworthy millisecond-scale performance comparison. The purpose is to avoid repeating exploratory debugging each time: substitute the task-specific profile, keep the measurement gates stable, and obtain a defensible result.

This playbook does **not** guarantee that a candidate becomes faster or reaches project score 99. It guarantees a repeatable decision process.

---

## 1. Freeze the benchmark profile

Create one profile from `templates/BENCHMARK-PROFILE.md` and freeze:

- task/contract identity;
- baseline implementation A;
- candidate implementation B, when applicable;
- workload/workflow/fixture;
- endpoint and runtime startup/readiness;
- `T_START` and `T_END`;
- exact output-validity gates;
- evidence root;
- environment fingerprint;
- warmup/block/seed policy;
- decision-rule version.

If any of these materially changes, create a new profile/harness identity instead of silently reusing old results.

---

## 2. Preflight

Before any timed run, verify:

1. runtime endpoint healthy;
2. expected port/listener state known;
3. output/evidence filesystem writable;
4. evidence path is short enough for the target OS;
5. enough disk space exists;
6. runner, launcher, rules, workflow and fixture exist;
7. no forbidden environment modification is required;
8. prior user processes are not terminated;
9. output validator passes on a known-good fixture;
10. timing marks use monotonic time.

On Windows, explicitly test creation of the deepest expected evidence path before the authoritative run. Long-path failure must be caught here, not after hundreds of runs.

If runtime creation is blocked by permission, report `BLOCKED_RUNTIME_PERMISSION`; do not bypass policy. A user- or operator-started existing runtime may be used if that is normal and permitted.

---

## 3. Freeze the harness identity

Record both:

- `RUNNER_SHA`
- `HARNESS_MANIFEST_SHA`

The harness manifest should deterministically cover every file that can change benchmark behavior, normally including:

- runner;
- launchers/wrappers;
- decision rules;
- bracket/statistical scripts;
- workflow;
- fixture;
- output validator;
- other runtime config that changes the measured path.

Never include the manifest itself recursively.

Any material covered-file change means a new harness fingerprint.

---

## 4. Label-blind selftest

Before A/A, prove that arm identity is metadata only.

Required gates:

- `WORKFLOW_LABEL_LEAK=0`
- `TIMED_PATH_LABEL_LEAK=0`
- `HTTP_LABEL_LEAK=0`
- `NORMALIZED_A_B_WORKFLOW_EQUAL=YES`

Strongly preferred:

- `A_NORMALIZED_WORKFLOW_SHA == B_NORMALIZED_WORKFLOW_SHA`

Arm names must not enter:

- workflow JSON;
- filename/output prefix;
- HTTP path/query;
- client/session identifier;
- timed raw-event path;
- timed evidence/output path.

Use opaque fixed-format run tokens. Store arm mapping outside the timed path.

If any leak gate fails, stop. Do not run authoritative A/A.

---

## 5. Statistical selftest and null calibration

Run the production statistical code against synthetic/null data using the same KEEP rule used later for real candidates.

Minimum outputs:

- `STATISTICAL_SELFTEST=PASS`
- `NULL_POSITIVE_FALSE_KEEP_RATE`
- `NULL_ANY_DIRECTION_REJECTION_RATE`
- simulation iteration count

For a two-sided 95% CI with a one-direction KEEP criterion, the positive false KEEP rate should be consistent with the intended Type-I budget and the any-direction rejection rate should be consistent with the two-sided alpha budget.

Do not compute or certify final MDE before null calibration passes.

---

## 6. Compute MDE under the real dependency structure

After null calibration PASS, estimate the smallest true gain detectable at target power under the same:

- block structure;
- cluster structure;
- bootstrap/statistical estimator;
- KEEP rule.

Store:

- `FINAL_MDE_MS`
- target power
- observed/estimated power
- full power curve when practical.

MDE is a measurement-resolution property, not a required optimization target.

---

## 7. Authoritative A/A

Run identical implementation vs identical implementation in the same lifecycle and warmed environment.

Recommended structure:

- fixed-seed interleaved ABBA/BAAB blocks;
- block is the independent unit;
- no arm-specific path behavior;
- 100% output validity required.

Report at minimum:

- valid runs;
- formal effect;
- 95% CI;
- A/A noise floor;
- order effect;
- order-effect 95% CI;
- environment drift status;
- A/A calibration status.

### A/A decision

`PASS` only when the frozen rules say the identical implementations are equivalent within the acceptable measurement bounds, including the order-effect gate.

`FAIL` when there is a reproducible, decision-relevant false effect.

`INCONCLUSIVE` when evidence is insufficient for equivalence or rejection. Do not force PASS by widening bounds or changing alpha after seeing the batch.

A/A FAIL or INCONCLUSIVE keeps candidate evaluation locked.

---

## 8. Interpret repair experiments correctly

When an A/A defect is found and repaired:

1. preserve original runner and evidence;
2. record root cause, diff and repair reason;
3. create a new runner/harness SHA;
4. repeat selftest/null checks as required;
5. rerun authoritative A/A.

A repair can be causally confirmed even if overall A/A remains INCONCLUSIVE for a different gate. Example pattern:

- old false effect CI entirely positive;
- repair removes label/path contamination;
- new formal CI crosses zero and falls within noise;
- a separate order-equivalence CI remains too wide.

In that situation record both facts: root-cause repair confirmed, overall A/A not yet PASS.

---

## 9. Candidate paired A/B

Only after `AA_CALIBRATION=PASS` set `CANDIDATE_LOCK=OFF`.

Use contemporaneous paired/interleaved A/B instead of a historical fixed median.

For each candidate:

- same workload/validator;
- same frozen harness;
- same environment window;
- independent block structure;
- paired delta estimator;
- output validity 100%;
- drift gate checked.

Do not delete slow samples. Do not silently replace failed attempts.

### Candidate statuses

Use:

- `KEEP`
- `ROLLBACK`
- `INCONCLUSIVE_BELOW_MEASUREMENT_RESOLUTION`
- `INVALID_ENVIRONMENT_DRIFT`
- `INCONCLUSIVE`

A robust KEEP normally requires:

- positive effect under the declared sign convention;
- CI supports the positive direction;
- effect exceeds relevant A/A noise floor;
- effect is detectable relative to MDE;
- output validity 100%;
- confirmation batches agree.

---

## 10. Shared-A / bracket handling

If multiple comparisons share `A_before` or `A_after`, observations are clustered.

Do not split them into IID samples. Resample at the explicit bracket/block identifier level.

Prefer independent `A_before, B, A_after` triples when using short brackets.

---

## 11. Order effect

Never use `p>0.05` as proof of equivalence.

Use:

- block-level order contrast;
- effect size;
- 95% CI;
- predeclared equivalence bound.

Only declare order equivalence PASS when the full CI is contained inside the equivalence interval required by the frozen rules.

If CI is too wide, result is `INCONCLUSIVE`, not automatic FAIL.

---

## 12. Environment drift

Evaluate contemporaneous A behavior for time-order drift.

If environment drift invalidates the comparison, report `INVALID_ENVIRONMENT_DRIFT`. Do not blame the candidate and do not merge the batch into authoritative history.

Record environment identity such as:

- OS;
- runtime/Python;
- key library versions;
- endpoint;
- output root;
- relevant hardware/runtime mode.

---

## 13. Confirmation

A candidate that initially passes should be rerun in independent confirmation batches before becoming the new stable baseline.

Confirmation should not reuse the same accidental time window as the discovery batch.

Keep the previous stable implementation and rollback path until confirmation is complete.

---

## 14. From benchmark PASS to project score 99

Benchmark certification and project score 99 are separate.

Use the benchmark to establish trustworthy `T_CURRENT` and candidate effects. Project-level 99 additionally requires checking:

1. current best stable implementation;
2. remaining high-value candidates;
3. external mature frontier;
4. first-principles physical-time direction/range where the project uses it;
5. confirmation and operational stability;
6. whether remaining feasible low-risk work is likely to produce material gain.

Only then freeze a project stage as 99.

---

## 15. Evidence retention

For each important batch retain:

- profile/contract;
- runner SHA;
- harness manifest SHA;
- raw monotonic events;
- exact output validity evidence;
- raw history/response where relevant;
- paired results;
- null/MDE outputs;
- environment record;
- decision summary;
- repair diff/reason when applicable.

Raw large run corpora may stay in the project Stage. The reusable skill should store durable rules, decision summaries and evidence pointers rather than duplicating every PNG/history file.

Never delete superseded failures; mark their role explicitly.

---

## 16. Fast path for future projects

Once this method is mature, the normal new-project path is:

1. copy profile template;
2. fill task-specific placeholders;
3. run preflight;
4. compute harness fingerprint;
5. run label-blind selftest;
6. run/verify statistical null calibration for the frozen statistical implementation;
7. run authoritative A/A;
8. if PASS, run paired A/B candidates;
9. confirmation;
10. update project 99/freeze decision.

Do **not** repeat historical root-cause exploration unless a gate fails. The purpose of this skill is that known failure modes are tested automatically or explicitly at preflight rather than rediscovered manually.
