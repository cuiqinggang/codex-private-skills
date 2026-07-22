# Artifact Checkpoint Closure Template

## purpose

Close generated artifacts, hashes, git state, and untracked file disposition.

## inputs

- generated files
- reports
- logs
- git status if repo

## forbidden scope

- untracked task artifacts hidden as residual risk
- missing manifest
- missing hash

## gates

1. capture artifact inventory
2. capture git status
3. classify untracked files
4. create artifact manifest
5. create sha256 manifest
6. validator review
7. orchestrator integration

## required evidence

- artifact-manifest
- sha256-manifest
- untracked disposition
- checkpoint method

## script verification

Run artifact checkpoint verification or deterministic checklist.

## final status codes

- ECC_ARTIFACT_CHECKPOINT_CLOSURE_PASS

## failure status codes

- ECC_ARTIFACT_CHECKPOINT_CLOSURE_STOP
