# v4.4.1 R1 Reality Delta

Observed on the real Windows host:

```text
REALITY_DELTA=RUNNER_ENCODING_PARSER_ERROR
STAGE=POWERSHELL_PARSE
REAL_VALIDATION_STARTED=NO
T_VALID_REAL=UNAVAILABLE
```

The remote R1 file is valid UTF-8, but the local temporary copy showed mojibake after the `git show | Set-Content` transfer path. This is an execution-wrapper delta, not a method-core delta.

Action:

```text
STOP
RETURN_TO_VIRTUAL
KEEP_METHOD=v4.4.1
PRESERVE_R1_AS_EVIDENCE
FREEZE_ASCII_ONLY_R2
```

R2 removes all non-ASCII script text and validates the foundation relationship using ASCII machine fields from the method manifest.
