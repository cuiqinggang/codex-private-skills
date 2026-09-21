# Codex Post-Run Verify — JEV P0 v0.5.1

Use only after the user has run the frozen v0.5.1 runner in their own PowerShell.

Codex must:
1. make no API call;
2. read no credential or environment variable;
3. not modify candidate, runner, result, benchmark, model, criteria, or gate;
4. execute only `verify-frozen-v051-result.ps1`;
5. return its final summary;
6. STOP whether PASS or FAIL.

No design authority.
