# Completion Ledger Template

## purpose

Track every required item until complete, stopped, or explicitly waived.

## inputs

- declared requirements
- gates
- hard rules
- scripts
- final status codes

## forbidden scope

- PARTIAL final PASS
- COMPLETE without evidence

## gates

1. create ledger
2. map requirements
3. attach evidence
4. verify statuses
5. final aggregation

## required evidence

Each item needs:

- id
- requirement
- owner
- source
- evidence path
- script/checklist result
- status
- gap
- next action
- final pass eligibility

## script verification

Run completion-ledger verification or deterministic checklist.

## final status codes

- ECC_COMPLETION_LEDGER_100_PASS

## failure status codes

- ECC_COMPLETION_LEDGER_STOP
