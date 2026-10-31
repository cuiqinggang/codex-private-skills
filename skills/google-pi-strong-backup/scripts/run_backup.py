"""Delegate to the versioned installed Windows strong-backup entry."""
from pathlib import Path
import subprocess
import sys
ENTRY = Path(r'C:\Users\A\Documents\DSH-Workspace\gsb-pi-google-v2-20261031\run_backup.py')
if not ENTRY.is_file():
    raise SystemExit('BLOCKED: installed Windows Pi strong-backup entry is unavailable')
raise SystemExit(subprocess.call([sys.executable, str(ENTRY), *sys.argv[1:]]))
