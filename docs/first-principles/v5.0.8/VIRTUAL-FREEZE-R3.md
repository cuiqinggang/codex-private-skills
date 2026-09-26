# v5.0.8 R3 Git native bytes materialization freeze

FREEZE_ID=ESTE-v5.0.8-GIT-NATIVE-BYTES-MATERIALIZATION-VIRTUAL-FREEZE-R3

The R2 Reality Capsule remains byte-for-byte immutable at Git blob
b265043bc4dac9ee2ca45057fcca18e451c51e25. The R2 set of 22 frozen
assets remains unchanged. R3 adds five assets for the materialization contract,
runtime, tests, maturity report, and this freeze record.

The normal source remains the shared private repository. Git fetch of the
specified branch populates the native object database. The R3 runtime uses
subprocess arguments, shell=False, text=False, and raw stdout bytes. Before
any later Reality timing it checks the Git blob SHA, ASCII-only bytes,
compile(bytes), fresh namespace exec, and callable certificate entry point.

Implementation validation:
- Exact frozen blob materialization: 1000/1000 PASS
- Wrong existing blob: 100/100 BLOCK
- Frozen source blob: MATCH
- ASCII-only, compile, fresh namespace exec, callable entry: PASS
- Host JavaScript encoding dependency: 0
- PowerShell source text recoding dependency: 0

The Reality Certificate was not called in task 03-01.
The original state machine and T*=min(T_VALID) remain unchanged.
Formal Reality requires a subsequent GPT dispatch after R3 Freeze reread.
