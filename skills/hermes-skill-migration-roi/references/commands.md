# Commands

${REDACTED_SECRET}

## G01/G02 refresh ROI classification

```powershell
${REDACTED_SECRET}
```

Success criteria:

- Prints `ROI_CLASSIFICATION_PASS`.
- `roi-111-classification.csv` contains 111 rows.
- `roi-summary.md` exists.

## Inspect counts

```powershell
${REDACTED_SECRET}
```

## Inspect rewrite shortlist

```powershell
${REDACTED_SECRET}
```

## Verify active Hermes visibility

```powershell
& "H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe" skills list --source local
```

Success criteria:

- The command exits with code 0.
- `hermes-skill-migration-roi` appears in the local skill list.

## Delete gate

Do not run delete commands from this skill unless the user explicitly approves a reviewed manifest. Deletion is a separate high-risk gate.
