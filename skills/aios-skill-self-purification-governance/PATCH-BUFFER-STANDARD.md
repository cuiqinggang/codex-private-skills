# Patch Buffer Standard

Every proposed edit must enter exactly one category.

## ACCEPTED_CANDIDATE

Means the candidate passed screening. It does not mean it has been merged.

Allowed when the edit:

- reduces duplication,
- preserves hard rules,
- improves executability,
- strengthens acceptance or safety,
- is low risk or reversible,
- does not make a skill into a giant prompt.

## REJECTED_EDIT

Must be kept in the rejected buffer so future runs do not propose the same bad change again.

Reject edits that:

- delete failure reviews,
- delete visual evidence rules,
- delete 12 Layer, checkpoint, or safety gates,
- make rules vague,
- only reword without benefit,
- increase text while weakening constraints,
- introduce auto-overwrite risk.

## NEEDS_HUMAN_REVIEW

Requires the user or GPT Gate Review. It cannot be automatically merged.

Use this for:

- deleting historical experience,
- renaming a skill,
- merging skills,
- changing orchestrator triggers,
- high-risk system operations,
- aesthetic tradeoffs,
- long-term direction changes.

