# Usage Log

## 2026-06-14

Created from Xunfei IME removal case.

Outcome:

- Normal uninstall reported success but left residues.
- User language list was cleaned to Microsoft Pinyin only.
- Xunfei package no longer appeared in winget.
- Startup SYSTEM cleanup ran but failed on locked `iFlyIMEQuickLaunch.dll`.
- `PendingFileRenameOperations` scheduled 72 child items plus target directory for next boot deletion.

Next related task must read this skill before attempting sticky Windows removal.

## 2026-06-14 Research Update

Added 360/security-suite reference layer after web research.

Key update:

- Security suites are treated as Level 4 sticky removal because they may include self-protection, services, drivers, browser/homepage hooks, and multiple related products.
- Official/community experience confirms reboot cleanup, Safe Mode deletion, and leftover scanning are common mature paths.

## 2026-06-14 360 Ecosystem Update

Added `sop/FULL-ECOSYSTEM-REMOVAL-MODEL.md`.

Core upgrade:

- Treat 360-like software as a connected ecosystem rather than one app.
- Inventory related products, services, drivers, tasks, shell/browser hooks, processes, folders, and registry before deletion.
- Remove in dependency order so one component cannot repair or revive another.
- Final verification must prove the ecosystem graph is broken, not only that one folder disappeared.

## 2026-06-14 Logic Update

Added backward-proof acceptance: final removal must be proven by package absence, integration absence, process non-revival, directory absence or boot-delete scheduling, and cleanup debt resolution. This prevents mistaking "command ran" for "software removed".
