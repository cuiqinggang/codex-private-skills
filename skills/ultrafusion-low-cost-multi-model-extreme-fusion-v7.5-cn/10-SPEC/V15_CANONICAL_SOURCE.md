# V15 Canonical Source

Status: active canonical source
Date: 2026-07-05

## Canonical File

Use this file as the current full V15 source for UltraFusion V7.0 ABCD prompt packages:

```text
${REDACTED_SECRET}
```

Validation:

- Size: 13292 bytes
- Lines: 333 by PowerShell split; 332 content lines before final trailing newline
- SHA256: `BB836AC959885190A1BEC81ECA77454F0CD183D08BB3814070A977C39147514E`
- Contains: `V15+G 前置约束层`, `Auto-V15`, `V15 瀑布式`, and `自适应字数规范 v3.0`

## User Recovery Attachment

The user supplied a recovery copy:

```text
${REDACTED_SECRET}
```

Validation:

- Size: 13290 bytes
- Lines: 332
- SHA256: `2950780DA16BDFCA8CA61D204F200F7A3E7AC161D623C15ED8793F752A4718BE`
- Trimmed text match with the canonical file: `true`

## Binding Rule

For UltraFusion V7.0 full ABCD runs, every A/B/C/D package must inject the canonical V15 text verbatim. A short summary, placeholder, compressed V15, or rewritten V15 is invalid.

Invalid package codes:

```text
A_PACKAGE_INVALID_V15_MISSING
A_PACKAGE_INVALID_WRONG_V15_VERSION
UF_PROMPT_ASSEMBLY_FAIL: V15_FULL_MISSING
UF_PROMPT_ASSEMBLY_FAIL: V15_CANONICAL_SOURCE_NOT_USED
UF_PROMPT_ASSEMBLY_FAIL: V15_PLACEHOLDER_NOT_REPLACED
```

If a later better or more complete V15 source is found, add it as a new versioned source file and update this pointer only after comparison evidence is recorded.
