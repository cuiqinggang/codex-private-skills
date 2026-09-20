# Frozen Runtime Spec — PE-P0 v3.1.6 Extreme-01

## Build-time
- Keep current Windows/proxy environment unchanged.
- Pin a Node-compatible stable Undici line; use Pool/request.
- Generate/bundle schema validator before runtime; no runtime schema compilation.
- Never pre-read/cache benchmark task contents, answers, oracle, or executor outcomes in the engine.

## Before T0
Allowed generic infrastructure:
- load model/endpoint/action ontology templates;
- create one OpenRouter Pool with exactly 2 persistent connections, pipelining=1;
- warm both connections using generic auth/schema probes containing no benchmark content;
- preload private oracle only inside verifier harness; engine cannot read it.

## T0 hot path
input release → read/parse → standalone validate → build 20 units → LPT 2-way pack → serialize projected bodies → concurrent 2 requests → per-shard early release → actions/dependency lookup → single receipt log → final gate → manifest → T1.

### Semantic units
- items 01–16: one current-action Choice each.
- four indivisible bundles: (17 + all 21 branch policies), (18 + 22), (19 + 23), (20 + 24).

### Projection
Each shard state includes:
- action ontology once;
- only referenced items;
- for each item only request/evidence/constraints.
Constant PENDING state, identical allowed_actions and dependency structure encoded by the question/unit graph are not repeated.

### Questions
Current: Choose the permitted action for `items.<id>` now.
Branch: If `dependency.result` is <SUCCESS|FAIL_TEMP|FAIL_PERM>, choose the permitted action for `items.<id>`.
Criteria point to `actions.EXECUTE/HOLD/ROUTE/REJECT`.

### Packing
After T0, compute each whole unit's serialized byte weight, sort descending, assign each to the currently lighter of exactly two shards. No oracle/answer data participates.

### Scheduler
Never wait for both model requests before action execution.
A shard continuation parses its own answers and immediately executes its own actions.
Each predecessor bundle contains its dependent branch answers, so real receipt selects an already-returned policy in O(1).

### Receipts / verifier
- immutable in-memory receipts;
- one append-only JSONL log, not 24 files;
- incremental deterministic verification;
- one final global barrier;
- one final manifest write.

## Real verify contract
One topology only: frozen s2.
3 warmups; 30 measured.
30/30 PASS and min < 840.6046999999962 ms required.
No executor optimization or fallback.
