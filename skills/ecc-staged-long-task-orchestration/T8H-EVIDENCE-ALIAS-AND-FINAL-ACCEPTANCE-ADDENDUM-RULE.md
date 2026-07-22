# T8H Evidence Alias And Final Acceptance Addendum Rule

## Purpose

The 2026-06-13 T8H recovery-mode pass exposed two evidence packaging risks:

1. expected file names and actual file names may differ;
2. Codex return packets may be non-path-only but still omit explicit GPT final
   acceptance request text.

## File Alias Rule

Prefer exact expected filenames. If an alias is used, create:

```text
evidence-alias-map.md
```

It must include:

```text
expected_file:
actual_file:
accepted_as_equivalent: true/false
reason:
verification_path:
```

Known 2026-06-13 example:

```text
expected_file: bad-case-test-result.json
actual_file: test-case-execution-result.json
accepted_as_equivalent: true
reason: contains valid_case_pass, bad_case_count, bad_cases_fail, failures, status_code
```

## Layer Filename Alias Rule

If layer files differ from canonical template names, create:

```text
filename-alias-map.md
```

Unstated aliases must not silently PASS when a verifier depends on fixed names.

## Codex Return Final Acceptance Rule

Codex evidence return packets must include:

```text
Request GPT final acceptance: YES
```

If the field is missing, generate:

```text
GPT-FINAL-ACCEPTANCE-ADDENDUM.md
GPT-FINAL-ACCEPTANCE-ADDENDUM.json
```

## Final Report Is Not Final Acceptance

Final reports, summaries, or path-only returns cannot replace:

```text
final-acceptance.md
final-acceptance.json
```

## Status Codes

```text
CODEX_RETURN_MUST_REQUEST_GPT_FINAL_ACCEPTANCE
GPT_FINAL_ACCEPTANCE_ADDENDUM_REQUIRED_IF_MISSING
BAD_CASE_RESULT_FILE_ALIAS_MUST_BE_DECLARED
LAYER_FILE_NAME_ALIAS_MUST_BE_DECLARED
FINAL_REPORT_ONLY_IS_NOT_FINAL_ACCEPTANCE
```
