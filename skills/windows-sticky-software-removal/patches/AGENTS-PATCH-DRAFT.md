# AGENTS.md Patch Draft: Sticky Windows Software Removal

When a Windows application is hard to uninstall, especially input methods, security suites, 360-like tools, shell extensions, proxy/network tools, drivers, or software whose uninstaller reports success but leaves files/processes behind, first reuse:

${REDACTED_SECRET}

Required behavior:

- Diagnose persistence layers before deleting files.
- Check package list, uninstall registry, processes, startup entries, services, tasks, user language list, TSF/CTF, COM/CLSID, and install directory.
- For IMEs, inspect and clean `Get-WinUserLanguageList` before file deletion.
- Do not shut down proxy/network clients such as FlClash without explicit user approval.
- If hot deletion fails on locked DLLs, use a SYSTEM startup task first; if that still fails, use `PendingFileRenameOperations`.
- Verify with logs and do not claim complete removal until the package, visible integration, processes, and directory are gone or boot deletion is scheduled.
