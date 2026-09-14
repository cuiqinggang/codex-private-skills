# Reusable Failure Lessons

These lessons are generalized from the first production case and should be checked before inventing a new measurement method.

## Historical baseline drift

Do not decide millisecond-scale candidates against a historical fixed median when unchanged code itself drifts by a comparable or larger amount. Prefer contemporaneous interleaved paired A/B.

## Null calibration before MDE

A mathematically plausible MDE is not authoritative if the actual production KEEP pipeline has an excessive gain=0 false-positive rate. Calibrate Type-I error first, then compute MDE using the same dependency structure and rule.

## `p>0.05` is not equivalence

Failure to reject a difference does not prove equivalence. Use a predeclared equivalence interval and require the confidence interval to fit inside it.

## Shared-A means clustered data

Comparisons that reuse the same A_before or A_after are not IID. Resample at the bracket/block level or redesign the experiment with independent triples.

## Statistical changes invalidate prior authority

If CI/bootstrap/null/MDE/order/drift logic materially changes, create a new runner SHA and rerun calibration. Old batches remain evidence but cannot be reclassified post hoc as authoritative under the new rule.

## Label leakage can create fake optimization

A/B arm labels must not change the execution path. Labels embedded in workflow output names, HTTP identities, client/session identifiers, raw-event paths or evidence paths can create a false arm effect even when the algorithm is identical.

Require normalized workflow equality and explicit zero-leak selftests before A/A.

## Statistical PASS does not imply runtime A/A PASS

Synthetic/null statistics can be correct while the real harness still produces a false difference because of scheduling, filesystem, client lifecycle, caching, path identity or other execution effects. Keep the gates independent.

## Root-cause repair and overall calibration are different conclusions

A repaired contaminant may be causally confirmed when its characteristic false signal disappears, while another independent gate remains inconclusive. Record both; do not collapse them into one PASS/FAIL label.

## Windows path length belongs in preflight

A deep Stage root plus per-run evidence subdirectories can exceed practical path limits. Pre-create the deepest expected evidence path before the authoritative run. Use a short neutral evidence root if necessary, but do not introduce arm-specific path behavior.

## Runtime permission is a real status

If an automation environment cannot start a localhost listener, record `BLOCKED_RUNTIME_PERMISSION`; do not bypass policy or mutate network/security settings. A normally started pre-existing runtime can be measured when permitted.

## Preserve raw failures

Do not delete failed, slow, superseded or invalid batches. Store their role explicitly (`PILOT`, `PREAUDIT`, `SUPERSEDED`, `INVALID_ENVIRONMENT`, etc.) so later audits can distinguish evidence from authority.

## Do not optimize the test forever

Once a measurement gate is mature, freeze it. Only reopen the harness when new empirical evidence shows a real defect. The purpose of this skill is to shorten future setup by front-loading known failure checks, not to turn benchmark engineering into an endless project.
