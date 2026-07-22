# Mechanical Drive Heat Diagnostic Checklist

Use when a mechanical drive is hot, noisy, spinning, or unexpectedly active.

## Diagnose

- Identify disk number, model, serial, media type, size, and drive letters.
- Check whether the drive has old Windows/system folders or boot partitions.
- Sample disk I/O for 3-5 seconds or longer if needed.
- List processes whose executable path or command line references non-C drives.
- List scheduled tasks and startup commands referencing non-C drives.
- Check services referencing non-C drives.
- Check pagefile and temp paths.
- Check indexing/search/sync/backup jobs.
- Check app-specific output/input/temp/cache settings.
- Check disk idle timeout.

## Fix Safely

- Move future runtime paths to `C:` when safe.
- Stop current non-C leaking processes only when they are clearly from old runtime paths.
- Disable or repair old scheduled tasks when permitted.
- Shorten idle disk timeout if the user wants the drive to cool down.
- Do not delete data, format partitions, or remove drive letters without explicit approval.

## Report

- Explain root cause in plain language.
- Separate fixed items from residual permission blockers.
- Include verification: process scan, disk I/O sample, script/config path check.

