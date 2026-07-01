---
name: trusted-browser-download-install
description: Use when Codex must download an installer or executable from a trusted web page in a visible browser like a human, click the real download link, wait for browser download completion, verify source/file/hash/signature, avoid third-party bundled installers, install only after validation, and produce Chinese evidence reports.
---

# Trusted Browser Download Install

Use this skill when a task requires a visible browser download instead of direct CLI download, especially after direct download, API lookup, or package-manager install failed.

## Safety Boundary

- Prefer official vendor pages, official GitHub releases, Microsoft Store, or trusted package registries with exact package identity.
- Do not use search ads, Softonic, Uptodown, unofficial mirrors, forum attachments, cloud drives, bundled downloaders, or name-similar packages.
- Do not install until the downloaded file is validated as a real installer from the intended source.
- If the browser leaves only `.crdownload` files that stop growing, record a download failure instead of pretending it completed.
- If the installer shows NSIS/corruption/signature mismatch, stop and record evidence.
- Use Chinese for user-facing reports and screenshots pages.

## Workflow

1. Define the trusted source allowlist and the expected file pattern.
2. Open the source page in a headed browser.
3. Capture the source page screenshot before clicking.
4. Locate and click the real download link on the page. Prefer visible link text; fall back to exact allowlisted href.
5. Wait for the browser download object and for `.crdownload` files to disappear.
6. Validate the downloaded file:
   - file exists and size is reasonable;
   - extension matches the expected installer type;
   - file is not HTML/text;
   - Windows executable files start with `MZ`;
   - hash is recorded;
   - Authenticode signature is recorded when available.
7. Install only the validated file, then verify app executable, protocol, shortcut, launch, and task-specific evidence.
8. Produce Chinese HTML/JSON/Markdown evidence under the task workspace.

## Bundled Script

Use `scripts/trusted_browser_download.py` for the browser download and file validation stage.

Typical command:

```powershell
python C:\Users\A\.codex\skills\trusted-browser-download-install\scripts\trusted_browser_download.py `
  --page-url https://obsidian.md/download `
  --download-dir H:\AI\downloads\obsidian-official-browser `
  --evidence-dir H:\AI\workspaces\OBSIDIAN_APP_INSTALL_OR_RESTORE_PREREQUISITE_V1 `
  --allow-host github.com `
  --allow-host objects.githubusercontent.com `
  --allow-host release-assets.githubusercontent.com `
  --link-contains obsidianmd/obsidian-releases `
  --link-contains .exe `
  --expected-ext .exe `
  --min-bytes 50000000
```

If the script returns `DOWNLOAD_FAILED` or `DOWNLOAD_STALLED`, preserve the output JSON/HTML and try the next trusted source rather than using an untrusted mirror.
