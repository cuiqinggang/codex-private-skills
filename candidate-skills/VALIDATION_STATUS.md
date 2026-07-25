# Windows reboot, uninstall, and VM skills — candidate status

Status: `PACKAGED_TESTING_DEFERRED`

The three skill packages are complete and intentionally stored under `candidate-skills/`, not the active `skills/` directory:

- `resume-windows-task-after-reboot`
- `remove-stubborn-windows-software`
- `test-windows-software-safely`

## Packaging evidence

- Skill structure validation: PASS for all three packages.
- Reusable scripts, safety contracts, UI metadata, and upstream attribution are included.
- The reboot-resume package now has a task-agnostic Loop adapter contract.
- `Invoke-TwoRebootLoopFixture.ps1` defines a bounded two-reboot Loop fixture with `LOOP-CONTRACT.json`, `STATE.json`, and `RUN-LOG.jsonl`.
- The fixture never reboots the host or guest itself; an external VM controller must perform each guest reboot.
- Earlier cross-platform fixture checks and PowerShell parsing remain historical candidate evidence.

## Deferred by user instruction

No runtime, VM, reboot, software-installation, software-removal, or 360 test is being run in this packaging phase. The packages must not be described as runtime-verified or promoted to active skills from this status.

## Later validation gates

1. Run the harmless two-reboot Loop fixture in a disposable VM and prove three distinct guest boot IDs, exactly two reboot requests, exact-once continuation, bounded retry, final `CLOSED`, and startup-hook cleanup.
2. Validate isolated VM preparation, checkpoint creation, evidence collection, and verified restoration.
3. Only if separately authorized later, test 360安全卫士 and 360杀毒 inside a dedicated disposable Windows VM; never install them on the host or a daily-use system.
4. Promote only after the selected runtime scope has reviewable evidence and its remaining platform limitations are stated explicitly.

Packaging completion is not runtime completion.
