#!/usr/bin/env python3
"""N001: consistent MySQL backup, isolated restore, and optional DB crash probe.

No packages, host credentials, source-schema writes, or active restart commands.
The only optional fault is docker kill --signal KILL of the verified N001 DB.
All backup bytes and reports stay on the Windows machine under --root.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

PROJECT = "n001-rental"
SOURCE_SCHEMA = "rental_n001"
TABLES = ("products", "customers", "reservations", "reservation_items", "payments", "reservation_activity")
IDENTIFIER = re.compile(r"^[A-Za-z0-9_]+$")


class ProbeError(RuntimeError):
    pass


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds")


def sha_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def quoted(identifier):
    if not IDENTIFIER.fullmatch(identifier):
        raise ProbeError("Unexpected SQL identifier; refusing interpolation")
    return "`" + identifier + "`"


class Probe:
    def __init__(self, root, timeout):
        self.root = root.resolve()
        self.timeout = timeout
        self.docker = shutil.which("docker")
        if not self.docker:
            raise ProbeError("Docker CLI is not available")
        for filename in ("db.env", "compose.n001.yml"):
            if not (self.root / filename).is_file():
                raise ProbeError("Required task file is missing: " + filename)
        self.compose = [self.docker, "compose", "-p", PROJECT, "--env-file", str(self.root / "db.env"),
                        "-f", str(self.root / "compose.n001.yml")]
        self.backups = self.root / "backups"
        self.backups.mkdir(parents=True, exist_ok=True)
        result = self.run(self.compose + ["ps", "-q", "db"], "discover_db").decode().split()
        if len(result) != 1 or not re.fullmatch(r"[a-f0-9]{12,64}", result[0]):
            raise ProbeError("Expected exactly one running DB container for the dedicated task")
        self.container = result[0]
        labels = json.loads(self.inspect("{{json .Config.Labels}}"))
        if labels.get("com.docker.compose.project") != PROJECT or labels.get("com.docker.compose.service") != "db":
            raise ProbeError("Container labels do not match the dedicated N001 DB; refusing")
        self.metadata = {}

    def run(self, command, stage, *, input_bytes=None, stdin_file=None, stdout_file=None, timeout=None):
        # Never print docker exec commands, environment variables, SQL result rows, or stderr.
        try:
            result = subprocess.run(command, input=input_bytes, stdin=stdin_file,
                                    stdout=stdout_file if stdout_file is not None else subprocess.PIPE,
                                    stderr=subprocess.PIPE, timeout=timeout or self.timeout, check=False)
        except subprocess.TimeoutExpired:
            raise ProbeError(stage + " timed out") from None
        except OSError:
            raise ProbeError(stage + " could not launch") from None
        if result.returncode:
            stderr_digest = hashlib.sha256(result.stderr or b"").hexdigest()
            raise ProbeError(f"{stage} failed: exit={result.returncode}; stderr_sha256={stderr_digest}")
        return result.stdout or b""

    def inspect(self, template):
        return self.run([self.docker, "inspect", "--format", template, self.container], "inspect_db").decode().strip()

    def state(self):
        # Restrict inspection fields: full docker inspect includes secret environment values.
        template = ('{"running":{{json .State.Running}},"status":{{json .State.Status}},'
                    '"exit_code":{{json .State.ExitCode}},"started_at":{{json .State.StartedAt}},'
                    '"restart_count":{{json .RestartCount}},"restart_policy":{{json .HostConfig.RestartPolicy.Name}}}')
        return json.loads(self.inspect(template))

    def mysql_command(self, schema=None):
        command = [self.docker, "exec", "-i", self.container, "sh", "-c",
                   'test -n "$MYSQL_ROOT_PASSWORD" || exit 65; '
                   'export MYSQL_PWD="$MYSQL_ROOT_PASSWORD"; '
                   'exec mysql -uroot --batch --raw --skip-column-names --binary-mode '
                   '--default-character-set=utf8mb4 "$@"', "mysql"]
        if schema is not None:
            quoted(schema)
            command.append("--database=" + schema)
        return command

    def sql(self, sql, schema=None, stage="mysql_query", stdout_file=None, timeout=None):
        return self.run(self.mysql_command(schema), stage, input_bytes=sql.encode("utf-8"),
                        stdout_file=stdout_file, timeout=timeout)

    def load_metadata(self):
        table_list = ",".join("'"+table+"'" for table in TABLES)
        sql = ("SELECT TABLE_NAME,COLUMN_NAME,ORDINAL_POSITION FROM information_schema.COLUMNS "
               f"WHERE TABLE_SCHEMA='{SOURCE_SCHEMA}' AND TABLE_NAME IN ({table_list}) "
               "ORDER BY TABLE_NAME,ORDINAL_POSITION;\n"
               "SELECT CONCAT('PK:',TABLE_NAME),COLUMN_NAME,SEQ_IN_INDEX FROM information_schema.STATISTICS "
               f"WHERE TABLE_SCHEMA='{SOURCE_SCHEMA}' AND TABLE_NAME IN ({table_list}) "
               "AND INDEX_NAME='PRIMARY' ORDER BY TABLE_NAME,SEQ_IN_INDEX;")
        for row in self.sql(sql, stage="read_schema_metadata").decode().splitlines():
            fields = row.split("\t")
            if len(fields) != 3:
                raise ProbeError("Unexpected schema metadata format")
            table, column, _ordinal = fields
            primary = table.startswith("PK:")
            if primary:
                table = table[3:]
            if table not in TABLES:
                raise ProbeError("Unexpected metadata table")
            quoted(column)
            info = self.metadata.setdefault(table, {"columns": [], "primary_key": []})
            info["primary_key" if primary else "columns"].append(column)
        if set(self.metadata) != set(TABLES) or any(not item["primary_key"] for item in self.metadata.values()):
            raise ProbeError("All six business tables and their primary keys are required")
        # A source-qualified trigger could write back into the original schema on restore.
        triggers = int(self.sql("SELECT COUNT(*) FROM information_schema.TRIGGERS "
                                f"WHERE TRIGGER_SCHEMA='{SOURCE_SCHEMA}';", stage="check_trigger_scope").strip())
        if triggers:
            raise ProbeError("Source has triggers; isolated trigger restoration needs separate review")

    def snapshot(self, schema, stage):
        statements = ["SET SESSION time_zone='+00:00';",
                      "SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;",
                      "START TRANSACTION WITH CONSISTENT SNAPSHOT;"]
        for table in TABLES:
            info = self.metadata[table]
            # Every non-null value is binary-cast then hex encoded; NULL has its own marker.
            # This avoids delimiter, newline, locale, JSON, and binary-value ambiguity.
            values = [f"IF({quoted(column)} IS NULL,'N',CONCAT('H',HEX(CAST({quoted(column)} AS BINARY))))"
                      for column in info["columns"]]
            expression = "CONCAT_WS(':'," + ",".join(values) + ")"
            ordering = ",".join(quoted(column) for column in info["primary_key"])
            statements += [f"SELECT 'N001_BEGIN_{table}';",
                           f"SELECT {expression} FROM {quoted(schema)}.{quoted(table)} ORDER BY {ordering};",
                           f"SELECT 'N001_END_{table}';"]
        statements.append("COMMIT;")
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=self.backups, prefix="snapshot-", suffix=".tmp", delete=False) as file:
                temporary = Path(file.name)
                self.sql("\n".join(statements), stage=stage, stdout_file=file)
            result, current, digest, count = {}, None, None, 0
            with temporary.open("rb") as file:
                for raw in file:
                    row = raw.rstrip(b"\r\n")
                    if row.startswith(b"N001_BEGIN_"):
                        if current is not None:
                            raise ProbeError("Nested snapshot marker")
                        current = row.decode()[len("N001_BEGIN_"):]
                        if current not in TABLES or current in result:
                            raise ProbeError("Unexpected snapshot marker")
                        digest = hashlib.sha256()
                        digest.update(json.dumps(self.metadata[current], sort_keys=True, separators=(",", ":")).encode())
                        digest.update(b"\n")
                        count = 0
                    elif row.startswith(b"N001_END_"):
                        if current is None or row.decode() != "N001_END_"+current:
                            raise ProbeError("Mismatched snapshot marker")
                        result[current] = {"rows": count, "sha256": digest.hexdigest()}
                        current, digest = None, None
                    else:
                        if current is None or not re.fullmatch(rb"(?:N|H[0-9A-F]*)(?::(?:N|H[0-9A-F]*))*", row):
                            raise ProbeError("Noncanonical snapshot row")
                        digest.update(row+b"\n")
                        count += 1
            if current is not None or set(result) != set(TABLES):
                raise ProbeError("Incomplete business snapshot")
            aggregate = hashlib.sha256(json.dumps(result, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            return {"tables": result, "sha256": aggregate}
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()

    def check_tables(self, schema, stage):
        output = self.sql("CHECK TABLE "+",".join(quoted(schema)+"."+quoted(t) for t in TABLES)+";", stage=stage).decode()
        results = {}
        for row in output.splitlines():
            fields = row.split("\t", 3)
            if len(fields) != 4:
                raise ProbeError("Unexpected CHECK TABLE result")
            full_table, _operation, message_type, message = fields
            table = full_table.split(".")[-1]
            if table not in TABLES:
                raise ProbeError("Unexpected CHECK TABLE name")
            if message_type == "status" and message == "OK":
                results[table] = "OK"
            elif message_type in ("error", "warning"):
                raise ProbeError("CHECK TABLE failed for " + table)
        if set(results) != set(TABLES):
            raise ProbeError("CHECK TABLE did not confirm all six tables")
        return results

    def backup(self, destination):
        command = [self.docker, "exec", self.container, "sh", "-c",
                   'test -n "$MYSQL_ROOT_PASSWORD" || exit 65; '
                   'export MYSQL_PWD="$MYSQL_ROOT_PASSWORD"; exec mysqldump -uroot "$@"', "mysqldump",
                   "--single-transaction", "--skip-lock-tables", "--no-tablespaces", "--hex-blob",
                   "--set-gtid-purged=OFF", "--default-character-set=utf8mb4", SOURCE_SCHEMA]
        temporary = destination.with_suffix(".sql.partial")
        try:
            with temporary.open("xb") as file:
                self.run(command, "consistent_mysqldump", stdout_file=file)
                file.flush()
                os.fsync(file.fileno())
            if temporary.stat().st_size == 0:
                raise ProbeError("Backup is empty")
            # --databases is never used; refuse an unexpected USE/CREATE DATABASE before restore.
            with temporary.open("rb") as file:
                for line in file:
                    if re.match(rb"\s*(USE\s|CREATE\s+DATABASE\b)", line, flags=re.I):
                        raise ProbeError("Backup unexpectedly switches database; refusing restore")
            os.replace(temporary, destination)
        except BaseException:
            if temporary.exists():
                temporary.unlink()
            raise
        return {"file": str(destination), "bytes": destination.stat().st_size, "sha256": sha_file(destination)}

    def restore(self, backup, schema):
        self.sql("CREATE DATABASE "+quoted(schema)+" CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;",
                 stage="create_isolated_restore_schema")
        with backup.open("rb") as file:
            self.run(self.mysql_command(schema), "restore_into_isolated_schema", stdin_file=file)


def health(url):
    try:
        request = urllib.request.Request(url, headers={"Cache-Control": "no-cache", "Accept": "application/json"})
        with urllib.request.urlopen(request, timeout=3) as response:
            data = json.loads(response.read(16384))
            return response.status == 200 and isinstance(data, dict) and data.get("status") == "healthy"
    except (OSError, ValueError, urllib.error.URLError):
        return False


def crash_probe(probe, health_url, wait_seconds):
    before = probe.state()
    if before["restart_policy"] != "unless-stopped" or not before["running"]:
        raise ProbeError("Crash probe requires the verified DB already running with unless-stopped")
    if not health(health_url):
        raise ProbeError("Health API is not healthy before fault injection; refusing to kill")
    baseline = probe.snapshot(SOURCE_SCHEMA, "snapshot_before_kill")
    result = {"fault": "docker kill --signal KILL", "container_id": probe.container,
              "state_before": before, "before": baseline, "active_restart_commands": 0,
              "automatic_recovery_observed": False, "started_at_utc": utc()}
    started = time.perf_counter()
    probe.run([probe.docker, "kill", "--signal", "KILL", probe.container], "kill_dedicated_db")
    deadline = started + wait_seconds
    db_ready = None
    while time.perf_counter() < deadline:
        try:
            current = probe.state()
            restarted = current["running"] and current["started_at"] != before["started_at"]
            if restarted:
                probe.sql("SELECT 1;", SOURCE_SCHEMA, stage="poll_db_after_kill", timeout=5)
                if db_ready is None:
                    db_ready = time.perf_counter() - started
                if health(health_url):
                    result.update(automatic_recovery_observed=True, db_ready_seconds=round(db_ready, 3),
                                  health_ready_seconds=round(time.perf_counter()-started, 3), state_after=current)
                    after = probe.snapshot(SOURCE_SCHEMA, "snapshot_after_automatic_recovery")
                    result["after"] = after
                    result["business_hash_unchanged"] = after == baseline
                    result["integrity"] = probe.check_tables(SOURCE_SCHEMA, "check_after_automatic_recovery")
                    result["passed"] = after == baseline
                    result["finished_at_utc"] = utc()
                    return result
        except ProbeError:
            pass
        time.sleep(0.5)
    result.update(passed=False, elapsed_seconds=round(time.perf_counter()-started, 3),
                  failure="No automatic DB plus API recovery observed; no restart was attempted",
                  state_after=probe.state(), finished_at_utc=utc())
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path, help="Task directory containing db.env and compose.n001.yml")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--command-timeout", type=int, default=180)
    parser.add_argument("--kill-db", action="store_true", help="Opt-in: kill only verified DB; observe, never actively restart")
    parser.add_argument("--health-url", help="Local Louez /api/health URL, required with --kill-db")
    parser.add_argument("--recovery-timeout", type=int, default=120)
    args = parser.parse_args()
    if args.command_timeout < 5 or args.recovery_timeout < 5:
        parser.error("Timeouts must be at least five seconds")
    if args.kill_db:
        parsed = urllib.parse.urlsplit(args.health_url or "")
        if parsed.scheme != "http" or parsed.hostname not in ("127.0.0.1", "localhost") or parsed.path != "/api/health" or parsed.username:
            parser.error("--kill-db requires a local http://127.0.0.1:PORT/api/health URL")
    root = args.root.resolve()
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:8]
    report_path = args.report.resolve() if args.report else root / "evidence" / ("backup-recovery-" + stamp + ".json")
    report = {"task": "AIORG-V4.2-N001", "test": "backup-isolated-restore-and-optional-db-crash",
              "started_at_utc": utc(), "source_schema": SOURCE_SCHEMA, "project": PROJECT,
              "kill_requested": args.kill_db, "status": "RUNNING", "stage": "initialization"}
    started = time.perf_counter()
    try:
        probe = Probe(root, args.command_timeout)
        report.update(container_id=probe.container, container_state=probe.state())
        report["stage"] = "source_metadata"
        probe.load_metadata()
        report["source_before"] = probe.snapshot(SOURCE_SCHEMA, "snapshot_before_backup")
        report["source_integrity"] = probe.check_tables(SOURCE_SCHEMA, "check_source_tables")
        report["stage"] = "backup"
        backup_path = probe.backups / (SOURCE_SCHEMA + "-" + stamp + ".sql")
        report["backup"] = probe.backup(backup_path)
        restore_schema = "rental_n001_restore_" + stamp
        report["restore_schema"] = restore_schema
        report["stage"] = "isolated_restore"
        restore_started = time.perf_counter()
        probe.restore(backup_path, restore_schema)
        report["restore_seconds"] = round(time.perf_counter()-restore_started, 3)
        report["restored"] = probe.snapshot(restore_schema, "snapshot_restored_schema")
        report["restore_integrity"] = probe.check_tables(restore_schema, "check_restored_tables")
        report["source_after_restore"] = probe.snapshot(SOURCE_SCHEMA, "snapshot_source_after_restore")
        report["source_unchanged_during_test"] = report["source_before"] == report["source_after_restore"]
        report["restored_matches_source"] = report["restored"] == report["source_before"]
        report["backup_restore_passed"] = report["source_unchanged_during_test"] and report["restored_matches_source"]
        if not report["backup_restore_passed"]:
            raise ProbeError("Source changed during test or restored business snapshot differs; inspect local report")
        if args.kill_db:
            report["stage"] = "optional_db_crash"
            report["crash_recovery"] = crash_probe(probe, args.health_url, args.recovery_timeout)
            if not report["crash_recovery"]["passed"]:
                raise ProbeError("Optional DB crash did not satisfy automatic recovery and unchanged-data gates")
        report["status"] = "PASS"
        report["stage"] = "complete"
    except Exception as exc:
        report["status"] = "FAIL"
        # ProbeError strings contain no raw SQL rows, stderr, passwords, or environment contents.
        report["failure"] = str(exc) if isinstance(exc, ProbeError) else type(exc).__name__
    finally:
        report["finished_at_utc"] = utc()
        report["wall_seconds"] = round(time.perf_counter()-started, 3)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = report_path.with_suffix(".json.partial")
        temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(temporary, report_path)
    print(json.dumps({"status": report["status"], "stage": report["stage"],
                      "report": str(report_path), "wall_seconds": report["wall_seconds"]}, ensure_ascii=False))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
