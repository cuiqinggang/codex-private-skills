import argparse, ctypes, datetime, http.cookiejar, json, os, pathlib, re, subprocess, sys, time, urllib.error, urllib.parse, urllib.request

ROOT = pathlib.Path(r"C:\AI\Douyin-Ultra-Direct")
DESKTOP = pathlib.Path.home() / "Desktop"
STATE = ROOT / "session.cookies"
LAST = ROOT / "last_run.json"
BASE = "https://demo.douyin.wtf"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36"
REFERER = "https://www.douyin.com/"
FALLBACK = pathlib.Path(r"C:\AI\Douyin-Direct-Save-Windows\Douyin-Direct-Save.cmd")
CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)

def now():
    return datetime.datetime.now().astimezone().isoformat()

def clipboard_text():
    u = ctypes.WinDLL("user32", use_last_error=True)
    k = ctypes.WinDLL("kernel32", use_last_error=True)
    u.GetClipboardData.argtypes = [ctypes.c_uint]
    u.GetClipboardData.restype = ctypes.c_void_p
    k.GlobalLock.argtypes = [ctypes.c_void_p]
    k.GlobalLock.restype = ctypes.c_void_p
    k.GlobalUnlock.argtypes = [ctypes.c_void_p]
    k.GlobalUnlock.restype = ctypes.c_bool
    if not u.OpenClipboard(None):
        raise RuntimeError("CLIPBOARD_OPEN_FAILED")
    try:
        h = u.GetClipboardData(13)
        if not h:
            raise RuntimeError("CLIPBOARD_UNICODE_TEXT_MISSING")
        p = k.GlobalLock(h)
        if not p:
            raise RuntimeError("CLIPBOARD_LOCK_FAILED")
        try:
            return ctypes.wstring_at(p)
        finally:
            k.GlobalUnlock(h)
    finally:
        u.CloseClipboard()

def extract_url(text):
    m = re.search(r"https?://[^\s<>\"\u3000]+", text)
    if not m:
        raise RuntimeError("NO_URL_IN_CLIPBOARD")
    u = m.group(0).rstrip(".,;，。！!；)")
    host = (urllib.parse.urlsplit(u).hostname or "").lower()
    if host != "douyin.com" and not host.endswith(".douyin.com"):
        raise RuntimeError("NOT_DOUYIN_URL")
    return u

def cookie_opener():
    jar = http.cookiejar.MozillaCookieJar(str(STATE))
    if STATE.exists():
        try:
            jar.load(ignore_discard=True, ignore_expires=False)
        except Exception:
            pass
    return jar, urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

def json_request(opener, url, method="GET", payload=None):
    data = None if payload is None else json.dumps(payload, separators=(",", ":")).encode("utf-8")
    headers = {"User-Agent": UA, "Referer": REFERER, "Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with opener.open(req, timeout=30) as r:
        body = r.read()
        return r.status, json.loads(body.decode("utf-8"))

def login(jar, opener):
    status, demo = json_request(opener, BASE + "/api/v1/auth/demo")
    if status != 200 or not demo.get("success"):
        raise RuntimeError("DEMO_AUTH_DISCOVERY_FAILED")
    password = demo.get("data", {}).get("password")
    if not password:
        raise RuntimeError("DEMO_PASSWORD_MISSING")
    status, obj = json_request(
        opener,
        BASE + "/api/v1/auth/login",
        "POST",
        {"username": "demo", "password": password},
    )
    if status != 200 or not obj.get("success", True):
        raise RuntimeError("DEMO_LOGIN_FAILED")
    jar.save(ignore_discard=True, ignore_expires=True)

def parse_share(share_url, run):
    jar, opener = cookie_opener()
    body = {"url": share_url}
    t0 = time.perf_counter()
    refreshed = False
    try:
        status, obj = json_request(opener, BASE + "/api/v1/parse?wait=25", "POST", body)
    except urllib.error.HTTPError as e:
        if e.code not in (401, 403):
            raise
        status, obj = e.code, {}
    if status in (401, 403):
        a0 = time.perf_counter()
        login(jar, opener)
        run["auth_refresh_ms"] = round((time.perf_counter() - a0) * 1000, 3)
        refreshed = True
        status, obj = json_request(opener, BASE + "/api/v1/parse?wait=25", "POST", body)
    run["parse_ms"] = round((time.perf_counter() - t0) * 1000, 3)
    run["auth_reused"] = not refreshed
    if status != 200 or not obj.get("success"):
        raise RuntimeError("PARSE_FAILED_STATUS_" + str(status))
    data = obj.get("data") or {}
    media = (data.get("media") or {}).get("video") or {}
    if not media.get("url"):
        raise RuntimeError("PARSE_VIDEO_URL_MISSING")
    return data

def select_video(data):
    media = data.get("media") or {}
    streams = []
    for s in media.get("streams") or []:
        try:
            if s.get("format") != "mp4" or s.get("watermark"):
                continue
            if not s.get("url") or int(s.get("width") or 0) <= 0 or int(s.get("height") or 0) <= 0:
                continue
            streams.append(s)
        except Exception:
            continue
    if not streams:
        v = media.get("video") or {}
        if not v.get("url"):
            raise RuntimeError("PARSE_VIDEO_URL_MISSING")
        return v
    # 720P 日常观看优先；不再默认追求 4K。24 分钟视频默认不超过约 120 MB。
    def area(v):
        return int(v.get("width") or 0) * int(v.get("height") or 0)
    hd = [v for v in streams if max(int(v.get("width") or 0), int(v.get("height") or 0)) <= 1280]
    if hd:
        within = [v for v in hd if 0 < int(v.get("size_bytes") or 0) <= 120_000_000]
        if within:
            return max(within, key=lambda v: (area(v), int(v.get("bitrate") or 0)))
        return min(hd, key=lambda v: (int(v.get("size_bytes") or 10**15), -area(v)))
    return min(streams, key=lambda v: area(v))

def unique_urls(video):
    vals = [video.get("url")] + list(video.get("urls") or [])
    seen, out = set(), []
    for u in vals:
        if not isinstance(u, str) or not u.startswith(("http://", "https://")) or u in seen:
            continue
        seen.add(u)
        out.append(u)
    if not out:
        raise RuntimeError("NO_MEDIA_URL")
    official = [u for u in out if (urllib.parse.urlsplit(u).hostname or "").lower() == "www.douyin.com"]
    rest = [u for u in out if u not in official]
    return official + rest

def curl_download(url, part):
    cmd = [
        "curl.exe", "-L", "--fail", "--silent", "--show-error",
        "--retry", "1", "--retry-delay", "0", "--connect-timeout", "5",
        "--max-time", "90", "-A", UA, "-e", REFERER,
        "-o", str(part), url,
    ]
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore", creationflags=CREATE_NO_WINDOW)

def ffprobe(path, expected_width=None, expected_height=None, allow_hevc=False):
    p = subprocess.run(
        ["ffprobe.exe", "-v", "error",
         "-show_entries", "format=format_name,duration:stream=codec_type,codec_name,width,height,sample_rate,channels",
         "-of", "json", str(path)],
        capture_output=True, text=True, encoding="utf-8", errors="ignore",
        timeout=20, creationflags=CREATE_NO_WINDOW,
    )
    if p.returncode:
        raise RuntimeError("FFPROBE_FAILED")
    info = json.loads(p.stdout)
    streams = info.get("streams") or []
    vs = [s for s in streams if s.get("codec_type") == "video"]
    au = [s for s in streams if s.get("codec_type") == "audio"]
    duration = float((info.get("format") or {}).get("duration") or 0)
    if not vs or not au or duration <= 0:
        raise RuntimeError("MISSING_AV_OR_DURATION")
    if vs[0].get("codec_name") not in (("h264", "hevc") if allow_hevc else ("h264",)):
        raise RuntimeError("VIDEO_NOT_H264:" + str(vs[0].get("codec_name")))
    if au[0].get("codec_name") != "aac":
        raise RuntimeError("AUDIO_NOT_AAC:" + str(au[0].get("codec_name")))
    actual_width = int(vs[0].get("width") or 0)
    actual_height = int(vs[0].get("height") or 0)
    if expected_width and expected_height and (actual_width != int(expected_width) or actual_height != int(expected_height)):
        raise RuntimeError("QUALITY_DIMENSION_MISMATCH:" + str(actual_width) + "x" + str(actual_height))
    return {
        "duration": duration,
        "video": vs[0].get("codec_name"),
        "audio": au[0].get("codec_name"),
        "width": actual_width,
        "height": actual_height,
    }


def compatible_mp4(part, expected_width=None, expected_height=None, run=None):
    source = ffprobe(part, expected_width, expected_height, allow_hevc=True)
    if source["video"] in ("h264", "hevc"):
        if run is not None:
            run["source_video"] = source["video"]
            run["compatibility_policy"] = "NO_REENCODE_KEEP_SOURCE"
        return source
    converted = part.with_name(part.name + ".h264.mp4")
    started = time.perf_counter()
    errors = []
    try:
        for encoder, options in [
            ("h264_nvenc", ["-preset", "p4", "-rc", "vbr", "-cq", "19", "-b:v", "0"]),
            ("libx264", ["-preset", "veryfast", "-crf", "19"]),
        ]:
            cmd = [
                "ffmpeg.exe", "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
                "-i", str(part), "-map", "0:v:0", "-map", "0:a:0",
                "-c:v", encoder,
            ] + options + [
                "-pix_fmt", "yuv420p", "-c:a", "copy",
                "-movflags", "+faststart", "-f", "mp4", str(converted),
            ]
            try:
                result = subprocess.run(
                    cmd, capture_output=True, text=True, encoding="utf-8",
                    errors="ignore", timeout=max(120, source["duration"] * 4),
                    creationflags=CREATE_NO_WINDOW,
                )
                if result.returncode:
                    raise RuntimeError(result.stderr[-1500:])
                probe = ffprobe(converted, source["width"], source["height"])
                if abs(probe["duration"] - source["duration"]) > 0.25:
                    raise RuntimeError("TRANSCODE_DURATION_MISMATCH")
                os.replace(converted, part)
                if run is not None:
                    run.update({
                        "source_video": source["video"], "compatibility_encoder": encoder,
                        "compatibility_ms": round((time.perf_counter() - started) * 1000, 3),
                    })
                return probe
            except (RuntimeError, subprocess.TimeoutExpired) as error:
                errors.append(encoder + ":" + str(error))
        raise RuntimeError("HEVC_COMPATIBILITY_FAILED:" + ";".join(errors))
    finally:
        if converted.exists():
            converted.unlink()

def fallback_existing(run):
    if not FALLBACK.exists():
        raise RuntimeError("FALLBACK_MISSING")
    t0 = time.perf_counter()
    p = subprocess.run(
        ["cmd.exe", "/c", str(FALLBACK)],
        capture_output=True, text=True, encoding="utf-8", errors="ignore",
        timeout=120, creationflags=CREATE_NO_WINDOW,
    )
    run["fallback_ms"] = round((time.perf_counter() - t0) * 1000, 3)
    run["fallback_exit"] = p.returncode
    if p.returncode != 0:
        raise RuntimeError("FALLBACK_FAILED")
    run["route"] = "FALLBACK_EXISTING_MATURE"
    return 0

def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--no-fallback", action="store_true")
    ap.add_argument("--url")
    args, _ = ap.parse_known_args()
    start = time.perf_counter()
    run = {"schema": "DOUYIN_ULTRA_DIRECT_V1", "started_at": now(), "route": "API_PRIMARY"}
    try:
        c0 = time.perf_counter()
        text = args.url if args.url else clipboard_text()
        share = extract_url(text)
        run["clipboard_ms"] = round((time.perf_counter() - c0) * 1000, 3)
        run["share_url"] = share

        data = parse_share(share, run)
        content_id = str(data.get("content_id") or int(time.time()))
        video = select_video(data)
        expected_width = int(video.get("width") or 0)
        expected_height = int(video.get("height") or 0)
        urls = unique_urls(video)
        run["selected_stream"] = {
            "width": expected_width,
            "height": expected_height,
            "size_bytes": int(video.get("size_bytes") or 0),
            "bitrate": int(video.get("bitrate") or 0),
        }
        run["media_candidates"] = [urllib.parse.urlsplit(u).hostname for u in urls]

        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        target = DESKTOP / f"douyin_{content_id}_{stamp}.mp4"
        work = ROOT / "work"
        work.mkdir(exist_ok=True)
        part = work / (target.name + ".part")
        if part.exists():
            part.unlink()

        d0 = time.perf_counter()
        chosen = None
        errors = []
        for i, u in enumerate(urls):
            if part.exists():
                part.unlink()
            p = curl_download(u, part)
            if p.returncode == 0 and part.exists() and part.stat().st_size > 65536:
                chosen = u
                run["download_candidate_index"] = i
                break
            errors.append({"i": i, "host": urllib.parse.urlsplit(u).hostname, "exit": p.returncode})
        run["download_ms"] = round((time.perf_counter() - d0) * 1000, 3)
        run["download_errors"] = errors
        if not chosen:
            raise RuntimeError("ALL_MEDIA_DOWNLOADS_FAILED")

        v0 = time.perf_counter()
        probe = compatible_mp4(part, expected_width, expected_height, run)
        run["verify_ms"] = round((time.perf_counter() - v0) * 1000, 3)
        os.replace(part, target)

        run.update({
            "status": "PASS",
            "output": str(target),
            "bytes": target.stat().st_size,
            "chosen_host": urllib.parse.urlsplit(chosen).hostname,
            "probe": probe,
            "finished_at": now(),
            "T_VALID_MS": round((time.perf_counter() - start) * 1000, 3),
        })
        LAST.write_text(json.dumps(run, ensure_ascii=False, indent=2), encoding="utf-8")
        print("FINAL_VALID=YES")
        print("OUTPUT=" + str(target))
        print("T_VALID_MS=" + str(run["T_VALID_MS"]))
        return 0
    except Exception as e:
        run["primary_error"] = repr(e)
        if not args.no_fallback:
            try:
                rc = fallback_existing(run)
                run.update({"status": "PASS_FALLBACK", "finished_at": now(), "T_VALID_MS": round((time.perf_counter() - start) * 1000, 3)})
                LAST.write_text(json.dumps(run, ensure_ascii=False, indent=2), encoding="utf-8")
                print("FINAL_VALID=YES_FALLBACK")
                print("T_VALID_MS=" + str(run["T_VALID_MS"]))
                return rc
            except Exception as fe:
                run["fallback_error"] = repr(fe)
        run.update({"status": "FAIL", "finished_at": now(), "T_VALID_MS": None})
        LAST.write_text(json.dumps(run, ensure_ascii=False, indent=2), encoding="utf-8")
        print("FINAL_VALID=NO")
        print("ERROR=" + repr(e))
        return 1

if __name__ == "__main__":
    sys.exit(main())
