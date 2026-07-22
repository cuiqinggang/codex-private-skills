# AGENTS.md Patch Draft

## C Drive Hotpath Default

- Default all local app runtime, saves, generated outputs, caches, temp directories, virtual environments, logs, scheduled tasks, Codex work, Knowledge Brain hot paths, CodeGraph hot scans, and AI tool working folders to the system SSD on `C:`.
- Treat `D:`, `H:`, and `K:` as ordinary mechanical, backup, reference, disaster-recovery, archive, or cold-storage drives unless the user explicitly asks to use them.
- Before starting long-running local workflows, check command lines, scheduled tasks, pagefile/temp paths, and app output/input/temp/cache settings for unintended non-C paths.
- Do not delete, format, repartition, move large data, or remove drive letters without explicit user approval.
- For cross-drive migrations, inspect reparse points and explicitly scan the authoritative data root; never treat a drive-root recursive scan returning zero as sufficient proof of no candidate.
- Persist core migration results before optional Git/CodeGraph probes, and handle expected native-command nonzero exits as non-fatal capability results.
${REDACTED_SECRET}
