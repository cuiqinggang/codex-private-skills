"""Install the pinned upstream Copyparty distribution; keep credentials on Windows only."""
import argparse
import base64
import csv
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
import urllib.request
import zipfile

ROOT = Path(r"C:\AI\Public-Server")
URL = "https://github.com/9001/copyparty/releases/download/v1.20.26/copyparty-sfx.py"
SHA256 = "8f9a0def8a9c15252a06395781ec083372043b60caa80fb33c3d6dafa7f1b40a"


def protect(path):
    raw = subprocess.check_output(["whoami.exe", "/user", "/fo", "csv", "/nh"])
    sid = next(csv.reader(io.StringIO(raw.decode("utf-8", errors="replace"))))[1]
    result = subprocess.run(["icacls.exe", str(path), "/inheritance:r", "/grant:r",
                             "*" + sid + ":F", "*S-1-5-18:F", "*S-1-5-32-544:F"],
                            capture_output=True)
    if result.returncode:
        raise RuntimeError("Unable to restrict private configuration file permissions")


def prepare():
    for name in ["bin", "shared", "private", "data", "logs", "backups"]:
        (ROOT / name).mkdir(exist_ok=True)
    binary = ROOT / "bin" / "copyparty-sfx.py"
    if not binary.exists() or hashlib.sha256(binary.read_bytes()).hexdigest() != SHA256:
        body = urllib.request.urlopen(URL, timeout=45).read()
        if hashlib.sha256(body).hexdigest() != SHA256:
            raise RuntimeError("Official release digest mismatch")
        binary.write_bytes(body)
    backup = ROOT / "backups" / ("before-share-" + time.strftime("%Y%m%d-%H%M%S"))
    backup.mkdir(exist_ok=False)
    for name in ["public_server.py", "config.json", "copyparty.conf", "tunnel.task.xml", "origin.task.xml", "public/index.html"]:
        source = ROOT / name
        if source.exists():
            dest = backup / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
    credentials_path = ROOT / "download-owner.json"
    if credentials_path.exists():
        credentials = json.loads(credentials_path.read_text(encoding="utf-8"))
    else:
        credentials = {"username": "owner", "password": secrets.token_urlsafe(30),
                       "salt": secrets.token_urlsafe(20)}
    if not credentials.get("ready"):
        credentials = {"username": "owner", "password": secrets.token_urlsafe(30),
                       "salt": secrets.token_urlsafe(20)}
    credentials_path.write_text(json.dumps(credentials), encoding="utf-8")
    protect(credentials_path)
    # Exact upstream v1.20.26 pwhash.py _gen_scrypt format and parameters.
    # Keep plaintext out of subprocess arguments and failure tracebacks.
    digest = credentials["password"].encode("utf-8")
    for _ in range(2):
        digest = hashlib.scrypt(digest, salt=credentials["salt"].encode("utf-8"),
                                n=16384, r=8, p=4, dklen=24, maxmem=32*1024*1024)
    password_hash = "+" + base64.urlsafe_b64encode(digest).decode("ascii")
    # A deliberately unused identity is immediately demoted to anonymous by ipr.
    # Distinct random hash avoids duplicate-password account rejection upstream.
    visitor_hash = "+" + base64.urlsafe_b64encode(secrets.token_bytes(24)).decode("ascii")
    text = """[global]
  i: 127.0.0.1,::1
  p: {port}
  lang: chi
  name: 我的文件分享站
  theme: 2
  no-dav
  no-robots
  no-logues
  no-readme
  xvol
  xdev
  e2dsa
  hist: C:/AI/Public-Server/data/hist
  ses-db: C:/AI/Public-Server/data/sessions.db
  shr: /s
  shr-db: C:/AI/Public-Server/data/shares.db
  shr-who: auth
  xff-hdr: cf-connecting-ip
  xff-src: ::1/128
  rproxy: 1
  ipu: 0.0.0.0/0=visitor
  ipu: ::/0=visitor
  ipu: 127.0.0.1/32=owner
  ipr: 127.0.0.1/32=owner
  ipr: 127.0.0.1/32=visitor
  ah-alg: scrypt,13,2,8,4,32
  ah-salt: {salt}
  lo: C:/AI/Public-Server/logs/copyparty-%Y-%m%d.log

[accounts]
  visitor: {visitor_hash}
  owner: {password_hash}

[/]
  C:/AI/Public-Server/public
  accs:
    h: *

[/download]
  C:/AI/Public-Server/shared
  accs:
    r: *
    rwmd: owner

[/private]
  C:/AI/Public-Server/private
  accs:
    rwmd: owner
"""
    for filename, port in [("copyparty.conf", 18780), ("copyparty-stage.conf", 18782)]:
        path = ROOT / filename
        rendered = text.format(port=port, salt=credentials["salt"], password_hash=password_hash, visitor_hash=visitor_hash)
        if port == 18782:
            rendered = rendered.replace("/data/hist", "/data/stage-hist").replace("/data/shares.db", "/data/stage-shares.db").replace("/data/sessions.db", "/data/stage-sessions.db")
        path.write_text(rendered, encoding="utf-8")
        protect(path)
    instructions = ("本机文件管理：不用登录\n\n本机管理地址：http://127.0.0.1:18780/download/\n"
                    "在这台电脑直接打开本机管理地址，即可拖文件上传、创建文件夹、重命名和删除。\n"
                    "最简单：直接把文件放到下载文件夹，别人打开下载区取走。\n"
                    "公开下载文件夹：C:\\AI\\Public-Server\\shared\n"
                    "私有文件夹：C:\\AI\\Public-Server\\private（访客不能直接访问）\n"
                    "只把准备公开的文件放入公开下载区。不要把本说明或密码配置放进去。\n"
                    "可对私有文件创建带密码、有效期的分享链接。\n")
    (ROOT / "owner-access.txt").write_text(instructions, encoding="utf-8-sig")
    protect(ROOT / "owner-access.txt")
    (ROOT / "shared" / "下载说明.txt").write_text(
        "欢迎来到我的文件分享站。\n点击文件名可以打开，使用下载按钮保存到设备。\n"
        "支持文件夹浏览、多个文件打包下载，以及浏览器支持的图片/音视频预览。\n"
        "文件由这台电脑提供，电脑关机或断网后暂停服务。\n", encoding="utf-8-sig")
    demo = ROOT / "shared" / "示例网站.zip"
    with zipfile.ZipFile(demo, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in ["index.html", "demo/index.html"]:
            archive.write(ROOT / "public" / name, name)
    (ROOT / "private" / "qa-private.txt").write_text("PRIVATE-CONTENT-MUST-NOT-LEAK", encoding="ascii")
    result = {"phase": "PREPARED", "version": "2.0.0", "upstream": "copyparty v1.20.26",
              "official_sha256": SHA256, "backup": str(backup), "credentials_disclosed": False}
    (ROOT / "share-upgrade.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    credentials["ready"] = True
    credentials_path.write_text(json.dumps(credentials), encoding="utf-8")
    print(json.dumps(result), flush=True)


def activate():
    import public_server as manager
    gate = json.loads((ROOT / "share-stage-acceptance.json").read_text(encoding="utf-8"))
    if not gate.get("all_pass") or gate.get("passed") != 27 or not gate.get("local_owner_no_login"):
        raise RuntimeError("Staging acceptance must pass before publication")
    # Separate trusted local management (IPv4) from tunnel traffic (IPv6).
    settings = manager.config()
    if settings.get("target") not in ("http://127.0.0.1:18780", "http://[::1]:18780"):
        raise RuntimeError("Another authorized app owns this tunnel; refusing to replace it")
    manager.stop()
    settings.update(version="2.0.0", origin_engine="copyparty", target="http://[::1]:18780")
    manager.save_json(ROOT / "config.json", settings)
    manager.register_tasks(settings)
    manager.start()
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        try:
            if manager.http_get("http://127.0.0.1:18780/download/")[0] == 200:
                break
        except OSError:
            pass
        time.sleep(.25)
    else:
        raise RuntimeError("New origin not ready; restore the recorded backup")
    controls = manager.write_share_controls()
    print(json.dumps({"phase": "ACTIVATED", "state": manager.status(),
                      "desktop_controls": str(controls), "public_upload": False}), flush=True)


def checkpoint():
    import public_server as manager
    gate = json.loads((ROOT / "share-public-acceptance.json").read_text(encoding="utf-8"))
    state = manager.status()
    if not gate.get("all_pass") or gate.get("passed") != 27 or gate.get("base_url") != state.get("public_url"):
        raise RuntimeError("Current public acceptance must pass before checkpoint")
    if manager.config().get("target") != "http://[::1]:18780":
        raise RuntimeError("Unexpected file-server origin")
    backup = ROOT / "backups" / ("verified-share-v2-" + time.strftime("%Y%m%d-%H%M%S"))
    backup.mkdir(exist_ok=False)
    protect(backup)
    for name in ["public_server.py", "upgrade_file_share.py", "verify_file_share.py", "config.json",
                 "copyparty.conf", "download-owner.json", "origin.task.xml", "tunnel.task.xml", "public/index.html"]:
        dest = backup / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, dest)
        protect(dest)
    record = json.loads((ROOT / "share-upgrade.json").read_text(encoding="utf-8"))
    record.update(phase="VERIFIED", verified_backup=str(backup), public_checks_passed=27,
                  public_checked_utc=gate["timestamp_utc"])
    manager.save_json(ROOT / "share-upgrade.json", record)
    print(json.dumps({"phase": "CHECKPOINT", "verified_backup": str(backup), "public_checks_passed": 27}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=["prepare", "activate", "checkpoint"])
    phase = parser.parse_args().phase
    try:
        if phase == "prepare":
            prepare()
        elif phase == "activate":
            activate()
        else:
            checkpoint()
    except Exception as exc:
        print(json.dumps({"phase": phase, "status": "FAILED", "error_type": type(exc).__name__}), flush=True)
        sys.exit(1)
