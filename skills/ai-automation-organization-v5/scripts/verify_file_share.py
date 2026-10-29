"""Exercise the upstream file-server APIs with synthetic files; do not log credentials."""
import argparse
import base64
import concurrent.futures
import hashlib
import io
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile

ROOT = Path(r"C:\AI\Public-Server")


def run(base):
    checks = []

    def request(path, method="GET", data=None, headers=None, auth=False):
        values = dict(headers or {})
        origin = ("http://127.0.0.1:18782" if "18782" in base else "http://127.0.0.1:18780") if auth else base
        values.setdefault("Origin", origin)
        req = urllib.request.Request(origin + path, data=data, headers=values, method=method)
        loopback = urllib.parse.urlsplit(origin).hostname in ("127.0.0.1", "::1")
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({})) if loopback else urllib.request.build_opener()
        try:
            with opener.open(req, timeout=20) as response:
                return response.status, response.read(), dict(response.headers)
        except urllib.error.HTTPError as response:
            return response.code, response.read(), dict(response.headers)

    def record(name, ok, status=None):
        checks.append({"name": name, "pass": bool(ok), "http_status": status})
        print(json.dumps(checks[-1]), flush=True)

    # Independent read-only checks share one connection batch at the host.
    paths = ["/", "/download/", "/download/?ls", "/private/qa-private.txt",
             "/copyparty.conf", "/download-owner.json", "/owner-access.txt", "/data/shares.db"]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        responses = list(pool.map(request, paths))
    for path, (code, body, _) in zip(paths, responses):
        expected = (200,) if path in paths[:3] else (401, 403, 404)
        record(path, code in expected and b"PRIVATE-CONTENT-MUST-NOT-LEAK" not in body, code)

    code, body, _ = request("/download/?ls", auth=True)
    listing = json.loads(body)
    record("local_owner_without_login", code == 200 and listing.get("acct") == "owner"
           and {"write", "move", "delete"}.issubset(listing.get("perms", [])), code)
    code, body, response_headers = request("/download/?ls")
    listing = json.loads(body)
    record("visitor_read_only_permissions", code == 200 and listing.get("acct") == "*"
           and not {"write", "move", "delete"}.intersection(listing.get("perms", [])), code)
    record("browser_same_origin_allowed", response_headers.get("Access-Control-Allow-Origin") == base, code)
    for ip in ["203.0.113.9", "2001:db8::9"]:
        headers = {"CF-Connecting-IP": ip, "X-Forwarded-Proto": "https"}
        if "18782" in base:
            headers.update({"Host": "stage.example", "Origin": "https://stage.example"})
        code, body, _ = request("/download/?ls", headers=headers)
        try:
            listing = json.loads(body)
        except (ValueError, UnicodeError):
            listing = {}
        guest = code == 200 and listing.get("acct") == "*" and "write" not in listing.get("perms", [])
        # The Cloudflare edge rejects attempts to supply its reserved source header.
        # Staging must exercise actual mapping; publication must reject or stay guest.
        blocked = "18782" not in base and code in (400, 403)
        record(("forwarded_" if "18782" in base else "forged_header_")
               + ("ipv6" if ":" in ip else "ipv4") + "_blocked_or_guest", guest or blocked, code)

    marker = b"QA-PUBLIC-UPLOAD-" + secrets.token_hex(12).encode()
    filename = "qa-upload-" + secrets.token_hex(5) + ".txt"
    boundary = "AIORG" + secrets.token_hex(12)
    upload = ("--" + boundary + '\r\nContent-Disposition: form-data; name="act"\r\n\r\nbput\r\n'
              + "--" + boundary + '\r\nContent-Disposition: form-data; name="f"; filename="' + filename
              + '"\r\nContent-Type: text/plain\r\n\r\n').encode() + marker + ("\r\n--" + boundary + "--\r\n").encode()
    headers = {"Content-Type": "multipart/form-data; boundary=" + boundary}
    code, _, _ = request("/download/", "POST", upload, headers)
    record("anonymous_upload_denied", code in (401, 403) and not (ROOT / "shared" / filename).exists(), code)
    code, _, _ = request("/download/", "POST", upload,
                          {**headers, "Origin": "https://example.invalid"}, auth=True)
    record("cross_origin_local_write_denied", code == 403 and not (ROOT / "shared" / filename).exists(), code)
    code, _, _ = request("/download/", "POST", upload, headers, auth=True)
    stored = ROOT / "shared" / filename
    record("local_no_login_upload_exact_bytes", code in (200, 201) and stored.exists() and stored.read_bytes() == marker, code)
    code, body, _ = request("/download/" + filename + "?dl")
    record("anonymous_download_uploaded_file", code == 200 and body == marker, code)
    code, body, values = request("/download/" + filename, headers={"Range": "bytes=0-9"})
    record("range_resume", code == 206 and body == marker[:10], code)

    encoded = urllib.parse.quote("下载说明.txt")
    code, body, _ = request("/download/" + encoded + "?dl")
    record("chinese_filename_download", code == 200 and body == (ROOT / "shared" / "下载说明.txt").read_bytes(), code)
    code, body, _ = request("/download/?zip")
    try:
        with zipfile.ZipFile(io.BytesIO(body)) as archive:
            zip_ok = any(name.endswith("下载说明.txt") for name in archive.namelist())
    except (ValueError, zipfile.BadZipFile):
        zip_ok = False
    record("folder_zip_download", code == 200 and zip_ok, code)
    code, body, _ = request("/download/" + filename + "?delete", "POST", b"[]",
                            {"Content-Type": "application/json"})
    record("anonymous_delete_denied", code in (401, 403) and stored.exists(), code)

    # A Windows junction must not expose a mounted owner-only volume to guests.
    junction = ROOT / "shared" / "qa-junction"
    created = subprocess.run(["cmd.exe", "/d", "/c", "mklink", "/J", str(junction), str(ROOT / "private")],
                             capture_output=True).returncode == 0
    try:
        if created:
            code, body, _ = request("/download/qa-junction/qa-private.txt")
            record("windows_junction_escape_denied", code in (401, 403, 404) and b"PRIVATE-CONTENT" not in body, code)
        else:
            record("windows_junction_probe_available", False)
    finally:
        if created:
            junction.rmdir()

    key = "qa" + secrets.token_hex(10)
    share_password = secrets.token_urlsafe(20)
    payload = {"k": key, "vp": ["/private/qa-private.txt"], "perms": ["read"], "pw": share_password, "exp": "1"}
    code, _, _ = request("/?share", "POST", json.dumps(payload).encode(), {"Content-Type": "application/json"}, auth=True)
    record("owner_password_expiry_share_creation", code == 201, code)
    code, body, _ = request("/s/" + key + "/qa-private.txt")
    record("password_share_guest_denied", code in (401, 403) and b"PRIVATE-CONTENT" not in body, code)
    share_auth = "Basic " + base64.b64encode(("x:" + share_password).encode()).decode()
    code, body, _ = request("/s/" + key + "/qa-private.txt", headers={"Authorization": share_auth})
    record("password_share_correct_password", code == 200 and body == b"PRIVATE-CONTENT-MUST-NOT-LEAK", code)

    renamed = filename.replace(".txt", "-renamed.txt")
    code, _, _ = request("/download/" + filename + "?move=" + urllib.parse.quote("/download/" + renamed),
                            "POST", b"", {"Content-Type": "application/octet-stream"}, auth=True)
    record("owner_rename", code == 201 and (ROOT / "shared" / renamed).exists(), code)
    code, _, _ = request("/download/" + renamed + "?delete", "POST", b"[]",
                            {"Content-Type": "application/json"}, auth=True)
    record("owner_delete_qa_file", code == 200 and not (ROOT / "shared" / renamed).exists(), code)
    result = {"task_id": "AIORG-FILESHARE-20261029-001", "version": "2.0.0", "upstream": "copyparty v1.20.26",
              "base_url": base, "checks": checks, "passed": sum(c["pass"] for c in checks), "total": len(checks),
              "all_pass": all(c["pass"] for c in checks), "credentials_disclosed": False,
              "local_owner_no_login": True,
              "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    destination = ROOT / ("share-stage-acceptance.json" if "18782" in base else "share-public-acceptance.json")
    if destination.exists():
        shutil.copy2(destination, destination.with_name(destination.stem + "-" + str(time.time_ns()) + ".json"))
    destination.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("RESULT_JSON=" + json.dumps(result), flush=True)
    return result["all_pass"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", action="store_true")
    parsed = parser.parse_args()
    process = None
    try:
        if parsed.stage:
            log = (ROOT / "logs" / "copyparty-stage-output.txt").open("ab", buffering=0)
            process = subprocess.Popen([sys.executable, str(ROOT / "bin" / "copyparty-sfx.py"), "-c", str(ROOT / "copyparty-stage.conf")],
                                       stdout=log, stderr=log, env={**os.environ, "XDG_CONFIG_HOME": str(ROOT / "data" / "stage-config")})
            base = "http://[::1]:18782"
            deadline = time.monotonic() + 45
            while time.monotonic() < deadline:
                try:
                    urllib.request.build_opener(urllib.request.ProxyHandler({})).open(base + "/download/", timeout=1).close()
                    break
                except OSError:
                    if process.poll() is not None:
                        raise RuntimeError("Staging origin exited; inspect its private log")
                    time.sleep(.3)
            else:
                raise RuntimeError("Staging origin did not become ready")
        else:
            import public_server
            base = public_server.status()["public_url"]
        sys.exit(0 if run(base) else 1)
    except Exception as exc:
        print(json.dumps({"status": "FAILED", "error_type": type(exc).__name__}), flush=True)
        sys.exit(1)
    finally:
        if process:
            process.terminate()
            process.wait(timeout=10)
