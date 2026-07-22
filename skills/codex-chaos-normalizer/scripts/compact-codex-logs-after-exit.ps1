param(
${REDACTED_SECRET}
  [int]$RetentionDays = 3,
  [string]$StatusPath = ''
)

$ErrorActionPreference = 'Stop'
if (-not $StatusPath) {
  $StatusPath = Join-Path (Join-Path $CodexHome 'repair-logs') 'compact-codex-logs-after-exit.status.txt'
}
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $StatusPath) | Out-Null
function Write-Status($Message) {
  $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $Message"
  $line | Tee-Object -FilePath $StatusPath -Append
}

Write-Host "Waiting for Codex.exe/codex.exe to exit before compacting logs..."
Write-Status "waiting_for_codex_exit retention_days=$RetentionDays codex_home=$CodexHome"
while (Get-Process Codex,codex -ErrorAction SilentlyContinue) {
  Start-Sleep -Seconds 2
}
Write-Status 'codex_exited_begin_compaction'

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$archive = Join-Path $CodexHome "logs-archive-$stamp"
New-Item -ItemType Directory -Force -Path $archive | Out-Null

$db = Join-Path $CodexHome 'logs_2.sqlite'
$tmp = Join-Path $CodexHome 'logs_2.compact.sqlite'
if (-not (Test-Path -LiteralPath $db)) {
  Write-Host "No logs_2.sqlite found."
  Write-Status 'no_logs_2_sqlite_found'
  exit 0
}

foreach ($name in 'logs_2.sqlite-wal','logs_2.sqlite-shm') {
  $p = Join-Path $CodexHome $name
  if (Test-Path -LiteralPath $p) {
    Move-Item -LiteralPath $p -Destination (Join-Path $archive $name) -Force
  }
}

Copy-Item -LiteralPath $db -Destination (Join-Path $archive 'logs_2.sqlite.original') -Force
if (Test-Path -LiteralPath $tmp) {
  Remove-Item -LiteralPath $tmp -Force
}

$py = @"
import os, sqlite3, time
src = os.environ["CODEX_LOG_SOURCE"]
dst = os.environ["CODEX_LOG_DEST"]
days = int(os.environ.get("CODEX_LOG_RETENTION_DAYS", "3"))
cutoff = int(time.time()) - days * 86400
s = sqlite3.connect("file:" + src + "?mode=ro", uri=True)
d = sqlite3.connect(dst)
d.executescript("""
CREATE TABLE _sqlx_migrations (
    version BIGINT PRIMARY KEY,
    description TEXT NOT NULL,
    installed_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN NOT NULL,
    checksum BLOB NOT NULL,
    execution_time BIGINT NOT NULL
);
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts INTEGER NOT NULL,
    ts_nanos INTEGER NOT NULL,
    level TEXT NOT NULL,
    target TEXT NOT NULL,
    feedback_log_body TEXT,
    module_path TEXT,
    file TEXT,
    line INTEGER,
    thread_id TEXT,
    process_uuid TEXT,
    estimated_bytes INTEGER NOT NULL DEFAULT 0
);
""")
for row in s.execute("select version, description, installed_on, success, checksum, execution_time from _sqlx_migrations"):
    d.execute("insert into _sqlx_migrations values (?,?,?,?,?,?)", row)
cols = "id,ts,ts_nanos,level,target,feedback_log_body,module_path,file,line,thread_id,process_uuid,estimated_bytes"
count = 0
for row in s.execute(f"select {cols} from logs where ts >= ? order by id", (cutoff,)):
    d.execute(f"insert into logs ({cols}) values (?,?,?,?,?,?,?,?,?,?,?,?)", row)
    count += 1
if count:
    seq = d.execute("select max(id) from logs").fetchone()[0]
    d.execute("insert into sqlite_sequence(name,seq) values('logs',?)", (seq,))
d.commit()
d.execute("vacuum")
d.close()
s.close()
print(f"kept_rows={count} cutoff={cutoff}")
"@

$env:CODEX_LOG_SOURCE = $db
$env:CODEX_LOG_DEST = $tmp
$env:CODEX_LOG_RETENTION_DAYS = [string]$RetentionDays
$py | python -

Move-Item -LiteralPath $db -Destination (Join-Path $archive 'logs_2.sqlite.replaced') -Force
Move-Item -LiteralPath $tmp -Destination $db -Force
Write-Host "Compacted logs_2.sqlite with RetentionDays=$RetentionDays; archive=$archive"
Write-Status "done archive=$archive"
