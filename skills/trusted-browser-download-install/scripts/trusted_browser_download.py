from __future__ import annotations

import argparse
import asyncio
import hashlib
import html
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import async_playwright


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def read_head(path: Path, n: int = 16) -> bytes:
    with path.open("rb") as f:
        return f.read(n)


def authenticode(path: Path) -> dict:
    safe_path = str(path).replace("'", "''")
    cmd = [
        "powershell",
        "-NoProfile",
        "-Command",
        f"Get-AuthenticodeSignature -LiteralPath '{safe_path}' | "
        "Select-Object Status,StatusMessage,SignerCertificate | ConvertTo-Json -Depth 4",
    ]
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        return {
            "ok": completed.returncode == 0,
            "stdout": (completed.stdout or "").strip(),
            "stderr": (completed.stderr or "").strip(),
        }
    except Exception as exc:
        return {"ok": False, "stdout": "", "stderr": repr(exc)}


def validate_file(path: Path, expected_ext: str, min_bytes: int) -> dict:
    result = {
        "path": str(path),
        "exists": path.exists(),
        "size": 0,
        "expected_ext": expected_ext,
        "extension_ok": False,
        "min_bytes": min_bytes,
        "size_ok": False,
        "head_hex": "",
        "mz_header": False,
        "looks_html": False,
        "sha256": "",
        "authenticode": {},
        "valid": False,
    }
    if not path.exists() or not path.is_file():
        return result
    result["size"] = path.stat().st_size
    result["extension_ok"] = path.suffix.lower() == expected_ext.lower()
    result["size_ok"] = result["size"] >= min_bytes
    head = read_head(path, 256)
    result["head_hex"] = head[:16].hex(" ").upper()
    result["mz_header"] = head.startswith(b"MZ") if expected_ext.lower() in [".exe", ".msi"] else True
    result["looks_html"] = head.lstrip().lower().startswith((b"<!doctype html", b"<html"))
    result["sha256"] = sha256_file(path)
    result["authenticode"] = authenticode(path) if expected_ext.lower() in [".exe", ".msi"] else {}
    result["valid"] = (
        result["extension_ok"]
        and result["size_ok"]
        and result["mz_header"]
        and not result["looks_html"]
    )
    return result


def write_reports(evidence_dir: Path, name: str, result: dict) -> None:
    evidence_dir.mkdir(parents=True, exist_ok=True)
    (evidence_dir / f"{name}.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    rows = []
    for key, value in result.items():
        if isinstance(value, (dict, list)):
            shown = html.escape(json.dumps(value, ensure_ascii=False, indent=2))
            rows.append(f"<tr><th>{html.escape(key)}</th><td><pre>{shown}</pre></td></tr>")
        else:
            rows.append(f"<tr><th>{html.escape(key)}</th><td>{html.escape(str(value))}</td></tr>")
    page = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>可信浏览器下载证据</title>
<style>
body{{font-family:Segoe UI,Microsoft YaHei,sans-serif;margin:32px;line-height:1.55;color:#1f2937;background:#f8fafc}}
h1{{font-size:26px;margin:0 0 12px}}
.status{{display:inline-block;padding:6px 10px;border-radius:6px;background:#111827;color:white;font-weight:700}}
table{{border-collapse:collapse;width:100%;background:white;margin-top:18px}}
th,td{{border:1px solid #d1d5db;padding:10px;vertical-align:top;text-align:left}}
th{{width:240px;background:#f3f4f6}}
pre{{white-space:pre-wrap;margin:0}}
a{{color:#2563eb}}
</style>
</head>
<body>
<h1>可信浏览器下载证据</h1>
<p>状态：<span class="status">{html.escape(str(result.get("status", "UNKNOWN")))}</span></p>
<p>说明：本页记录真实浏览器页面、点击链接、下载文件与校验结果，不代表已经安装成功。</p>
<table>{''.join(rows)}</table>
</body>
</html>"""
    (evidence_dir / f"{name}.html").write_text(page, encoding="utf-8")


async def run(args: argparse.Namespace) -> dict:
    download_dir = Path(args.download_dir)
    evidence_dir = Path(args.evidence_dir)
    download_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    screenshot = evidence_dir / "official-download-page-screenshot.png"
    after_click = evidence_dir / "browser-download-after-click.png"
    result = {
        "created_at": now(),
        "status": "STARTED",
        "method": "真实浏览器打开可信网页并点击页面上的下载链接",
        "page_url": args.page_url,
        "download_dir": str(download_dir),
        "allow_hosts": args.allow_host,
        "link_contains": args.link_contains,
        "clicked_href": "",
        "suggested_filename": "",
        "downloaded_file": "",
        "source_page_screenshot": str(screenshot),
        "after_click_screenshot": str(after_click),
        "download_validation": {},
        "error": "",
    }
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(evidence_dir / "chrome-human-download-profile"),
            channel=args.channel,
            headless=False,
            accept_downloads=True,
            downloads_path=str(download_dir),
            viewport={"width": 1440, "height": 1000},
        )
        page = context.pages[0] if context.pages else await context.new_page()
        try:
            await page.goto(args.page_url, wait_until="domcontentloaded", timeout=args.page_timeout_ms)
            await page.wait_for_timeout(2500)
            await page.screenshot(path=str(screenshot), full_page=True)
            anchors = await page.locator("a").evaluate_all(
                """els => els.map(a => ({
                    text: (a.innerText || a.textContent || '').trim(),
                    href: a.href || '',
                    aria: a.getAttribute('aria-label') || ''
                }))"""
            )
            result["anchors_seen"] = anchors
            candidates = []
            for anchor in anchors:
                href = anchor.get("href") or ""
                host_ok = not args.allow_host or urlparse(href).hostname in args.allow_host
                contains_ok = all(s.lower() in href.lower() for s in args.link_contains)
                ext_ok = href.lower().split("?")[0].endswith(args.expected_ext.lower())
                if host_ok and contains_ok and ext_ok:
                    candidates.append(anchor)
            if not candidates:
                raise RuntimeError("未在可信页面中找到符合 allow-host/link-contains/expected-ext 的下载链接")
            chosen = candidates[0]
            href = chosen["href"]
            result["clicked_href"] = href
            locator = page.locator(f"a[href='{href}']").first
            async with page.expect_download(timeout=args.download_timeout_ms) as download_info:
                await locator.click()
            download = await download_info.value
            result["suggested_filename"] = download.suggested_filename
            target = download_dir / download.suggested_filename
            await download.save_as(str(target))
            await page.screenshot(path=str(after_click), full_page=True)
            result["downloaded_file"] = str(target)
            result["download_validation"] = validate_file(target, args.expected_ext, args.min_bytes)
            result["status"] = "DOWNLOADED_VALIDATED" if result["download_validation"]["valid"] else "DOWNLOADED_INVALID"
        except Exception as exc:
            result["status"] = "DOWNLOAD_FAILED"
            result["error"] = repr(exc)
            try:
                await page.screenshot(path=str(evidence_dir / "browser-download-failed.png"), full_page=True)
            except Exception:
                pass
        finally:
            await context.close()
    write_reports(evidence_dir, args.report_name, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--page-url", required=True)
    parser.add_argument("--download-dir", required=True)
    parser.add_argument("--evidence-dir", required=True)
    parser.add_argument("--allow-host", action="append", default=[])
    parser.add_argument("--link-contains", action="append", default=[])
    parser.add_argument("--expected-ext", default=".exe")
    parser.add_argument("--min-bytes", type=int, default=1)
    parser.add_argument("--channel", default="chrome")
    parser.add_argument("--page-timeout-ms", type=int, default=60000)
    parser.add_argument("--download-timeout-ms", type=int, default=600000)
    parser.add_argument("--report-name", default="official-download-evidence")
    args = parser.parse_args()
    result = asyncio.run(run(args))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "DOWNLOADED_VALIDATED":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
