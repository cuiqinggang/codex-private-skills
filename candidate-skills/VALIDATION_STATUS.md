# Windows reboot, uninstall, and VM skills — candidate status

Status: `HOLD_INSUFFICIENT_EVIDENCE`

These three packages are intentionally stored under `candidate-skills/`, not the active `skills/` directory:

- `resume-windows-task-after-reboot`
- `remove-stubborn-windows-software`
- `test-windows-software-safely`

## Completed evidence

- Skill structure validation: PASS for all three packages.
- Cross-platform fixture and negative tests: PASS / `STATIC_VERIFIED`.
- Tree-sitter PowerShell AST parse: PASS for all 9 PowerShell scripts.
- Independent security audit: `ACCEPT_STATIC` after two repair rounds.

## Mandatory VM evidence before promotion

Run only in a dedicated disposable Windows virtual machine. Never install 360 products on the host or a daily-use Windows system.

1. Validate Hyper-V prerequisites, Private/None network isolation, checkpoint creation, and verified restoration.
2. Run the harmless two-reboot fixture inside the guest and prove three distinct guest boot IDs, exact-once continuation, duplicate-start protection, bounded retry, and startup-hook cleanup.
3. Inject network loss, stale remote state, hash mismatch, duplicate startup, maximum-attempt, guest reboot timeout, network-adapter drift, payload failure, and failed-then-verified rollback cases.
4. In a fresh checkpointed guest, obtain 360安全卫士 and 360杀毒 only from their official sources, record versions, signatures, signer thumbprints, URLs, and SHA-256 values, and install both inside the guest.
5. Use exact registered/vendor uninstallers, cross-reboot continuation, baseline-bound residual inventory, and post-uninstall comparison. Check applications, processes, services, loaded drivers, scheduled tasks, startup entries, active network components, and executable remnants.
6. Accept only `ABSENT`, or explicitly report `KNOWN_VENDOR_RESIDUE`; any active or ambiguous evidence remains `ACTIVE_PRODUCT` or `UNKNOWN_BLOCKER`.
7. Restore the baseline checkpoint and verify the guest marker and both products are absent.

Promotion is forbidden until the full VM run produces reviewable evidence for every mandatory item. Static PASS is not completion.
