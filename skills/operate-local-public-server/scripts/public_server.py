"""Manage a Windows local website or upstream file server with official cloudflared.

No router rules, system proxy changes, or additional scheduler.
Only the explicit public directory is served. Runtime data never belongs in skills.
"""
from __future__ import annotations

import argparse
import csv
import functools
import hashlib
import http.server
import io
import json
import os
from pathlib import Path
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from xml.sax.saxutils import escape

VERSION = "2.0.0"
ROOT = Path(os.environ.get("AIORG_PUBLIC_ROOT", r"C:\AI\Public-Server"))
TASKS = {"origin": "AIORG-PublicWeb-Origin", "tunnel": "AIORG-PublicWeb-Tunnel"}
MARKER = "AIORG_PUBLIC_WEB_V1"


def output(value):
    print(json.dumps(value, ensure_ascii=True), flush=True)


def save_json(path, value):
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                     prefix=path.name + ".", suffix=".new", delete=False) as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2))
        candidate = Path(stream.name)
    os.replace(candidate, path)


def command(args, required=True):
    result = subprocess.run(args, capture_output=True, timeout=20)
    if required and result.returncode:
        raise RuntimeError(f"Command failed ({result.returncode}): {args[0]} {args[1:3]}: "
                           + result.stderr.decode("utf-8", errors="replace")[:500])
    return result


def config():
    return json.loads((ROOT / "config.json").read_text(encoding="utf-8"))


def http_get(url, timeout=3):
    # Bypass environment proxies only for this loopback check, without system changes.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(url, timeout=timeout) as response:
        return response.status, response.read()


def port_open(port):
    with socket.socket() as sock:
        sock.settimeout(0.3)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def task_xml(executable, arguments, sid):
    return f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
 <RegistrationInfo><Author>AIORG</Author><Description>{MARKER}</Description></RegistrationInfo>
 <Triggers><LogonTrigger><Enabled>true</Enabled><UserId>{escape(sid)}</UserId></LogonTrigger></Triggers>
 <Principals><Principal id="Author"><UserId>{escape(sid)}</UserId><LogonType>InteractiveToken</LogonType><RunLevel>LeastPrivilege</RunLevel></Principal></Principals>
 <Settings><MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy><DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries><StopIfGoingOnBatteries>false</StopIfGoingOnBatteries><StartWhenAvailable>true</StartWhenAvailable><ExecutionTimeLimit>PT0S</ExecutionTimeLimit><RestartOnFailure><Interval>PT1M</Interval><Count>3</Count></RestartOnFailure></Settings>
 <Actions Context="Author"><Exec><Command>{escape(executable)}</Command><Arguments>{escape(arguments)}</Arguments><WorkingDirectory>{escape(str(ROOT))}</WorkingDirectory></Exec></Actions>
</Task>'''


def register_tasks(settings, roles=None):
    identity = command(["whoami.exe", "/user", "/fo", "csv", "/nh"])
    sid = next(csv.reader(io.StringIO(identity.stdout.decode("utf-8", errors="replace"))))[1]
    commands = {
        "origin": (sys.executable, subprocess.list2cmdline(
            [str(ROOT / "bin" / "copyparty-sfx.py"), "-c", str(ROOT / "copyparty.conf")]
            if settings.get("origin_engine") == "copyparty" else
            [str(ROOT / "public_server.py"), "serve"])),
        "tunnel": (str(ROOT / "bin" / "cloudflared.exe"), subprocess.list2cmdline([
            "tunnel", "--no-autoupdate", "--protocol", "http2", "--metrics",
            "127.0.0.1:18781", "--logfile", str(ROOT / "logs" / "tunnel.log"),
            "--url", settings["target"]])),
    }
    for role, (executable, arguments) in commands.items():
        if roles is not None and role not in roles:
            continue
        existing = command(["schtasks.exe", "/Query", "/TN", TASKS[role], "/XML"], False)
        if existing.returncode == 0 and MARKER.encode() not in existing.stdout.replace(b"\x00", b""):
            raise RuntimeError("Task name is owned by another application: " + TASKS[role])
        path = ROOT / (role + ".task.xml")
        path.write_text(task_xml(executable, arguments, sid), encoding="utf-16")
        command(["schtasks.exe", "/Create", "/TN", TASKS[role], "/XML", str(path), "/F"])


def desktop_directory():
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                        r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders") as key:
        return Path(os.path.expandvars(winreg.QueryValueEx(key, "Desktop")[0]))


def write_controls():
    folder = desktop_directory() / "\u6211\u7684\u516c\u7f51\u670d\u52a1\u5668"
    folder.mkdir(exist_ok=True)
    controls = {
        "\u542f\u52a8\u516c\u7f51\u670d\u52a1.cmd": "start",
        "\u505c\u6b62\u516c\u7f51\u670d\u52a1.cmd": "stop",
        "\u67e5\u770b\u516c\u7f51\u7f51\u5740.cmd": "open",
    }
    for filename, action in controls.items():
        (folder / filename).write_text(
            '@echo off\r\n' + subprocess.list2cmdline([sys.executable, str(ROOT / "public_server.py"), action])
            + '\r\npause\r\n', encoding="ascii")
    (folder / "\u6253\u5f00\u5171\u4eab\u76ee\u5f55.cmd").write_text(
        '@echo off\r\nexplorer.exe "' + str(ROOT / "public") + '"\r\n', encoding="ascii")
    (folder / "\u4f7f\u7528\u8bf4\u660e.txt").write_text(
        "\u8fd9\u53f0\u7535\u8111\u5c31\u662f\u670d\u52a1\u5668\u3002\n"
        "\u542f\u52a8\u540e\u67e5\u770b\u516c\u7f51\u7f51\u5740\uff0c\u590d\u5236\u7ed9\u522b\u4eba\u5373\u53ef\u8bbf\u95ee\u3002\n"
        "\u53ea\u5c06\u51c6\u5907\u516c\u5f00\u7684\u7f51\u9875\u3001\u56fe\u7247\u6216\u6587\u4ef6\u653e\u8fdb\u5171\u4eab\u76ee\u5f55\u3002\n"
        "\u4f8b\uff1a\u5171\u4eab\u76ee\u5f55\u4e0b\u65b0\u5efa test/index.html\uff0c\u8bbf\u95ee \u516c\u7f51\u7f51\u5740/test/\u3002\n"
        "\u7535\u8111\u5173\u673a\u3001\u7761\u7720\u3001\u65ad\u7f51\u65f6\u65e0\u6cd5\u8bbf\u95ee\u3002\u542f\u52a8\u540e\u4e0b\u6b21\u767b\u5f55 Windows \u4f1a\u81ea\u52a8\u8fd0\u884c\u3002\n"
        "\u505c\u6b62\u6309\u94ae\u4f1a\u540c\u65f6\u7981\u7528\u81ea\u542f\u52a8\uff1b\u542f\u52a8\u6309\u94ae\u4f1a\u91cd\u65b0\u542f\u7528\u3002\n"
        "\u514d\u8d39\u4e34\u65f6\u7f51\u5740\u91cd\u542f\u96a7\u9053\u540e\u4f1a\u6539\u53d8\uff0c\u4ee5\u67e5\u770b\u6309\u94ae\u663e\u793a\u4e3a\u51c6\u3002\n"
        "\u5f53\u524d\u652f\u6301\u5c55\u793a\u7f51\u7ad9\u4e0e\u6587\u4ef6\u3002\u52a8\u6001\u5e94\u7528\u9700\u5148\u8fd0\u884c\u8be5\u5e94\u7528\uff0c\u518d\u7531 AI \u6309\u6388\u6743\u5207\u6362\u5230\u5b83\u7684\u672c\u5730\u7aef\u53e3\u3002\n",
        encoding="utf-8-sig")
    return folder


def write_share_controls():
    folder = desktop_directory() / "我的公网服务器"
    folder.mkdir(exist_ok=True)
    legacy = folder / "其他入口"
    legacy.mkdir(exist_ok=True)
    for name in ["打开下载区.cmd", "管理文件（本机）.cmd", "打开下载文件夹.cmd",
                 "下载文件夹（拖文件到这里）.lnk", "打开共享目录.cmd", "查看公网网址.cmd"]:
        source = folder / name
        if source.exists() and not (legacy / name).exists():
            shutil.move(str(source), str(legacy / name))
    # Native directory junction: Explorer treats this as a folder, not a command.
    shared = ROOT / "shared"
    destination = folder / "放文件（拖到这里即可分享）"
    if destination.exists():
        if not os.path.samefile(destination, shared):
            raise RuntimeError("Existing drop folder points somewhere else")
    else:
        command(["cmd.exe", "/d", "/c", "mklink", "/J", str(destination), str(shared)])
    for name, action in [("本机上传（免登录）.cmd", "admin"), ("给别人下载（打开后复制网址）.cmd", "downloads")]:
        (folder / name).write_text('@echo off\r\n' + subprocess.list2cmdline(
            [sys.executable, str(ROOT / "public_server.py"), action]) + '\r\n', encoding="ascii")
    (folder / "使用说明.txt").write_text(
        "放文件：把文件拖进「放文件（拖到这里即可分享）」这个文件夹。\n"
        "也可打开「本机上传（免登录）」，在本机网页上传。\n"
        "分享：打开「给别人下载」，复制浏览器地址发给别人；新增文件后刷新页面。\n"
        "给别人下载的公网页面不能接收上传。本机上传地址：http://127.0.0.1:18780/download/\n"
        "文件夹内的文件会公开，只放准备分享的文件。关机、睡眠、断网时服务暂停。\n",
        encoding="utf-8-sig")
    return folder


def install(source):
    if os.name != "nt":
        raise RuntimeError("Installation requires Windows")
    for name in ["public", "bin", "logs"]:
        (ROOT / name).mkdir(parents=True, exist_ok=True)
    settings_path = ROOT / "config.json"
    settings = config() if settings_path.exists() else {
        "version": VERSION, "port": 18780, "target": "http://127.0.0.1:18780"}
    if not settings_path.exists() and (port_open(18780) or port_open(18781)):
        raise RuntimeError("A required loopback port is occupied")
    source = Path(source).resolve(strict=True)
    if source != (ROOT / "bin" / "cloudflared.exe").resolve():
        shutil.copy2(source, ROOT / "bin" / "cloudflared.exe")
    save_json(settings_path, settings)
    register_tasks(settings)
    controls = write_controls()
    version = command([str(ROOT / "bin" / "cloudflared.exe"), "--version"]).stdout.decode().strip()
    result = {"status": "INSTALLED", "version": VERSION, "root": str(ROOT),
              "controls": str(controls), "cloudflared_version": version,
              "cloudflared_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "tasks": TASKS, "auto_start": "CURRENT_USER_LOGON", "sleep_settings_changed": False}
    save_json(ROOT / "installation.json", result)
    output(result)


def status():
    log = ROOT / "logs" / "tunnel.log"
    content = log.read_text(encoding="utf-8", errors="replace")[-100000:] if log.exists() else ""
    urls = re.findall(r"https://[a-z0-9-]+\.trycloudflare\.com", content)
    try:
        ready = http_get("http://127.0.0.1:18781/ready")[0] == 200
    except (OSError, urllib.error.URLError):
        ready = False
    try:
        local_status = http_get(config()["target"])[0]
    except (OSError, urllib.error.URLError):
        local_status = None
    value = {"status": "RUNNING" if ready and local_status == 200 and urls else "STOPPED_OR_NOT_READY",
             "public_url": urls[-1] if ready and urls else None,
             "target": config()["target"], "local_http_status": local_status,
             "tunnel_ready": ready, "public_directory": str(ROOT / "public"),
             "version": VERSION, "checked_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    if config().get("origin_engine") == "copyparty":
        value["download_directory"] = str(ROOT / "shared")
        value["download_url"] = value["public_url"] + "/download/" if value["public_url"] else None
    save_json(ROOT / "status.json", value)
    if value["public_url"]:
        (ROOT / "CURRENT-URL.txt").write_text(value["public_url"] + "\n", encoding="ascii")
    return value


def start():
    # Remove a completed session's log before Run, so a stale hostname is never reused.
    previous = status()
    if not previous["tunnel_ready"]:
        log = ROOT / "logs" / "tunnel.log"
        if log.exists():
            os.replace(log, log.with_name("tunnel.previous.log"))
    for role in ("origin", "tunnel"):
        command(["schtasks.exe", "/Change", "/TN", TASKS[role], "/ENABLE"])
        command(["schtasks.exe", "/Run", "/TN", TASKS[role]])
    deadline = time.monotonic() + 75
    retry_at = time.monotonic() + 15
    attempts = 1
    while time.monotonic() < deadline:
        value = status()
        if value["status"] == "RUNNING":
            output(value)
            return
        if time.monotonic() >= retry_at and attempts < 3:
            # The existing scheduler's IgnoreNew policy prevents duplicate processes.
            # A cold-DNS cloudflared exit can return 0, so RestartOnFailure alone is insufficient.
            try:
                subprocess.run([sys.executable, "-c", "import socket; "
                    "socket.getaddrinfo('region1.v2.argotunnel.com.',7844,socket.AF_INET); "
                    "socket.getaddrinfo('region2.v2.argotunnel.com.',7844,socket.AF_INET)"],
                    capture_output=True, timeout=min(5, max(0.1, deadline - time.monotonic())))
            except (OSError, subprocess.TimeoutExpired):
                pass
            command(["schtasks.exe", "/Run", "/TN", TASKS["tunnel"]])
            attempts += 1
            retry_at = time.monotonic() + 15
        time.sleep(0.5)
    output(status())
    raise RuntimeError("Services not ready within bounded startup window; inspect logs")


def stop():
    for role in ("tunnel", "origin"):
        command(["schtasks.exe", "/Change", "/TN", TASKS[role], "/DISABLE"])
        command(["schtasks.exe", "/End", "/TN", TASKS[role]], False)
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline and (port_open(18780) or port_open(18781)):
        time.sleep(0.2)
    if port_open(18780) or port_open(18781):
        raise RuntimeError("Scheduled service still listening after stop")
    (ROOT / "CURRENT-URL.txt").write_text("STOPPED\n", encoding="ascii")
    output({"status": "STOPPED", "auto_start": "DISABLED", "ports_closed": True})


def serve():
    public = (ROOT / "public").resolve()

    class Handler(http.server.SimpleHTTPRequestHandler):
        def list_directory(self, path):
            self.send_error(404, "Directory listing disabled")
            return None

        def send_head(self):
            if not Path(self.translate_path(self.path)).resolve().is_relative_to(public):
                self.send_error(403, "Outside public directory")
                return None
            return super().send_head()

        def end_headers(self):
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            super().end_headers()

    with (ROOT / "logs" / "origin.log").open("a", encoding="utf-8", buffering=1) as log:
        sys.stderr = log
        handler = functools.partial(Handler, directory=str(public))
        with http.server.ThreadingHTTPServer(("127.0.0.1", config()["port"]), handler) as server:
            server.serve_forever()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["install", "start", "stop", "status", "open", "serve", "target", "downloads", "admin", "repair-controls"])
    parser.add_argument("--cloudflared-source")
    parser.add_argument("--url")
    parsed = parser.parse_args()
    if parsed.action == "install":
        if not parsed.cloudflared_source:
            parser.error("--cloudflared-source is required")
        install(parsed.cloudflared_source)
    elif parsed.action == "serve":
        serve()
    elif parsed.action == "start":
        start()
    elif parsed.action == "stop":
        stop()
    elif parsed.action == "repair-controls":
        output({"status": "CONTROLS_READY", "directory": str(write_share_controls())})
    elif parsed.action == "target":
        url = urllib.parse.urlsplit(parsed.url or "")
        if url.scheme != "http" or url.hostname not in ("127.0.0.1", "::1") or not url.port or url.username or url.password or url.query or url.fragment or url.path not in ("", "/"):
            parser.error("Use an explicitly authorized http://127.0.0.1:PORT origin")
        if url.port in (18781, 18782) or (config().get("origin_engine") == "copyparty" and url.port == 18780 and url.hostname != "::1"):
            parser.error("Reserved local management or metrics endpoint cannot be published")
        http_get(parsed.url)
        stop()
        settings = config()
        settings["target"] = parsed.url.rstrip("/")
        save_json(ROOT / "config.json", settings)
        register_tasks(settings)
        start()
    else:
        value = status()
        output(value)
        if parsed.action == "open" and value["public_url"]:
            os.startfile(value["public_url"] + ("/download/" if config().get("origin_engine") == "copyparty" else ""))
        elif parsed.action == "downloads" and value["public_url"]:
            os.startfile(value["public_url"] + "/download/")
        elif parsed.action == "admin":
            os.startfile("http://127.0.0.1:18780/download/")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        output({"status": "FAILED", "error": str(exc)})
        sys.exit(1)
