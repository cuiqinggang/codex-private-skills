# P0 99 Certification Status — 2026-09-15

```text
P0_99_TIME_MS=NOT_CERTIFIED
CURRENT_CONFIRMED_P50_MS=41.5258
P0_99_P95_MS=NOT_CERTIFIED
CURRENT_CONFIRMED_P95_MS=58.000845
P0_MIN_MS=29.7895
P0_MAX_MS=71.9496
PREVIOUS_REFERENCE_MS=32.55975
IMPROVEMENT_PERCENT=-27.537220
CONTRACT_ID=P0-CONTROL-V2-CANDIDATE
BEST_IMPLEMENTATION=R6_SUCCESS_LOCAL_HISTORY_V2
AA_CALIBRATION=FAIL
CONFIRMATION_BATCH_1=R6-CONFIRMATION-1-20B-20260915; B=44.33395; EFFECT=11.451175; CI=[9.370775,13.531575]
CONFIRMATION_BATCH_2=R6-CONFIRMATION-2-20B-20260915; B=39.18285; EFFECT=8.465825; CI=[6.691,10.24065]
T_PHY_WORKING_RANGE_MS=28-33
PHYSICAL_GAP_MS=13.5258
UNTESTED_HIGH_VALUE_CANDIDATES=SERVER_TO_CLIENT_IN_MEMORY_OUTPUT_BYTES_NEW_CONTRACT
P0_99=NO
P0_FREEZE=NO
```

The pooled confirmation distribution contains 80 candidate runs from two independent
20-block ABBA/BAAB batches. All 160 measured A/B runs were valid. Every candidate
run matched the exact prompt, successful completed history, exactly one SaveImage
output, full PNG signature/chunk/CRC/zlib/size/SHA validation, and post-timing
HTTP/local byte equality.

## Calibration status

The final independent frozen-harness A/A is `a4/`: 160/160 valid, formal effect
`-1.469375 ms`, 95% CI `[-3.10655,0.1678]`, noise floor `1.637175 ms`,
order effect `2.60595 ms`, order CI `[-0.839375,5.72315]`. The frozen
environment-drift gate failed after a single large runtime tail contributed a
significant time trend, so `AA_CALIBRATION=FAIL` and `CANDIDATE_LOCK=ON`.

## Search result

- R1 HTTP history/view parallelism: 80/80 valid; effect `1.7572 ms`, CI
  `[-0.120775,3.635175]`; not retained.
- Existing local-file V2: 80/80 valid; effect `8.239325 ms`, CI
  `[5.27395,11.2047]`; all HTTP/local comparisons equal.
- R4 success→history→local: 80/80 valid; effect `5.75745 ms`, CI
  `[2.59985,8.91505]`.
- R6 success→local→history: search effect `16.25985 ms`, CI
  `[9.622,22.8977]`; confirmations remained positive with the CIs above.

R6 is a real relative improvement, not a certified absolute P0 99 result. Its two
confirmation candidate medians were `44.33395` and `39.18285 ms`, and their
pooled median is `41.5258 ms`, slower than the historical `32.55975 ms`
reference.

## Remaining architecture

In R6 search, median candidate segments were request→ack `6.4937 ms`,
ack→execution start `9.447 ms`, execution start→SaveImage executed
`7.135 ms`, save→success `0.81715 ms`, and success→result
`14.33105 ms`; local file open/read alone was `10.3341 ms`, history
`1.25545 ms`, and full PNG validation `0.59405 ms`.

The repeated confirmation minima `29.7895/30.2293 ms` support an engineering
working range of `28-33 ms` for the current file-backed architecture. Removing
the remaining file-publication/open cost requires a new server-to-client
in-memory output-bytes contract and a ComfyUI/server integration change. That is
not a low-risk client-only candidate and was not authorized or tested here.

