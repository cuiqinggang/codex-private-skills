# Cleanup Decision Matrix

## Safe By Default

Clean these when the user asks for C drive cleanup and the scan confirms meaningful size:

${REDACTED_SECRET}
- Browser cache folders
- pip/npm cache
- Crash dumps
- Windows Error Reporting files
- Recycle Bin, when the user's intent is broad cleanup

## Review Only

Do not delete automatically. Show size, top items, and likely meaning:

- Desktop
- Downloads
- Documents
- Codex workspaces
- `.codex`
- Skills, reports, knowledge brain, Obsidian vaults
- ComfyUI, Stable Diffusion, generated media, project folders

## Inspect Before Action

Only prune after listing contents and explaining impact:

- Docker images
- Docker containers
- Docker volumes
- AI model stores
- Databases
- Virtual environments
- Package stores such as pnpm

## Migration-Specific Check

For HDD-to-SSD system migration, always compare:

- Source disk size
- Source C partition size
- Used C data
- Target SSD size
- EFI/System partitions

If used data fits but the partition is larger than the SSD, recommend a resize-aware migration tool or shrink the C partition before cloning.
