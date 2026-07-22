# Acceptance Gate

PASS is allowed only when:

- formal business skills modified: NO,
- accepted/rejected/needs-human buffers exist,
- rejected buffer is preserved,
- do-not-auto-optimize list is present,
- runtime gate applies when the run claims 30min/2H/4H/8H,
- runtime-evidence.json exists for runtime runs,
- checkpoint timeline exists for runtime runs,
- verify-runtime-gate.mjs passes for runtime runs,
- clickable acceptance page exists,
- no auto-merge occurred.

If a runtime run finishes early, mark FAIL or PARTIAL.

If a patch install finishes quickly, it may pass as `PATCH_INSTALL_PASS`, not as runtime PASS.

