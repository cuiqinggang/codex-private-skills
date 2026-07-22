# Declared Requirement 100 Template

## purpose

Ensure every written requirement enters the Completion Ledger and has evidence.

## inputs

- user request
- task package
- gates
- templates
- status code list

## forbidden scope

- treating written requirements as optional
- old PASS reuse

## gates

1. extract declared requirements
2. map to ledger
3. require evidence
4. validator review
5. orchestrator integration

## required evidence

- declared-requirements.json
- declared-requirements.md
- requirement-to-ledger map
- validator coverage review

## script verification

Run verify-declared-requirements or deterministic checklist.

## final status codes

- ECC_DECLARED_REQUIREMENT_100_PASS

## failure status codes

- ECC_DECLARED_REQUIREMENT_100_STOP
