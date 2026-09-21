# Codex Post-Run Verify — no credential access

Use only after the user has manually run the frozen v0.5.0 candidate runner in their own PowerShell.

Codex must:
1. make no API call;
2. read no credential or environment variable;
3. not modify candidate, runner, result, benchmark, model, or gate;
4. execute only `verify-frozen-v050-result.ps1`;
5. return its final summary;
6. STOP whether PASS or FAIL.

This is evidence verification only.
