# Candidate Patch Format

Each candidate patch must include:

- `patch_id`
- `skill_name`
- `file_path`
- `edit_type`: `ADD`, `DELETE`, or `REPLACE`
- `original_text`
- `proposed_text`
- `why`
- `expected_improvement`
- `risk_level`: `LOW`, `MEDIUM`, or `HIGH`
- `should_accept`: `YES`, `NO`, or `NEEDS_HUMAN`
- `validation_checklist`

Reject edits when they:

- weaken user hard rules,
- remove final acceptance,
- remove failure history,
- automate destructive actions,
- broaden skill triggers too much,
- create a larger prompt without real benefit,
- cannot be validated.
