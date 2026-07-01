# Commands

Run these from `C:\Users\A\Desktop\1` in Windows PowerShell.

## G01/G02 refresh ROI classification

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\A\Desktop\1\output\hermes-wsl-openclaw-roi-20260519\build-roi-classification.ps1"
```

Success criteria:

- Prints `ROI_CLASSIFICATION_PASS`.
- `roi-111-classification.csv` contains 111 rows.
- `roi-summary.md` exists.

## Inspect counts

```powershell
Import-Csv "C:\Users\A\Desktop\1\output\hermes-wsl-openclaw-roi-20260519\roi-111-classification.csv" | Group-Object ROIClass | Select-Object Name,Count
```

## Inspect rewrite shortlist

```powershell
Import-Csv "C:\Users\A\Desktop\1\output\hermes-wsl-openclaw-roi-20260519\rewrite-shortlist.csv" | Select-Object Priority,SkillName,FrontmatterName,RewriteCostScore,RecommendedAction
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
